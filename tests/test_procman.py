import pytest

from procman.procman import *


def test_self_test(capfd):
    self_test()
    out, err = capfd.readouterr()
    assert 'procman' in out


def test_show_paths(capfd):
    show_paths()
    out, err = capfd.readouterr()
    for x in ['parsing.', 'procman.yaml', 'web', 'redis', 'examples']:
        assert x in out
