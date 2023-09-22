import logging
from pathlib import Path

import pytest
from munch import Munch

from procman.procman import *
from procman.utils import *


def test_load_base_config():
    pcfg = load_base_config()

    assert isinstance(pcfg, Munch)
    assert hasattr(pcfg, 'scripts')


def test_load_config():
    popts, pfile = load_config()

    assert isinstance(pfile, Path)
    assert isinstance(popts, Munch)


def test_load_config_env(monkeypatch):
    """monkeypatch env good test"""
    monkeypatch.setenv("PROCMAN_CFG", "testme.yml")
    _, pfile = load_config()
    assert isinstance(pfile, Path)


def test_load_config_bogus(monkeypatch):
    """monkeypatch env bogus test"""
    monkeypatch.setenv("PROCMAN_CFG", "testme.txt")
    with pytest.raises(FileTypeError) as excinfo:
        _, pfile = load_config()
    assert 'unknown file extension' in str(excinfo.value)
    assert 'testme.txt' in str(excinfo.value)


def test_get_userscripts():
    uscripts = get_userscripts(True)

    assert isinstance(uscripts, list)
    assert len(uscripts) == 2
