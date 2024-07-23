import sys
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import json
from .phononweb.qephonon_qetools import QePhononQetools
from ..tool import kayser2meV
from ..high_symmetry_point import HighSymmetryPointFigureProps


class Phonon():

    def __init__(
        self,
        name: str,
        scf_in_path:  str = 'scf.in',
        scf_out_path: str = 'scf.out',
        flvec_path:   str = 'matdyn.modes',
        matdyn_freq_in_path: str | None = None,
        highsym_qpts_names: list[str] | None = None,
        json_out_path: str | None = None,
        **kwargs
    ) -> None:

        self.phonon_props = self.read_phonon_props(
            name          = name,
            scf_in_path   = scf_in_path,
            scf_out_path  = scf_out_path,
            flvec_path    = flvec_path,
            json_out_path = json_out_path,
            **kwargs
        )

        self.vectors = np.array( self.phonon_props[ 'vectors' ] )
        self.qpoints = np.array( self.phonon_props[ 'qpoints' ] )
        self.eigenvalues_kayser = np.array( self.phonon_props[ 'eigenvalues' ] )

        self.lattice      = np.array( self.phonon_props[ 'lattice' ] ) # lattice vectors (bohr)
        self.atom_types   = np.array( self.phonon_props[ 'atom_types' ] ) # atom type for each atom (string) e.g. [ 'Ga', 'N', ... ]
        self.atom_numbers = np.array( self.phonon_props[ 'atom_numbers' ] ) # atom number for each atom (integer) e.g. [ 31, 7, ... ]
        self.atom_pos_car = np.array( self.phonon_props[ 'atom_pos_car' ] ) # atomic positions in cartesian coordinates
        self.atom_pos_red = np.array( self.phonon_props[ 'atom_pos_red' ] ) # atomic positions in reduced coordinates

        self.distances    = np.array( self.phonon_props[ 'distances' ] )

        self.n_atoms   = self.phonon_props[ 'natoms' ]
        self.n_modes   = len( self.eigenvalues_kayser[0] )
        self.n_qpoints = len( self.qpoints )


        # high-symmetry q points
        if matdyn_freq_in_path is not None:
            self.highSymQPtFigProps = HighSymmetryPointFigureProps(
                matdyn_freq_in_path = matdyn_freq_in_path,
                highsym_qpts_names  = highsym_qpts_names
            )
        else:
            self.highSymQPtFigProps = None


    def set_xticks( self ) -> None:
        if self.highSymQPtFigProps is None:
            return

        tick_points = self.distances[ self.highSymQPtFigProps.ticks.indices ]
        tick_labels = self.highSymQPtFigProps.ticks.labels

        if self.n_qpoints != self.highSymQPtFigProps.n_points:
            print( '[error] Phonon.set_xticks' )
            print( 'invalid number of q points.' )
            print( self.n_qpoints, self.highSymQPtFigProps.n_points )
            sys.exit(1)


        plt.tick_params( bottom = False, top = False, which = 'major' )
        plt.tick_params( bottom = False, top = False, which = 'minor' )
        plt.grid( which = 'major', axis = 'x', color = 'k' )

        plt.xticks(
            ticks  = tick_points,
            labels = tick_labels,
            minor  = False
        )


    @staticmethod
    def read_phonon_props(
        name: str,
        scf_in_path:  str = 'scf.in',
        scf_out_path: str = 'scf.out',
        flvec_path:   str = 'matdyn.modes',
        json_out_path: str | None = None,
        **kwargs
    ) -> dict:

        with open( scf_in_path ) as f:
            scf_input = f.read()

        with open( scf_out_path ) as f:
            scf_output = f.read()

        with open( flvec_path ) as f:
            matdyn_modes = f.read()

        phonons = QePhononQetools(
            scf_input     = scf_input,
            scf_output    = scf_output,
            matdyn_modes  = matdyn_modes,
            # highsym_qpts  = [],
            # starting_reps = (),
            # reorder       = True,
            name          = name,
            **kwargs
        )
        print( phonons )

        phonon_props = phonons.get_dict()
        # Remove alat if defined (so there is no message about Quantum ESPRESSO when the JSON file is loaded)
        try:
            phonon_props.pop( 'alat' )
        except KeyError:
            pass


        #--------------------------------------------------------------#
        # export as json if json_out_path is not None
        #--------------------------------------------------------------#
        if json_out_path is not None:
            with open( json_out_path, 'w' ) as f:
                json.dump( phonon_props, f )


        return phonon_props


    def get_vector(
        self,
        i_q:    int | slice,
        i_mode: int | slice,
        i_atom: int | slice
    ) -> npt.NDArray:
        return np.array( self.vectors[ i_q, i_mode, i_atom ] )

    def get_vector_norm(
        self,
        i_q:    int | slice,
        i_mode: int | slice,
        i_atom: int | slice
    ) -> npt.NDArray:
        complex_vecs = self.get_vector( i_q=i_q, i_mode=i_mode, i_atom=i_atom )
        vecs  = np.linalg.norm( complex_vecs, axis = -1 )
        norms = np.linalg.norm( vecs, axis = -1 )
        return norms

    def get_qpoint(
        self,
        i_q: int | slice
    ) -> npt.NDArray:
        return np.array( self.qpoints[ i_q ] )

    def get_eigenvalue_kayser(
        self,
        i_q:    int | slice,
        i_mode: int | slice
    ) -> float:
        eigenvalue = self.eigenvalues_kayser[ i_q, i_mode ]
        if isinstance( eigenvalue, list ):
            eigenvalue = np.array( eigenvalue )
        return eigenvalue

    def get_eigenvalue_meV(
        self,
        i_q:    int | slice,
        i_mode: int | slice
    ) -> float:
        return kayser2meV( self.get_eigenvalue_kayser( i_q=i_q, i_mode=i_mode ) )
