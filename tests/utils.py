# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import os
import unittest

from eventb_to_txt.context import Context
from eventb_to_txt.machine import Machine


class EventBTestCase(unittest.TestCase):
    def __init__(self, *arguments):
        self.output = ""
        super().__init__(*arguments)
        self.maxDiff = None

    def compare_context(self, context, expected):
        c = Context(context)
        context_txt = os.path.join(
            os.path.dirname(expected), c.get_component_name() + ".txt"
        )
        c.to_txt(context_txt)

        self.__compare(context_txt, expected)

    def compare_machine(self, machine, expected):
        m = Machine(machine)
        machine_txt = os.path.join(
            os.path.dirname(expected), m.get_component_name() + ".txt"
        )
        m.to_txt(machine_txt)

        self.__compare(machine_txt, expected)

    def __compare(self, output, expected):
        self.output = output

        output_str = self._read_file_to_str(output)
        expected_str = self._read_file_to_str(expected)

        self.assertEqual(expected_str, output_str)

    def tearDown(self):
        """tearDown called immediately after the test method has been called"""

        if os.path.exists(self.output):
            os.remove(self.output)

    def _read_file_to_str(self, file):
        if not os.path.exists(file):
            self.fail("File {} does not exist.".format(file))

        with open(file, "r") as file_fh:
            return "".join(file_fh.readlines())
