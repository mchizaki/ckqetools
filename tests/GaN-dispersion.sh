#!/bin/bash -eu

ckqetools-phonon-dispersion \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq/matdyn.freq.in \
    --savefname-extra        __GaN \
    --title                  GaN \
    --savedir                result/GaN
