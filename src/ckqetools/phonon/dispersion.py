import os
import sys
import pandas as pd
from dataclasses import dataclass
from ..tool import get_file_path, kayser2meV

DISPERSION_READ_PROPS = dict(
    header           = None,
    delim_whitespace = True
)

@dataclass
class HighSymmetryPoint():
    point: list[float] | str
    tex: str
    num: int = None


class Dispersion:

    def __init__(
        self,
        high_symmetry_points: list[type[HighSymmetryPoint]] | None = None,
        path:    str | None = None,
        dirname: str | None = None,
        fname:   str  = '*.freq.gp',
        input_fname: str = 'matdyn.freq.in',
        point_names: list[str] | None = None
    ) -> None:
        """
        * if high_symmetry_points is None:
            the high symmetry points are read from input file of f"{dirname}/{input_fname}"
            (if `dirname` is None: `dirname` is determined from `path`)
        """


        #--------------------------------------------------------------#
        # read high_symmetry_points if None
        #--------------------------------------------------------------#
        if high_symmetry_points is None:
            _dirname = dirname if dirname is not None else os.path.dirname( path )
            self.input_path = get_file_path(
                dirname = _dirname,
                fname   = input_fname
            )
            print( f' * high symmetry points are read from "{self.input_path}"' )
            high_symmetry_points = self.read_high_symmetry_points( self.input_path )


        #--------------------------------------------------------------#
        # update high_symmetry_points names if None
        #--------------------------------------------------------------#
        if point_names is not None:
            if len( point_names ) != len( high_symmetry_points ):
                print( '[error] invalid length of list of point_names' )
                sys.exit(1)

            for name, high_symmetry_point in zip( point_names, high_symmetry_points ):
                high_symmetry_point.tex = self._replace_high_symmetry_point_name( name )


        #--------------------------------------------------------------#
        # read dispersion data
        #--------------------------------------------------------------#
        self.path = get_file_path(
            path    = path,
            dirname = dirname,
            fname   = fname
        )
        dispersion_df = pd.read_csv(
            self.path,
            **DISPERSION_READ_PROPS
        )
        self.wavenumber       = dispersion_df[0]
        self.frequency_kayser = dispersion_df.iloc[:, 1:]
        self.frequency_meV    = kayser2meV( self.frequency_kayser )
        self.mode_num         = self.frequency_kayser.shape[1]


        #--------------------------------------------------------------#
        # make wavenumber ticks using high-symmetry points
        #--------------------------------------------------------------#
        self.kticks = []
        self.kticklabels = []

        index_k = 0
        for i, highSymmetryPoint in enumerate( high_symmetry_points ):
            self.kticks.append( self.wavenumber[ index_k ] )
            self.kticklabels.append( highSymmetryPoint.tex )
            # print( i, index_k )
            if i == len( high_symmetry_points ) - 1:
                index_k += 1
            elif highSymmetryPoint.num is not None:
                index_k += highSymmetryPoint.num

        # check
        if index_k != len( dispersion_df[0] ):
            print( '[error] number of points is not equal to that in read file.' )
            print( index_k, len( dispersion_df[0] ) )
            sys,exit(1)


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



# high_symmetry_points = [
#     HighSymmetryPoint( point = 'gG', tex = r'$\Gamma$', num = 20 ),
#     HighSymmetryPoint( point = 'M',  tex = 'M',         num = 20 ),
#     HighSymmetryPoint( point = 'K',  tex = 'K',         num = 20 ),
#     HighSymmetryPoint( point = 'gG', tex = r'$\Gamma$', num = 20 ),
#     HighSymmetryPoint( point = 'A',  tex = 'A',         num = 20 ),
#     HighSymmetryPoint( point = 'L',  tex = 'L',         num = 20 ),
#     HighSymmetryPoint( point = 'H',  tex = 'H',         num = 20 ),
#     HighSymmetryPoint( point = 'A',  tex = 'A' )
# ]

# high_symmetry_points = [
#     HighSymmetryPoint( point = [ 0.0000000000,  0.0000000000,  0.0000000000 ], tex = r'$\Gamma$', num = 20 ),
#     HighSymmetryPoint( point = [ 0.5000000000, -0.5000000000,  0.0000000000 ], tex = 'M',         num = 20 ),
#     HighSymmetryPoint( point = [ 0.6666666667, -0.3333333333,  0.0000000000 ], tex = 'K',         num = 20 ),
#     HighSymmetryPoint( point = [ 0.0000000000,  0.0000000000,  0.0000000000 ], tex = r'$\Gamma$', num = 20 ),
#     HighSymmetryPoint( point = [ 0.0000000000,  0.0000000000,  0.5000000000 ], tex = 'A',         num = 20 ),
#     HighSymmetryPoint( point = [ 0.5000000000, -0.5000000000,  0.5000000000 ], tex = 'L',         num = 20 ),
#     HighSymmetryPoint( point = [ 0.6666666667, -0.3333333333,  0.5000000000 ], tex = 'H',         num = 20 ),
#     HighSymmetryPoint( point = [ 0.0000000000,  0.0000000000,  0.5000000000 ], tex = 'A' )
# ]

