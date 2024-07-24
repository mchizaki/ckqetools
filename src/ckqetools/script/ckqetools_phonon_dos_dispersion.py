#!/usr/bin/env python
"""
* Written by CK
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import ckplotlib.ckplot as cplt

from ckqetools.phonon.dos import DOS
from ckqetools.phonon.phonon import Phonon
from ckqetools.pyrun_props.add_argument import (
    addarg_highsym_pts_labels,
    addarg_phonon,
    addarg_dos,
    addarg_matdyn_freq_input,
    addarg_kayser,
    addarg_saveprops,
    addarg_figprops
)

SAVE_FNAME = 'dos_dispersion'
DISPERSION_PLOT_PROPS = dict(
    color = cplt.ckcolor['blue'],
    linewidth = 1
)
DOS_PLOT_PROPS = dict(
    color = cplt.ckcolor['blue'],
    linewidth = 1
)


def main():
    #==============================================================#
    # Arguments
    #==============================================================#
    parser = argparse.ArgumentParser(
        description = 'plot DOS and dispersion from "matdyn.dos" and "matdyn.modes" files. \
            input and output file of scf calculation are also required.'
    )

    addarg_dos( parser )
    addarg_phonon( parser )
    addarg_matdyn_freq_input( parser )
    addarg_highsym_pts_labels( parser )
    addarg_kayser( parser )

    addarg_saveprops( parser )
    addarg_figprops( parser )
    parser.add_argument(
        '--colorful',
        action = 'store_true',
        help   = 'flag: dispersion lines are colorful'
    )

    args = parser.parse_args()


    #==============================================================#
    # Main
    #==============================================================#
    dos = DOS(
        path = args.dos_path
    )

    phonon = Phonon(
        name                = args.name,
        scf_in_path         = args.scf_input_path,
        scf_out_path        = args.scf_output_path,
        flvec_path          = args.flvec_path,
        matdyn_freq_in_path = args.matdyn_freq_input_path,
        json_out_path       = args.phonon_json_path,
        highsym_qpts_labels = args.high_symmetry_point_labels,
        reorder             = not args.disable_reorder
    )




    #--------------------------------------------------------------#
    # Dispersion (meV)
    #--------------------------------------------------------------#
    if args.colorful:
        DISPERSION_PLOT_PROPS.pop( 'color' )
    if args.kayser:
        freq_unit_label = 'Frequency (cm$^{-1}$)'
        get_eigenvalues = phonon.get_eigenvalue_kayser
        dos_freq = dos.frequency_kayser
    else:
        freq_unit_label = 'Energy (meV)'
        get_eigenvalues = phonon.get_eigenvalue_meV
        dos_freq = dos.energy_meV

    margins = [
        0.05 if args.vmin is None else 0,
        0.05 if args.vmax is None else 0
    ]

    dos_figure_props = cplt.get_figure_props(
        save_dirname = f'{args.savedir}',
        save_fname   = f'{SAVE_FNAME}{args.savefname_extra}',
        plt_props = dict(
            xlabel = 'DOS'
        ),
        ymin = args.vmin,
        ymax = args.vmax,
        axes_xmargins = [ 0, 0.05 ],
        axes_ymargins = margins,
        common_xlim = False
    )
    dispersion_figure_props = cplt.get_figure_props(
        plt_props = dict(
            xlabel = 'Wavenumber',
            ylabel = freq_unit_label,
        ),
        ymin = args.vmin,
        ymax = args.vmax,
        axes_xmargins = [ 0, 0 ],
        axes_ymargins = margins,
        common_xlim = False
    )

    figure_props_list = [
        dispersion_figure_props,
        dos_figure_props
    ]

    with cplt.ckfigure( *figure_props_list, common_subplot_props = False ):
        fs = plt.rcParams[ 'figure.figsize' ]

        plt.figure( figsize = ( fs[0]*1.5, fs[1] ) )

        gs = GridSpec( nrows = 1, ncols = 2, width_ratios = [3, 1] )
        plt.subplots_adjust( wspace = 0.1 )


        #--------------------------------------------------------------#
        # Dispersion (meV)
        #--------------------------------------------------------------#
        plt.subplot( gs[0, 0] )
        for i_mode in range( phonon.n_modes ):
            q_points = []
            energies = []
            for i_group, highSymTicks in enumerate( phonon.highSymQPtFigProps.ticks_list ):
                i_start = highSymTicks.indices[0]
                i_end   = highSymTicks.indices[-1]
                slice_region = slice( i_start, i_end + 1 )

                if i_group > 0:
                    q_points.append( np.nan )
                    energies.append( np.nan )

                q_points.extend( phonon.distances[ slice_region ] )
                energies.extend( get_eigenvalues(
                    i_q    = slice_region,
                    i_mode = i_mode
                ))
            plt.plot(
                q_points,
                energies,
                **DISPERSION_PLOT_PROPS
            )

        phonon.set_xticks()


        #--------------------------------------------------------------#
        # DOS
        #--------------------------------------------------------------#
        plt.subplot( gs[0, 1] )
        plt.plot(
            dos.dos,
            dos_freq,
            **DOS_PLOT_PROPS
        )
        plt.tick_params( labelleft = False, which = 'major' )

        off_tick_keys = [
            'bottom', 'top', 'labelbottom', 'labeltop'
        ]
        for key in off_tick_keys:
            plt.tick_params( which = 'major', **{ key: False } )
            plt.tick_params( which = 'minor', **{ key: False } )

        if args.title is not None:
            plt.suptitle( args.title )


if __name__ == '__main__':
    main()
