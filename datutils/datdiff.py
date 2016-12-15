from __future__ import unicode_literals, print_function, division, \
absolute_import

import numpy as np
from datutils.utils import load_dat, create_dat, BUFFER_SIZE

def datdiff(datfile, outfile, channels):
    if not channels:
        channels = (0, 1)
    assert len(channels) == 2

    data, params = load_dat(datfile)
    outparams = params.copy()
    outparams['n_channels'] = 1
    out = create_dat(outfile, outparams)
    for i in range(0, len(out), BUFFER_SIZE):
        out[i:i+BUFFER_SIZE] = (data[i:i+BUFFER_SIZE, channels[0]] -
                                data[i:i+BUFFER_SIZE, channels[1]]
                                ).reshape(-1, 1)

def main():
    import argparse
    p = argparse.ArgumentParser(description="""
    Subtracts one channel from another
    """)
    p.add_argument("dat", help="dat file")
    p.add_argument("-c", "--channels",
            help="channels to difference, zero indexed, default: 0 1, subtracts second channel from first.",
            type=int, nargs="+")
    p.add_argument("-o", "--out",
                   help="name of output dat file")
    opt = p.parse_args() 
    datdiff(opt.dat, opt.out, opt.channels)

if __name__ == "__main__":
    main()
