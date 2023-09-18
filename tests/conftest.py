from pathlib import Path

import pytest

from procman import utils


def pytest_configure(config):
    """Create app config data"""
    # can use `config` to use command line options
    utils.init_cfg_file()
