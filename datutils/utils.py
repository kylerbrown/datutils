from __future__ import division, print_function, absolute_import, \
        unicode_literals

import sys
import os.path
import yaml
import numpy as np

BUFFER_SIZE = 10000


def create_dat(datfile, params):
    data = np.memmap(datfile,
                     dtype=params["dtype"],
                     mode="w+",
                     shape=(params["n_samples"], params["n_channels"]))
    write_metadata(datfile, **params)
    return data


def load_dat(datfile, mode="r"):
    """ loads raw binary file

    mode may be "r" or "r+", use "r+" for modifiying the data (not
    recommended).
    """
    params = read_metadata(datfile)
    data = np.memmap(datfile, dtype=params["dtype"], mode=mode)
    data = data.reshape(-1, params["n_channels"])
    return data, params


def read_metadata(datfile):
    metafile = datfile + ".meta"
    try:
        with open(metafile, 'r') as fp:
            params = yaml.load(fp)
        return params
    except IOError as err:
        print("""
{dat} is missing an associated .meta file, which should be named {dat}.meta

The .meta is plaintext YAML file of the following format:

---
dtype: int16
n_channels: 4
sampling_rate: 30000.0

(you may include any other metadata you like, such as experimenter, date etc.)

to create a .meta file interactively, type:
python datmeta.py {dat}
        """.format(dat=datfile))
        sys.exit(0)


def write_metadata(dat_filename, sampling_rate, n_channels, dtype, **kwargs):
    filename = dat_filename + ".meta"
    params = dict(sampling_rate=sampling_rate,
                  n_channels=n_channels,
                  dtype=dtype)
    params.update(kwargs)
    for k, v in params.items():
        if isinstance(v, (np.ndarray, np.generic)):
            params[k] = v.tolist()
    print(filename)
    print(yaml.dump(params, default_flow_style=False))
    with open(filename, 'w') as yaml_file:
        header = """# metadata for raw binary file (.dat) using YAML syntax\n---\n"""
        yaml_file.write(header)
        yaml_file.write(yaml.dump(params, default_flow_style=False))
