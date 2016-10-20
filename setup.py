from __future__ import print_function
from setuptools import setup
import re
VERSIONFILE="datutils/_version.py"
version = open(VERSIONFILE, "rt").read().split('"')[-2]

setup(
        name='datutils',
        version=version,
        url='http://github.com/kylerbrown/datutils/',
        author="Kyler Brown",
        author_email="kylerjbrown@gmail.com",
        description="signal processing tools for continuously recorded raw binary files",
        platforms="any",
        install_requires=[
            'ewave',
            'PyYAML',
            'numpy',
            'scipy',
            'matplotlib',
            ],
        long_description="""
        Commandline tools for creating data pipelines for high frequency continuously sampled data, 
        common in neuroscience, and used by programs like klustakwik and neuroscope.

        These raw binary files are also known as pulse code modulated (pcm) files and may have
        the extension .pcm or .dat.
        The format is specified at http://neurosuite.sourceforge.net/formats.html.
        """,
        entry_points = {
            "console_scripts" : [
                'dat-to-wav = datutils.dat2wav:main',
                'dat-to-waveclus = datutils.dat2wave_clus:main',
                'dat-diff = datutils.datdiff:main',
                'dat-enrich = datutils.datenrich:main',
                'dat-filt = datutils.datfilt:main',
                'dat-merge = datutils.datmerge:main',
                'dat-meta = datutils.datmeta:main',
                'dat-split = datutils.datsplit:main',
                'dat-artifact = datutils.datartifact:main',
                'dat-ref = datutils.datref:main',
                ]

            }
        )
