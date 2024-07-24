#!/bin/bash -eu

ckqetools-phonon-json \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq/matdyn.freq.in \
    --phonon-json-path       result/GaN/GaN.json \
    --name                   GaN

