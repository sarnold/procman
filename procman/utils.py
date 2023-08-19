"""
procman utils for config parsing.
"""
import os
import sys
import time

from pathlib import Path

from munch import Munch
from appdirs import AppDirs

if sys.version_info < (3, 10):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

from ._version import __version__


def get_userdirs():
    """
    Set platform-agnostic user directory paths via appdirs.
    :return: list of Path objs
    """
    dirs = AppDirs(appname='procman', version=__version__)
    logdir = Path(dirs.user_log_dir)
    cachedir = Path(dirs.user_cache_dir)
    configdir = Path(dirs.user_config_dir)
    return [cachedir, configdir, logdir]


def get_userfiles():
    """
    Get user-managed config file paths.
    :return: list of Path objs
    """
    dirs = get_userdirs()
    u_cfg = dirs[1].joinpath('procman.yaml')
    return [u_cfg]


def get_userscripts():
    """
    Get user scripts from Munchified user cfg.
    :return: list of scripts
    """
    uscripts = []
    ucfg = load_cfg_files()[0]
    for item in [x for x in ucfg.scripts if x.script_enable]:
        if getattr(sys, 'frozen', False):
            pkg = os.path.join(os.path.dirname(sys.executable), 'procman')
        else:
            pkg = importlib_resources.files('procman')
        script = os.path.join(pkg, item.script_dir, item.script_name)
        uscripts.extend(['--scripts', script])
        for opt in item.script_opts:
            uscripts.extend(['--set', opt])
    return uscripts


def init_cfg_files():
    """
    Create initial user/procman configuration files.
    """
    files = get_userfiles()
    ucfg, pcfg = load_base_configs()
    if not files[1].exists():
        files[1].write_text(Munch.toYAML(pcfg), encoding='utf-8')
    if not files[0].exists():
        files[0].write_text(Munch.toYAML(ucfg), encoding='utf-8')


def load_cfg_files():
    """
    Load user/procman configuration files and munchify the data.
    :return: list of Munch cfg objs
    """
    files = get_userfiles()
    ucfg = Munch.fromYAML(files[0].read_text(encoding='utf-8'))
    pcfg = Munch.fromYAML(files[1].read_text(encoding='utf-8'))
    return ucfg, pcfg


def load_base_configs():
    """
    Load initial procman config with our baseline values.
    :return: tuple of Munch config objs
    """

    proc_cfg = Munch.fromYAML("""
    scripts: []
    """)

    # note scripts are loaded from here (not proc_cfg)
    user_cfg = Munch.fromYAML("""
    scripts:
      - script_name: app.py
        script_dir: examples
        script_opts: []
        script_enable: true
        script_runner: python
      - script_name: run_redis.sh
        script_dir: examples
        script_opts:
          - 'run'
        script_enable: true
        script_runner: bash
    """)

    return user_cfg, proc_cfg


# usage
if __name__ == '__main__':

    print("User dirs:")
    print(get_userdirs())
    print("User files:")
    print(get_userfiles())
    print("User scripts:")
    print(get_userscripts())
