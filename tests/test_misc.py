import logging
from pathlib import Path

import pytest
from munch import Munch

import procman
from procman.utils import (
    FileTypeError,
    get_userscripts,
    load_base_config,
    load_config,
)


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
    assert 'invalid YAML extension' in str(excinfo.value)
    assert 'testme.txt' in str(excinfo.value)


def test_get_userscripts():
    popts, pfile = load_config()
    uscripts = get_userscripts(popts, pfile, True)
    print(uscripts)

    assert isinstance(uscripts, list)
    assert len(uscripts) == 2

    for item in uscripts:
        assert isinstance(item, list)
        path_str = item[1].split()[1]
        print(path_str)
        assert isinstance(path_str, str)
        assert Path(path_str).is_absolute
