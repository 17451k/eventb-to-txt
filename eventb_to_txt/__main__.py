#!/usr/bin/env python3

# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import argparse
import glob
import os
import sys

from eventb_to_txt.context import Context
from eventb_to_txt.machine import Machine


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--in', help='set PATH to the Event-B model directory. Default one is the current directory',
                            dest='in_path', metavar='PATH', default=os.getcwd())
    arg_parser.add_argument('-o', '--out', help='set PATH to the output directory. Default one is the current directory',
                            dest='out_path', metavar='PATH', default=os.getcwd())
    args = arg_parser.parse_args()

    if not os.path.exists(args.in_path):
        sys.exit('"{}" path does not exist'.format(args.in_path))

    if not os.path.exists(args.out_path):
        sys.exit('"{}" path does not exist'.format(args.out_path))

    context_files = glob.glob(os.path.join(args.in_path, "*.buc"))
    machine_files = glob.glob(os.path.join(args.in_path, "*.bum"))

    if not context_files and not machine_files:
        sys.exit('It seems that the specified directory does not contain any Event-B models')

    for context_file in context_files:
        c = Context(context_file)
        c.print(args.out_path)

    for machine_file in machine_files:
        m = Machine(machine_file)
        m.print(args.out_path)

    print('Txt files were successfully generated')


if __name__ == '__main__':
    main()
