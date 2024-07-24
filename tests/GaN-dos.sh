#!/bin/bash -eu

ckqetools-phonon-dos \
    --dos-path               sample/GaN/dos/matdyn.dos \
    --savefname-extra        __GaN \
    --title                  GaN \
    --savedir                result/GaN
