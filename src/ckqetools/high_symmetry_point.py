"""
* Written by CK
"""
import sys
from dataclasses import dataclass, field

@dataclass
class HighSymmetryPoint():
    point: list[float] | str
    tex: str
    num: int = None


@dataclass
class HighSymmetryPointTicks():
    indices: list[int] = field( default_factory = list )
    labels:  list[str] = field( default_factory = list )


class HighSymmetryPointFigureProps():
    ticks: type[HighSymmetryPointTicks]
    ticks_list: list[type[HighSymmetryPointTicks]]
    n_points: int

    def __init__(
        self,
        matdyn_freq_in_path: str = 'matdyn.freq.in',
        highsym_point_names: list[str] | None = None
    ):
        highsym_pts = self.read_high_symmetry_points( matdyn_freq_in_path )


        #--------------------------------------------------------------#
        # update high_symmetry_points names if None
        #--------------------------------------------------------------#
        if highsym_point_names is not None:
            if len( highsym_point_names ) != len( highsym_pts ):
                print( '[error] invalid length of list of highsym_point_names' )
                sys.exit(1)

            for name, highSymPt in zip( highsym_point_names, highsym_pts ):
                highSymPt.tex = self._replace_high_symmetry_point_name( name )


        #--------------------------------------------------------------#
        # make wavenumber ticks using high-symmetry points
        #--------------------------------------------------------------#
        self.ticks_list = [ HighSymmetryPointTicks() ]

        group_index = 0
        index_k = 0

        for i, highSymPt in enumerate( highsym_pts ):

            cut_line = False
            if i > 0:
                cut_line = ( highSymPt.point == _highSymPt.point )

            if cut_line:
                self.ticks_list.append( HighSymmetryPointTicks() )
                group_index += 1

            self.ticks_list[ group_index ].indices.append( index_k )
            self.ticks_list[ group_index ].labels.append( highSymPt.tex )

            if i == len( highsym_pts ) - 1:
                index_k += 1
            elif highSymPt.num is not None:
                index_k += highSymPt.num

            _highSymPt = highSymPt

        # self.ticks = replace( self.ticks_list[0] )
        self.ticks = HighSymmetryPointTicks(
            indices = self.ticks_list[0].indices[:],
            labels  = self.ticks_list[0].labels [:]
        )
        for _ticks in self.ticks_list[1:]:
            self.ticks.indices.extend( _ticks.indices[1:] )
            self.ticks.labels .extend( _ticks.labels [1:] )

        self.n_points = index_k

        print( '\nticks_list' )
        for _ticks in self.ticks_list:
            print( _ticks )


    def read_high_symmetry_points( self, path: str ) -> list[type[HighSymmetryPoint]]:
        high_symmetry_points = []

        is_file_end = False
        is_points_props_start = False

        def _exit_if_file_end():
            if is_file_end:
                print( '[error] high-symmetry points are not written.' )
                sys.exit(1)

        with open( path, 'r' ) as f:

            #--------------------------------------------------------------#
            # find the start of settings
            #--------------------------------------------------------------#
            while ( not is_points_props_start ):
                line = f.readline()

                is_file_end = not line
                _exit_if_file_end()

                is_points_props_start = line.strip()[0] == '/'

            #--------------------------------------------------------------#
            # read points info
            #--------------------------------------------------------------#
            points_num = int( f.readline() )
            for i in range( points_num ):
                line = f.readline()

                is_file_end = not line
                _exit_if_file_end()

                line_str = line.strip()
                if '!' in line_str:
                    line_str = line_str[ : line_str.find( '!' ) ]
                    line_str = line_str.strip()

                line_list = line_str.split()

                point: list = line_list[:-1]
                tex:   str  = self._replace_high_symmetry_point_name( point, i = i )
                num:   int  = int( line_list[-1] )

                high_symmetry_points.append(
                    HighSymmetryPoint(
                        point = point,
                        tex   = tex,
                        num   = num
                    )
                )

        return high_symmetry_points


    @staticmethod
    def _replace_high_symmetry_point_name(
        name: str | list,
        i: int | None = None
    ) -> str:

        if isinstance( name, list ):
            if len( name ) == 1:
                name = name[0]
            else:
                # name = str( name )
                # name = str( i )
                name = f'$Q_{i}$'
                return name

        if name == 'gG':
            name = r'$\mathrm{\Gamma}$'
        elif name == 'gS':
            name = r'$\mathrm{\Sigma}$'
        else:
            name = rf'$\mathrm{{{name}}}$'
        return name
