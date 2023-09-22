import logging
import warnings

import pytest

from procman.procman import *


def test_self_test(capfd):
    with warnings.catch_warnings(record=True) as w:
        self_test()
        out, err = capfd.readouterr()
        assert 'procman' in out
        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert "Cannot verify" in str(w[-1].message)


def test_show_paths(capfd):
    show_paths()
    out, err = capfd.readouterr()
    for x in ['parsing.', 'procman.yaml', 'web', 'redis', 'examples']:
        assert x in out
