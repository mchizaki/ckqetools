#!/usr/bin/env python
"""
* Written by CK
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt

from ckqetools.phonon.phonon import Phonon
from ckqetools.pyrun_props.add_argument import (
    addarg_highsym_pts_names,
    addarg_phonon,
    addarg_matdyn_freq_input,
    addarg_saveprops,
    addarg_figprops
)

SAVE_FNAME = 'dispersion'
PLOT_PROPS = dict(
    color = cplt.ckcolor['blue'],
    linewidth = 1
)


def main():
    #==============================================================#
    # Arguments
    #==============================================================#
    parser = argparse.ArgumentParser(
        description = 'plot dispersion from "matdyn.modes" file. \
            input and output file of scf calculation are also required.'
    )

    addarg_phonon( parser )
    addarg_matdyn_freq_input( parser )
    addarg_highsym_pts_names( parser )

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
    phonon = Phonon(
        name                = args.name,
        scf_in_path         = args.scf_input_path,
        scf_out_path        = args.scf_output_path,
        flvec_path          = args.flvec_path,
        matdyn_freq_in_path = args.matdyn_freq_input_path,
        json_out_path       = args.phonon_json_path,
        highsym_qpts_names  = args.high_symmetry_point_names,
        reorder             = not args.disable_reorder
    )




    #--------------------------------------------------------------#
    # Dispersion (meV)
    #--------------------------------------------------------------#
    if args.colorful:
        PLOT_PROPS.pop( 'color' )

    margins = [
        0.05 if args.emin is None else 0,
        0.05 if args.emax is None else 0
    ]

    figure_props = cplt.get_figure_props(
        save_dirname = f'{args.savedir}',
        save_fname   = f'{SAVE_FNAME}{args.savefname_extra}',
        plt_props = dict(
            xlabel = 'Wavenumber',
            ylabel = 'Energy (meV)',
            title = args.title
        ),
        ymin = args.emin,
        ymax = args.emax,
        axes_xmargins = [ 0, 0 ],
        axes_ymargins = margins
    )


    with cplt.ckfigure( **figure_props ):
        fs = plt.rcParams[ 'figure.figsize' ]
        plt.figure( figsize = ( fs[0]*1.5, fs[1] ) )

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
                energies.extend( phonon.get_eigenvalue_meV(
                    i_q    = slice_region,
                    i_mode = i_mode
                ))
            plt.plot(
                q_points,
                energies,
                **PLOT_PROPS
            )

        phonon.set_xticks()


if __name__ == '__main__':
    main()
