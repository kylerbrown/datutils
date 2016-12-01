#!/bin/python3
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from datutils.utils import read_metadata, write_metadata, BUFFER_SIZE


def datsplit(datfile, chan_select=(), outfile=None):
    params = read_metadata(datfile)
    nchannels = params.pop("n_channels")
    dtype = params.pop("dtype")
    if not chan_select:
        chan_select = range(nchannels)
    if outfile is None:
        outfile = datfile + "_".join([str(x) for x in chan_select]) + ".dat"
    nbuf = nchannels * BUFFER_SIZE
    data = np.memmap(datfile, dtype=dtype, mode="r")
    with open(outfile, "wb") as outfp:
        for i in range(0, len(data), nbuf):
            buffer = data[i:i + nbuf]
            mask = np.zeros_like(buffer, dtype=np.bool).reshape(-1, nchannels)
            mask[:, chan_select] = True
            outfp.write(buffer[mask.ravel()].tobytes())
    write_metadata(outfile, n_channels=len(chan_select), dtype=dtype, **params)


def main():
    import argparse
    p = argparse.ArgumentParser(prog="dat2wav.py")
    p.add_argument("dat", help="dat file")
    p.add_argument("-c",
                   "--chan-select",
                   help="channels to extract",
                   nargs="+",
                   type=int,
                   required=True)
    p.add_argument("-o", "--out", help="name of output dat file")
    options = p.parse_args()
    datsplit(options.dat, options.chan_select, options.out)


if __name__ == "__main__":
    main()
