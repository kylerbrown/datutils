from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import ewave

from datutils.utils import load_dat, BUFFER_SIZE


def dat2wav(datfile, wavfile=None):
    if wavfile is None:
        wavfile = datfile + ".wav"
    data, params = load_dat(datfile)
    rate = params["sampling_rate"]
    nchannels = params["n_channels"]
    dtype = params["dtype"]
    with ewave.open(wavfile,
                    "w+",
                    sampling_rate=rate,
                    dtype=dtype,
                    nchannels=nchannels) as wavfp:
        for i in range(0, len(data), nchannels * BUFFER_SIZE):
            buffer = data[i:i + nchannels * BUFFER_SIZE]
            wavfp.write(buffer)

def main():
    import argparse
    p = argparse.ArgumentParser(prog="dat2wav.py")
    p.add_argument("dat", help="dat file to convert to wav, can be any number of channels but you probably want 1 or 2")
    p.add_argument("-o", "--out", help="name of output wav file")
    options = p.parse_args()
    dat2wav(options.dat, options.out)

if __name__ == "__main__":
    main()
    
