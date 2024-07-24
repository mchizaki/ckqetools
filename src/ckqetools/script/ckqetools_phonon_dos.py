#!/usr/bin/env python
"""
* Written by CK
"""
import argparse
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt

from ckqetools.phonon.dos import DOS
from ckqetools.pyrun_props.add_argument import (
    addarg_dos,
    addarg_saveprops,
    addarg_figprops
)

SAVE_FNAME = 'dos'
PLOT_PROPS = dict(
    color     = cplt.ckcolor['blue'],
    linewidth = 1
)


def main():
    #==============================================================#
    # Arguments
    #==============================================================#
    parser = argparse.ArgumentParser(
        description = 'plot DOS from matdyn.dos file. \
            '
    )
    addarg_dos( parser )
    addarg_saveprops( parser )
    addarg_figprops( parser )

    args = parser.parse_args()


    #==============================================================#
    # Main
    #==============================================================#
    dos = DOS(
        path = args.dos_path
    )


    #--------------------------------------------------------------#
    # DOS vs Energy
    #--------------------------------------------------------------#
    margins = [
        0.05 if args.emin is None else 0,
        0.05 if args.emax is None else 0
    ]

    figure_props = cplt.get_figure_props(
        save_dirname = f'{args.savedir}',
        save_fname   = f'{SAVE_FNAME}{args.savefname_extra}',
        plt_props = dict(
            xlabel = 'Energy (meV)',
            ylabel = 'DOS',
            title = args.title
        ),
        xmin = args.emin,
        xmax = args.emax,
        axes_xmargins = margins,
        axes_ymargins = [ 0, 0.05 ]
    )
    with cplt.ckfigure( **figure_props ):
        plt.figure()
        plt.plot( dos.energy_meV, dos.dos, **PLOT_PROPS )


if __name__ == '__main__':
    main()
