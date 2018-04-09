# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import os
import unittest

import utils

test_model = os.path.join(os.path.dirname(__file__), 'test_model')


class TestContext(utils.EventBTestCase):
    def test_model_C0(self):
        C = os.path.join(test_model, 'C0.buc')
        C_expected = os.path.join(test_model, 'C0_expected.txt')

        self.compare_context(C, C_expected)

    def test_model_C1(self):
        C = os.path.join(test_model, 'C1.buc')
        C_expected = os.path.join(test_model, 'C1_expected.txt')

        self.compare_context(C, C_expected)


class TestMachine(utils.EventBTestCase):
    def test_model_M0(self):
        M = os.path.join(test_model, 'M0.bum')
        M_expected = os.path.join(test_model, 'M0_expected.txt')

        self.compare_machine(M, M_expected)

    def test_model_M1(self):
        M = os.path.join(test_model, 'M1.bum')
        M_expected = os.path.join(test_model, 'M1_expected.txt')

        self.compare_machine(M, M_expected)

    def test_model_M2(self):
        M = os.path.join(test_model, 'M2.bum')
        M_expected = os.path.join(test_model, 'M2_expected.txt')

        self.compare_machine(M, M_expected)


if __name__ == '__main__':
    unittest.main()
