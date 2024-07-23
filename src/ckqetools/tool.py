import os
import sys
from glob import glob

ELEMENTARY_CHARGE     = 1.602176634e-19
PLANCK_CONSTANT       = 6.62607015e-34
LIGHT_SPEED_IN_VACUUM = 2.99792458e8

def J2meV( E ):
    return E / ELEMENTARY_CHARGE * 1e3

def kayser2meV( k ):
    return J2meV( PLANCK_CONSTANT * LIGHT_SPEED_IN_VACUUM * ( k * 100 ) )


def get_file_path(
    path:    str | None = None,
    dirname: str | None = None,
    fname  : str  = '*.dat'
) -> str:

    if path is None and dirname is None:
        print( '[error] both path and dirname are None.' )
        sys.exit(1)

    if path is not None:
        if not os.path.isfile( path ):
            print( f'[error] file of name "{path}" is not found.' )
            sys.exit(1)

    if path is None and dirname is not None:
        path_fmt = os.path.join( dirname, fname )
        path_list = glob( path_fmt )
        len_path_list = len( path_list )

        if len_path_list == 0:
            print( f'[error] file of name "{path_fmt}" is not found.' )
            sys.exit(1)

        if len_path_list > 1:
            print( f'[error] there are multiple files of name "{path_fmt}".' )
            sys.exit(1)

        path = path_list[0]

    return path
