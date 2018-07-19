# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import glob
import os

from eventb_to_txt.context import Context
from eventb_to_txt.machine import Machine


def uniqify(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


class Model():
    def __init__(self, in_path):
        context_files = glob.glob(os.path.abspath(os.path.join(in_path, "**/*.buc")), recursive=True)
        machine_files = glob.glob(os.path.abspath(os.path.join(in_path, "**/*.bum")), recursive=True)

        if not context_files and not machine_files:
            raise RuntimeError('It seems that the specified directory does not contain any Event-B models')

        self.model_objs = self.__parse_model(context_files, machine_files)

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
            if type(obj) is Context and obj.context_head["name"] == name:
                return obj
            if type(obj) is Machine and obj.machine_head["name"] == name:
                return obj

        raise RuntimeError("Cant find object by name '{}'".format(name))

    def __get_context_print_queue(self, context):
        if not context:
            return []

        queue = []

        for extended in context.extends:
            queue.extend(self.__get_context_print_queue(self.__search_obj_by_name(extended)))

        queue.append(context)

        return queue

    def __get_machine_print_queue(self, machine):
        if not machine:
            return []

        queue = []

        if machine.refines:
            refines_obj = self.__search_obj_by_name(machine.refines)
            queue.extend(self.__get_machine_print_queue(refines_obj))

        for context in machine.sees:
            context_obj = self.__search_obj_by_name(context)
            queue.extend(self.__get_context_print_queue(context_obj))

        queue.append(machine)

        return queue

    def __get_print_queue(self):
        queue = []

        for obj in self.model_objs:
            if type(obj) is Machine:
                obj_queue = self.__get_machine_print_queue(obj)
            elif type(obj) is Context:
                obj_queue = self.__get_context_print_queue(obj)

            obj_queue = uniqify(obj_queue)
            if len(obj_queue) >= len(queue):
                queue = obj_queue

        return queue

    def print(self, out_path, merge):
        txt_hash = dict()

        queue = self.__get_print_queue()

        for el in queue:
            if merge:
                model_name = os.path.basename(os.path.dirname(el.path))

                txt_hash[el] = os.path.join(out_path, model_name + ".txt")
            else:
                if type(el) is Context:
                    txt_hash[el] = os.path.join(out_path, el.context_head['name'] + ".txt")
                else:
                    txt_hash[el] = os.path.join(out_path, el.machine_head['name'] + ".txt")

            if os.path.exists(txt_hash[el]):
                os.remove(txt_hash[el])

        for el in queue:
            el.to_txt(txt_hash[el], merge)
