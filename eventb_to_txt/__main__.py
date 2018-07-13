#!/usr/bin/env python3

# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import argparse
import glob
import os
import shutil
import sys
import tempfile
import zipfile

from eventb_to_txt.context import Context
from eventb_to_txt.machine import Machine


def parse_model(context_files, machine_files):
    hierarchy = dict()

    for context_file in context_files:
        c = Context(context_file)

        hierarchy[c] = list(c.extends)

    for machine_file in machine_files:
        m = Machine(machine_file)

        hierarchy[m] = list(m.sees)
        if m.refines:
            hierarchy[m].append(m.refines)

    return hierarchy


def get_print_queue(hierarchy):
    hierarchy = dict(hierarchy)
    queue = []

    while hierarchy:
        # All contexts without references to other unprinted contexts
        # must be printed first
        for obj in hierarchy:
            if not hierarchy[obj] and hasattr(obj, 'context_head'):
                queue.append(obj)

                obj_name = obj.context_head['name']
                for another_obj in hierarchy:
                    if obj_name in hierarchy[another_obj]:
                        hierarchy[another_obj].remove(obj_name)

        # Machines without references to other unprinted contexts and machines
        # must be printed second
        for obj in hierarchy:
            if not hierarchy[obj] and hasattr(obj, 'machine_head'):
                queue.append(obj)

                obj_name = obj.machine_head['name']
                for another_obj in hierarchy:
                    if obj_name in hierarchy[another_obj]:
                        hierarchy[another_obj].remove(obj_name)

        for key in queue:
            if key in hierarchy:
                del hierarchy[key]

    return queue


def print_queue(queue, out_path, merge):
    txt_hash = dict()

    for el in queue:
        if merge:
            model_name = os.path.basename(os.path.dirname(el.path))

            txt_hash[el] = os.path.join(out_path, model_name + ".txt")
        else:
            if hasattr(el, "context_head"):
                txt_hash[el] = os.path.join(out_path, el.context_head['name'] + ".txt")
            else:
                txt_hash[el] = os.path.join(out_path, el.machine_head['name'] + ".txt")

        if os.path.exists(txt_hash[el]):
            os.remove(txt_hash[el])

    for el in queue:
        el.to_txt(txt_hash[el], merge)


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
        sys.exit('"{}" path does not exist'.format(args.in_path))

    if not os.path.exists(args.out_path):
        sys.exit('"{}" path does not exist'.format(args.out_path))

    is_zipfile = False
    if zipfile.is_zipfile(args.in_path):
        is_zipfile = True

        tmp_in = tempfile.mkdtemp()

        with zipfile.ZipFile(args.in_path) as zip_f:
            zip_f.extractall(tmp_in)

        args.in_path = tmp_in

    context_files = glob.glob(os.path.abspath(os.path.join(args.in_path, "**/*.buc")), recursive=True)
    machine_files = glob.glob(os.path.abspath(os.path.join(args.in_path, "**/*.bum")), recursive=True)

    if not context_files and not machine_files:
        sys.exit('It seems that the specified directory does not contain any Event-B models')

    hierarchy = parse_model(context_files, machine_files)
    queue = get_print_queue(hierarchy)
    print_queue(queue, args.out_path, args.merge)

    if is_zipfile:
        shutil.rmtree(args.in_path)

    print('Txt files were successfully generated')


if __name__ == '__main__':
    main(sys.argv[1:])
