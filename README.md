# datutils

Commandline tools for creating signal processing data pipelines with continuously sampled raw binary data, also known as pulse code modulated (PCM) files, often with a `.dat` extension.

All tools stream from disk, making them fast and memory efficient.

The raw binary format is specified here: http://neurosuite.sourceforge.net/formats.html

Many electrophysiology programs can read raw binary files including

- [neuroscope](http://neurosuite.sourceforge.net)
- [Plexon offline sorter](http://www.plexon.com/products/offline-sorter)
- [Phy/klustaviewa](https://github.com/kwikteam/phy)
- [Spyking Circus](https://github.com/spyking-circus/spyking-circus)
- [Neo](https://github.com/NeuralEnsemble/python-neo)

## Installation
### Requirements

- numpy
- scipy
- matplotlib

If this sounds daunting, I recomend using [anaconda](https://www.continuum.io/downloads) which includes these packages.

### instructions

    git clone https://github.com/kylerbrown/datutils.git
    cd datutils
    python setup.py install

## metadata
The disadvantage of simple raw binary files is that no metadata are stored within the file itself. At a minimum three values a required to read a raw binary file:

- sampling rate, such as 30000
- numeric type, such as 16 bit integer or 32 bit float
- number of channels, such as 32

`datutils` solves this problem by creating simple plain-text metadata files using [YAML](http://www.yaml.org/start.html) syntax. For example, the above information would be recorded as:

    ---
    sampling_rate : 30000.0
    dtype : int16
    n_channels : 32

A metadata file can be created interactively with:

    $ dat-meta myfile.dat

creating a new file called `myfile.dat.meta`. Now you're ready to create a pipeline!

Feel free to include additional attributes to aid in analysis, such as

    experimenter: Jill
    subject: ab31
    condition: 1

## command-line tools
### getting help

All utilities have help available with the `--help` flag. For example:

    $ dat-filt --help

    dat file filtering program, uses zero-phase butterworth filter (filtfilt)

    positional arguments:
      dat                   dat file

    optional arguments:
      -h, --help            show this help message and exit
      -c CHANNELS [CHANNELS ...], --channels CHANNELS [CHANNELS ...]
                            channels to filter, zero indexed, default:all
      -o OUT, --out OUT     name of output dat file
      --order ORDER         filter order
      --highpass HIGHPASS   highpass frequency
      --lowpass LOWPASS     lowpass frequency
      -f FILTER, --filter FILTER
                            filter type: butter or bessel


### signal processing

- dat-split -- extracts channels
- dat-merge -- combines channels from different files, must have the same number of samples per channel
- dat-filt -- filters specified channels using a bessel or butterworth filter
- dat-diff -- takes the difference between two channels
- dat-ref -- reference each channel to the median of all the other channels
- dat-artifact -- removes large waveforms from a signal (remove artifacts)
- dat-enrich -- extracts segments of the data based on a csv with fields "start" and "stop". These columns of numbers must have units of seconds.

### Converters

- dat-to-wav -- creates a .wav file from the data, useful for acoustic analysis
- dat-to-waveclus -- creates a .mat file compatible with the single electrode spike sorter [wave_clus](https://github.com/csn-le/wave_clus)

### utilities

- dat-meta -- create a .meta file interactively. Only required for the first file in the pipeline, the rest are created automatically.

### robust pipelines with Make

Pairing `make` with datutils is highly recomended. For an introduction to make for scientists see https://swcarpentry.github.io/make-novice/

## custom analysis
Easily read and manipulate raw binary files from within Python:

    from datutils import load_dat
    data, parameters = load_dat("myfile.dat")

The `data` object is [memory mapped](https://docs.scipy.org/doc/numpy/reference/generated/numpy.memmap.html), meaning files larger than the available RAM can be loaded.

