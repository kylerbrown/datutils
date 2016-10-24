from __future__ import unicode_literals, print_function, division, \
absolute_import

from datutils.utils import read_metadata, write_metadata, BUFFER_SIZE
import numpy as np


def datmerge(datfiles, outfile):
    paramsets = [read_metadata(x) for x in datfiles]
    for p in paramsets:
        assert p["dtype"] == paramsets[0]["dtype"]
        assert p["sampling_rate"] == paramsets[0]["sampling_rate"]
    params = paramsets[0].copy()
    params["n_channels"] = sum([p["n_channels"] for p in paramsets])
    datasets = [np.memmap(x,
                          dtype=p["dtype"],
                          mode="r").reshape(-1, p["n_channels"])
                for x, p in zip(datfiles, paramsets)]
    n_samples = datasets[0].shape[0]
    for d in datasets:
        assert d.shape[0] == n_samples
    out = np.memmap(outfile,
                    dtype=params["dtype"],
                    mode="w+",
                    shape=(n_samples, params["n_channels"]))
    for i in range(0, len(out), BUFFER_SIZE):
        out[i:i + BUFFER_SIZE, :] = np.column_stack((x[i:i + BUFFER_SIZE, :]
                                                     for x in datasets))
    write_metadata(outfile, **params)


def main():
    import argparse
    p = argparse.ArgumentParser(prog="datmerge",
                                description="""
            Combines dat files by adding new channels with the same number
            samples. To add additional samples, use the unix utility 'cat'.""")
    p.add_argument("dat", help="dat files", nargs="+")
    p.add_argument("-o", "--out", help="name of output dat file")
    options = p.parse_args()
    datmerge(options.dat, options.out)


if __name__ == "__main__":
    main()
