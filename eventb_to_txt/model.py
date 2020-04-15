# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import collections
import glob
import os

from eventb_to_txt.context import Context
from eventb_to_txt.machine import Machine


class Model():
    def __init__(self, model_path):
        context_files = self.__find_context_files(model_path)
        machine_files = self.__find_machine_files(model_path)

        if not context_files and not machine_files:
            raise RuntimeError('It seems that the specified directory does not contain any Event-B models')

        self.model_objs = self.__parse_model(context_files, machine_files)

    @staticmethod
    def find_model_paths(in_path):
        model_paths = set()

        for path in Model.__find_context_files(in_path):
            model_paths.add(os.path.dirname(path))

        for path in Model.__find_machine_files(in_path):
            model_paths.add(os.path.dirname(path))

        if not model_paths:
            raise RuntimeError('It seems that the specified directory does not contain any Event-B models')

        return model_paths

    @staticmethod
    def __find_context_files(path):
        return glob.glob(os.path.abspath(os.path.join(path, "**/*.buc")), recursive=True)

    @staticmethod
    def __find_machine_files(path):
        return glob.glob(os.path.abspath(os.path.join(path, "**/*.bum")), recursive=True)

    def __parse_model(self, context_files, machine_files):
        model_objs = []

        for context_file in context_files:
            c = Context(context_file)
            model_objs.append(c)

        for machine_file in machine_files:
            m = Machine(machine_file)
            model_objs.append(m)

        return model_objs

    def __search_obj_by_name(self, name):
        for obj in self.model_objs:
            if obj.get_component_name() == name:
                return obj

        raise RuntimeError("Cant find object by name '{}'".format(name))

    def __get_context_print_queue(self, context):
        queue = []

        for extended in context.extends:
            queue.extend(self.__get_context_print_queue(self.__search_obj_by_name(extended)))

        queue.append(context)

        return queue

    def __get_machine_print_queue(self, machine):
        queue = []

        if machine.refines:
            refines_obj = self.__search_obj_by_name(machine.refines)
            queue.extend(self.__get_machine_print_queue(refines_obj))

        for context in machine.sees:
            context_obj = self.__search_obj_by_name(context)
            queue.extend(self.__get_context_print_queue(context_obj))

        queue.append(machine)

        return queue

    def __get_obj_print_queue(self, obj):
        if type(obj) is Machine:
            return self.__get_machine_print_queue(obj)
        elif type(obj) is Context:
            return self.__get_context_print_queue(obj)

    def __find_leaves(self):
        # Find model components that are not extended or refined
        leaves = []

        for obj in self.model_objs:
            if type(obj) is Machine:
                if obj.refines:
                    leaves.append(obj.refines)

                leaves.extend(obj.sees)

            if type(obj) is Context:
                leaves.extend(obj.extends)

        leaves = [x for x in self.model_objs if x.get_component_name() not in leaves]
        leaves.sort(key=lambda x: x.head['name'], reverse=True)

        return leaves

    def __get_print_queue(self):
        leaves = self.__find_leaves()

        queue = []

        for leaf in leaves:
            leaf_queue = self.__get_obj_print_queue(leaf)
            queue.extend([x for x in leaf_queue if x not in queue])

        # Remove duplicate entries from the queue
        return list(collections.OrderedDict.fromkeys(queue))

    def print(self, out_path, merge):
        txt_hash = dict()

        if merge:
            queue = self.__get_print_queue()
        else:
            queue = self.model_objs

        for el in queue:
            if merge:
                model_name = os.path.basename(os.path.dirname(el.path))

                txt_hash[el] = os.path.join(out_path, model_name + ".txt")
            else:
                txt_hash[el] = os.path.join(out_path, el.get_component_name() + ".txt")

            if os.path.exists(txt_hash[el]):
                os.remove(txt_hash[el])

        for el in queue:
            el.to_txt(txt_hash[el], merge)
