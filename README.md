# ckqetools
Tools to analyze results by Quantum ESPRESSO



## ckqetools-phonon-dos

```
$ ckqetools-phonon-dos -h

usage: ckqetools-phonon-dos [-h] --dos-path DOS_PATH [--savedir SAVEDIR] [--savefname-extra SAVEFNAME_EXTRA]
                            [--title TITLE] [--emin EMIN] [--emax EMAX]

plot DOS from matdyn.dos file.

options:
  -h, --help            show this help message and exit
  --dos-path DOS_PATH   matdyn.dos file path
  --savedir SAVEDIR     directory name of saved figure [default: result]
  --savefname-extra SAVEFNAME_EXTRA
                        extra file name of saved figure
  --title TITLE         title of figure [default: None]
  --emin EMIN           Emin of figure [default: 0]
  --emax EMAX           Emax of figure [default: None]
```



## ckqetools-phonon-dispersion

```
$ ckqetools-phonon-dispersion -h

usage: ckqetools-phonon-dispersion [-h] --scf-input-path SCF_INPUT_PATH --scf-output-path SCF_OUTPUT_PATH
                                   --flvec-path FLVEC_PATH [--name NAME] [--phonon-json-path PHONON_JSON_PATH]
                                   [--disable-reorder] --matdyn-freq-input-path MATDYN_FREQ_INPUT_PATH
                                   [--high-symmetry-point-names [HIGH_SYMMETRY_POINT_NAMES ...]]
                                   [--savedir SAVEDIR] [--savefname-extra SAVEFNAME_EXTRA] [--title TITLE]
                                   [--emin EMIN] [--emax EMAX] [--colorful]

plot dispersion from "matdyn.modes" file. input and output file of scf calculation are also required.

options:
  -h, --help            show this help message and exit
  --scf-input-path SCF_INPUT_PATH
                        path of input file of scf calculation
  --scf-output-path SCF_OUTPUT_PATH
                        path of output file of scf calculation
  --flvec-path FLVEC_PATH
                        path of flvec file (output of matdyn.x) [QE default: "matdyn.modes"]
  --name NAME           name [default: test]
  --phonon-json-path PHONON_JSON_PATH
                        path of output json file [default: None]
  --disable-reorder     if this oprion is "not" used: reorder eigenvalues at q by comparing the eigenvectors
                        and solve the band-crossings by phononweb
  --matdyn-freq-input-path MATDYN_FREQ_INPUT_PATH
                        path of input file to make dispersion by matdyn.x
  --high-symmetry-point-names [HIGH_SYMMETRY_POINT_NAMES ...]
                        list of high-symmetry point names [default: None]
  --savedir SAVEDIR     directory name of saved figure [default: result]
  --savefname-extra SAVEFNAME_EXTRA
                        extra file name of saved figure
  --title TITLE         title of figure [default: None]
  --emin EMIN           Emin of figure [default: 0]
  --emax EMAX           Emax of figure [default: None]
  --colorful            flag: dispersion lines are colorful
```

