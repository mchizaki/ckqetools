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
    addarg_kayser,
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
    addarg_kayser( parser )

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
        0.05 if args.vmin is None else 0,
        0.05 if args.vmax is None else 0
    ]
    if args.kayser:
        freq_unit_label = 'Frequency (cm$^{-1}$)'
        dos_freq = dos.frequency_kayser
    else:
        freq_unit_label = 'Energy (meV)'
        dos_freq = dos.energy_meV

    figure_props = cplt.get_figure_props(
        save_dirname = f'{args.savedir}',
        save_fname   = f'{SAVE_FNAME}{args.savefname_extra}',
        plt_args = dict(
            xlabel = freq_unit_label,
            ylabel = 'DOS',
            title = args.title
        ),
        xmin = args.vmin,
        xmax = args.vmax,
        axes_xmargins = margins,
        axes_ymargins = [ 0, 0.05 ]
    )
    with cplt.ckfigure( **figure_props ):
        plt.figure()
        plt.plot( dos_freq, dos.dos, **PLOT_PROPS )


if __name__ == '__main__':
    main()
