import quickspikes

import numpy as np
import quickspikes as qs
from datutils.utils import load_dat, create_dat


def datspikes(datfile, thresh):
    data, params = load_dat(datfile)
    assert params["n_channels"] == 1

    tempparams = params.copy()
    tempparams["dtype"] = "float64"
    create_dat("temp.dat", tempparams)


def main():
    import argparse
    p = argparse.ArgumentParser(description="""
    detects spikes in a dat file
    """)
    p.add_argument("dat", help="dat file")
    p.add_argument("-t", "--thresh", help="threshold in samples", type=int)
    opt = p.parse_args()
    datspikes(opt.dat, opt.thresh)


if __name__ == "__main__":
    main()
