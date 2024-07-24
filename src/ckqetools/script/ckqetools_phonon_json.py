#!/usr/bin/env python
"""
* Written by CK
"""
import argparse

from ckqetools.phonon.phonon import Phonon
from ckqetools.pyrun_props.add_argument import (
    addarg_phonon,
    addarg_matdyn_freq_input,
    addarg_highsym_pts_labels
)

def main():
    #==============================================================#
    # Arguments
    #==============================================================#
    parser = argparse.ArgumentParser(
        description = 'get phonon json for phononwebsite from "matdyn.modes" file. \
            input and output file of scf calculation are also required.'
    )
    addarg_phonon( parser )
    addarg_matdyn_freq_input( parser )
    addarg_highsym_pts_labels( parser )

    args = parser.parse_args()


    #==============================================================#
    # Main
    #==============================================================#
    Phonon(
        name                = args.name,
        scf_in_path         = args.scf_input_path,
        scf_out_path        = args.scf_output_path,
        flvec_path          = args.flvec_path,
        json_out_path       = args.phonon_json_path,
        matdyn_freq_in_path = args.matdyn_freq_input_path,
        highsym_qpts_labels = args.high_symmetry_point_labels,
        reorder             = not args.disable_reorder
    )


if __name__ == '__main__':
    main()
