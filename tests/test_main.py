# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import os
import pytest
import shutil

from eventb_to_txt.__main__ import main

test_model = os.path.join(os.path.dirname(__file__), 'test_model')
invalid_path = os.path.join(os.path.dirname(__file__), 'invalid_path')


def test_main_ok_not_merge(tmpdir):
    main([test_model, "-o", str(tmpdir)])


def test_main_ok_merge(tmpdir):
    main([test_model, "-o", str(tmpdir), "-m"])


def test_main_no_model(tmpdir):
    with pytest.raises(SystemExit):
        main(["/dev/null"])


def test_main_invalid_in(tmpdir):
    with pytest.raises(SystemExit):
        main([invalid_path])


def test_main_invalid_out(tmpdir):
    with pytest.raises(SystemExit):
        main(["-o", invalid_path])


def test_main_zipfile(tmpdir):
    test_zipfile = shutil.make_archive(os.path.join(str(tmpdir), "test_model"), "zip", root_dir=test_model)
    main([test_zipfile, "-o", str(tmpdir)])
