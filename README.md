[![Build Status](https://travis-ci.org/17451k/eventb-to-txt.svg?branch=master)](https://travis-ci.org/17451k/eventb-to-txt)
[![Coverage Status](https://coveralls.io/repos/github/17451k/eventb-to-txt/badge.svg?branch=master)](https://coveralls.io/github/17451k/eventb-to-txt?branch=master)

# Event-B to txt converter

The eventb-to-txt script simply converts Event-B machines and contexts (.bum and .buc files) to the plain text. This text itself is a valid Event-B model that can be used in the Camille editor.

Compatible with Event-B models created with Rodin 3.0 and above.

# Installation

Just clone the repository and run the following command from its root directory:

    $ pip install .

# Usage

    usage: eventb-to-txt [-h] [-i PATH] [-o PATH]

    optional arguments:
        -h, --help           show this help message and exit
        -i PATH, --in PATH   set PATH to the Event-B model directory. Default one is
                            the current directory
        -o PATH, --out PATH  set PATH to the output directory. Default one is the
                            current directory
