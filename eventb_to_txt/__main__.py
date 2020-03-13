#!/usr/bin/env python3

# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import argparse
import os
import shutil
import sys
import tempfile
import zipfile

from eventb_to_txt.model import Model


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out', help='PATH to the output directory',
                        dest='out_path', metavar='PATH', default=os.getcwd())
    parser.add_argument("-m", "--merge", help="merge all generated txt files into a single txt file",
                        action="store_true")
    parser.add_argument(help="path to the Event-B model directory or zipfile",
                        dest="in_path", nargs=argparse.OPTIONAL, default=os.getcwd())

    args = parser.parse_args(args)

    if not os.path.exists(args.in_path):
        sys.exit('{!r} path does not exist'.format(args.in_path))

    try:
        os.makedirs(args.out_path, exist_ok=True)
    except (OSError, PermissionError, TypeError, AttributeError) as e:
        sys.exit("{}: Can't create output directory {!r}".format(type(e).__name__, args.out_path))

    is_zipfile = False
    if zipfile.is_zipfile(args.in_path):
        is_zipfile = True

        tmp_in = tempfile.mkdtemp()

        with zipfile.ZipFile(args.in_path) as zip_f:
            zip_f.extractall(tmp_in)

        args.in_path = tmp_in

    try:
        for model_path in Model.find_model_paths(args.in_path):
            m = Model(model_path)
            m.print(args.out_path, args.merge)
    except RuntimeError as e:
        raise SystemExit(e)
    except (OSError, PermissionError) as e:
        raise SystemExit("{}: {}".format(type(e).__name__, e))

    if is_zipfile:
        shutil.rmtree(args.in_path)

    print('Txt files were successfully generated')


if __name__ == '__main__':
    main(sys.argv[1:])
