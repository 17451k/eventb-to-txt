# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import os
import pytest
import tempfile

from eventb_to_txt.__main__ import main

test_model = os.path.join(os.path.dirname(__file__), 'test_model')
invalid_path = os.path.join(os.path.dirname(__file__), 'invalid_path')


def test_main_ok(tmpdir):
    main(["-i", test_model, "-o", tempfile.mkdtemp()])


def test_main_no_model(tmpdir):
    with pytest.raises(SystemExit):
        main([])


def test_main_invalid_in(tmpdir):
    with pytest.raises(SystemExit):
        main(["-i", invalid_path])


def test_main_invalid_out(tmpdir):
    with pytest.raises(SystemExit):
        main(["-o", invalid_path])
