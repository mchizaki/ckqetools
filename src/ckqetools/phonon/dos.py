import pandas as pd
from ..tool import get_file_path, kayser2meV

COL_FREQ = 'Frequency [cm^-1]'
COL_DOS  = 'DOS'
DOS_READ_PROPS = dict(
    header           = None,
    delim_whitespace = True,
    skiprows         = 1
)

class DOS:

    def __init__(
        self,
        path:    str | None = None,
        dirname: str | None = None,
        fname:   str  = 'matdyn.dos'
    ) -> None:

        self.path = get_file_path(
            path    = path,
            dirname = dirname,
            fname   = fname
        )

        dos_df = pd.read_csv(
            self.path,
            usecols = [ 0, 1 ],
            names   = [ COL_FREQ, COL_DOS ],
            **DOS_READ_PROPS
        )

        self.frequency_kayser = dos_df[ COL_FREQ ]
        self.energy_meV       = kayser2meV( self.frequency_kayser )
        self.dos              = dos_df[ COL_DOS  ]
