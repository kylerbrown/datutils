from __future__ import unicode_literals, print_function, division, \
absolute_import
import numpy as np
from scipy.io import savemat
from datutils.utils import load_dat, create_dat, BUFFER_SIZE
BUF = BUFFER_SIZE


def dat2wave_clus(datfile, outfile):
    data, params = load_dat(datfile)
    sr = params["sampling_rate"]

    savemat(outfile, {"data": data.T, "sr": sr}, appendmat=False)

def main():
    import argparse
    p = argparse.ArgumentParser(prog="dat2wave_clus",
                                description="""
    Converts a raw binary file to a wav_clus compatible matlab file
    """)
    p.add_argument("dat", help="dat file")
    p.add_argument("-o", "--out", help="name of output .mat file")
    options = p.parse_args()
    dat2wave_clus(options.dat, options.out)

if __name__ == "__main__":
    main()
