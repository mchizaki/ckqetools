"""
* Written by CK
"""
from argparse import ArgumentParser


def addarg_phonon(
    parser: ArgumentParser
):
    parser.add_argument(
        '--scf-input-path', type=str, required=True,
        help = 'path of input file of scf calculation'
    )
    parser.add_argument(
        '--scf-output-path', type=str, required=True,
        help = 'path of output file of scf calculation'
    )
    parser.add_argument(
        '--flvec-path', type=str, required=True,
        help = 'path of flvec file (output of matdyn.x) [QE default: "matdyn.modes"]'
    )
    parser.add_argument(
        '--name', type=str, default='test',
        help = 'name [default: test]'
    )
    parser.add_argument(
        '--phonon-json-path', type=str, default=None,
        help = 'path of output json file [default: None]'
    )
    parser.add_argument(
        '--disable-reorder', action='store_true',
        help = 'if this oprion is "not" used: \
            reorder eigenvalues at q by comparing the eigenvectors \
            and solve the band-crossings by phononweb\
            '
    )
    return 'scf_input_path', 'scf_output_path', 'flvec_path', 'name', 'phonon_json_path', 'disable_reorder'


def addarg_matdyn_freq_input(
    parser: ArgumentParser
):
    parser.add_argument(
        '--matdyn-freq-input-path', type=str, required=True,
        help = 'path of input file to make dispersion by matdyn.x'
    )
    return 'matdyn_freq_input_path'


def addarg_dos(
    parser: ArgumentParser
):
    parser.add_argument(
        '--dos-path', type=str, required=True,
        help = f'matdyn.dos file path'
    )
    return 'dos_path'


def addarg_dispersion(
    parser: ArgumentParser
):
    parser.add_argument(
        '--dispersion-path', type=str, required=True,
        help = '*.freq.gp file path'
    )
    return 'dispersion_path'


def addarg_highsym_pts_names(
    parser: ArgumentParser
):
    parser.add_argument(
        '--high-symmetry-point-names', nargs='*', type=str, default=None,
        help = 'list of high-symmetry point names [default: None]'
    )
    return 'qpoint_names'


def addarg_saveprops(
    parser: ArgumentParser,
    default_savedir: str = 'result'
) -> tuple[str]:
    """
    * --savedir
    * --savefname_extra
    """
    parser.add_argument(
        '--savedir', default=default_savedir, type=str,
        help = f'directory name of saved figure [default: {default_savedir}]'
    )
    parser.add_argument(
        '--savefname-extra', default='', type=str,
        help='extra file name of saved figure'
    )
    return 'savedir', 'savefname_extra'


def addarg_figprops(
    parser: ArgumentParser
):
    parser.add_argument(
        '--title', type=str, default=None,
        help = f'title of figure [default: {None}]'
    )
    parser.add_argument(
        '--emin', type=float, default=0,
        help = f'Emin of figure [default: {0}]'
    )
    parser.add_argument(
        '--emax', type=float, default=None,
        help = f'Emax of figure [default: {None}]'
    )
    return 'title', 'emin', 'emax'

