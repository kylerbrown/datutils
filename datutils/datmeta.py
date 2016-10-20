from builtins import input

from datutils.utils import write_metadata


def datmeta(datfiles):
    sr = False
    while not sr:
        try:
            print("sampling rate:")
            isr = float(input())
            assert isr > 0
            sr = isr
        except:
            pass
    n_channels = False
    while not n_channels:
        try:
            print("number of channels:")
            in_channels = int(input())
            assert in_channels > 0
            n_channels = in_channels
        except:
            pass

    dtype = False
    while not dtype:
        try:
            print("datatype, probably int16 or float64:")
            idtype = input()
            assert idtype in ('int8', 'int16', 'int32', 'int64', 'float32',
                              'float64', 'float128', 'uint8', 'uint16',
                              'uint32', 'uint64')
            dtype = idtype
        except:
            pass
    for datfile in datfiles:
        write_metadata(datfile,
                       n_channels=n_channels,
                       sampling_rate=sr,
                       dtype=dtype)


def main():
    import argparse
    p = argparse.ArgumentParser(prog="datmerge.py",
                                description="""
    Generates metadata files for raw binary files, accepts multiple files
    (assuming the have the same metadata parameters).
    
    Feel free to create .meta files yourself and include other parameters.
    The .meta files use YAML syntax.
    """)
    p.add_argument("dat", help="dat file(s)", nargs="+")
    options = p.parse_args()
    datmeta(options.dat)


if __name__ == "__main__":
    main()
