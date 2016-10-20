from __future__ import unicode_literals, print_function, division, \
absolute_import

import numpy as np
from scipy.signal import butter, lfilter
from datutils.utils import load_dat, create_dat, BUFFER_SIZE, \
        write_metadata
BUF = BUFFER_SIZE


def datref(datfile, outfile):
    data, params = load_dat(datfile)
    outparams = params.copy()
    out = create_dat(outfile, outparams)
    # determine reference coefficient
    n_channels = params["n_channels"]
    coefs = np.zeros((n_channels, len(range(0, len(out), BUF))))
    power = np.zeros_like(coefs)
    b, a = butter(3, 500 / (params["sampling_rate"] / 2), btype="lowpass")
    for ith, i in enumerate(range(0, len(out), BUF)):
        for c in range(n_channels):
            refs = np.delete(data[i:i + BUF, :], c, axis=1)  # remove col c
            #refs = data[i:i+BUF,:]
            ref = np.mean(refs, axis=1)
            #ref = lfilter(b, a, ref)
            x = data[i:i + BUF, c]
            #x = lfilter(b, a, x)
            coefs[c, ith] = np.dot(x, ref) / np.dot(ref, ref)

    best_C = np.zeros(n_channels)
    for c in range(n_channels):
        c_coefs = coefs[c, :]
        c_power = power[c, :]
        mask = c_power >= np.percentile(c_power, 90)
        best_C[c] = np.mean(c_coefs[mask])
    print("best reference coefficients: {}".format(best_C))
    outparams["reference_coefficients"] = best_C.tolist()
    for i in range(0, len(out), BUF):
        for c in range(n_channels):
            refs = np.delete(data[i:i + BUF, :], c, axis=1)  # remove col c
            #refs = data[i:i+BUF,:]
            ref = np.mean(refs, axis=1)
            x = data[i:i + BUF, c]
            out[i:i + BUF, c] = data[i:i + BUF, c] - best_C[c] * np.median(
                refs,
                axis=1)
    write_metadata(outfile, **outparams)


def main():
    import argparse
    p = argparse.ArgumentParser(description="""
    References each channel from the median of all the others
    """)
    p.add_argument("dat", help="dat file")
    p.add_argument("-o", "--out", help="name of output dat file")
    opt = p.parse_args()
    datref(opt.dat, opt.out)
if __name__ == "__main__":
    main()
