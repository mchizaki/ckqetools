#!/bin/bash -eu

# colorful
ckqetools-phonon-dispersion \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq/matdyn.freq.in \
    --savefname-extra        __GaN_colorful \
    --title                  GaN \
    --savedir                result/GaN \
    --colorful

# 100 intervals
ckqetools-phonon-dispersion \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq100/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq100/matdyn.freq.in \
    --savefname-extra        __GaN_100 \
    --title                  GaN \
    --savedir                result/GaN

# qpointsspecs
ckqetools-phonon-dispersion \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq_qpointsspecs/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq_qpointsspecs/matdyn.freq.in \
    --savefname-extra        __GaN_qpointsspecs \
    --title                  GaN \
    --savedir                result/GaN

# qpointsspecs (with high-symmetry-point-labels option)
ckqetools-phonon-dispersion \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq_qpointsspecs/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq_qpointsspecs/matdyn.freq.in \
    --savefname-extra        __GaN_qpointsspecs_w_highsym_labels \
    --title                  GaN \
    --savedir                result/GaN \
    --high-symmetry-point-labels gG M K gG gG A L H A 

# disable-reorder
ckqetools-phonon-dispersion \
    --scf-input-path         sample/GaN/scf.in \
    --scf-output-path        sample/GaN/scf.out \
    --flvec-path             sample/GaN/freq/matdyn.modes \
    --matdyn-freq-input-path sample/GaN/freq/matdyn.freq.in \
    --savefname-extra        __GaN_reorder \
    --title                  GaN \
    --savedir                result/GaN \
    --colorful --disable-reorder

