![test](https://github.com/17451k/eventb-to-txt/workflows/test/badge.svg)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/eventb-to-txt.svg)](https://pypi.python.org/pypi/eventb-to-txt/)
[![PyPI version](https://badge.fury.io/py/eventb-to-txt.svg)](https://badge.fury.io/py/eventb-to-txt)

# Event-B to txt converter
The eventb-to-txt script simply converts Event-B machines and contexts (.bum and .buc files) to the plain text. This text itself is a valid Event-B model that can be used in the CamilleX editor.

Compatible with Event-B models created with Rodin 3.0 and above.

## Installation
```
    $ python3 -m pip install eventb-to-txt
```

## Usage
```
    usage: eventb-to-txt [-h] [-o PATH] [-m] [in_path]

    positional arguments:
    in_path              path to the Event-B model directory or zipfile

    optional arguments:
    -h, --help           show this help message and exit
    -o PATH, --out PATH  PATH to the output directory
    -m, --merge          merge all generated txt files into a single txt file
```
