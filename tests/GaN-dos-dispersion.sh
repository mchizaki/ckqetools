#!/bin/bash -eu

ckqetools-phonon-dos-dispersion \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq/matdyn.freq.in \
    --dos-path               sample/GaN/dos/matdyn.dos \
    --savefname-extra        __GaN \
    --title                  GaN \
    --savedir                result/GaN
