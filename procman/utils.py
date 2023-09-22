"""
procman utils for file handling and config parsing.
"""
import logging
import os
import sys
from pathlib import Path

from munch import Munch

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

if sys.version_info < (3, 10):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

VERSION = version('procman')


class FileTypeError(Exception):
    """Raise when the file extension is not '.yml' or '.yaml'"""

    __module__ = Exception.__module__


def load_config(file_encoding='utf-8'):
    """
    Load yaml configuration file and munchify the data. If ENV path or local
    file is not found in current directory, the default cfg will be loaded.

    :param file_encoding: file encoding of config file
    :type file_encoding: str
    :return tuple: Munch cfg obj
    :raises FileTypeError: if the input file is not yml
    """
    proc_cfg = os.getenv('PROCMAN_CFG', default='')
    defconfig = '.procman.yaml'

    cfgfile = Path(proc_cfg) if proc_cfg else Path(defconfig)
    if not cfgfile.name.lower().endswith(('.yml', '.yaml')):
        raise FileTypeError(f"FileTypeError: unknown file extension: {cfgfile.name}")
    if not cfgfile.exists():
        cfgobj = load_base_config()
    else:
        cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))
    logging.debug('Using config: %s', str(cfgfile.resolve()))

    return cfgobj, cfgfile


def get_userscripts(demo_mode=False):
    """
    Get user scripts from Munchified user cfg.

    :return: list of scripts
    """
    uscripts = []
    usr_cfg, usr_file = load_config()
    ucfg = load_base_config() if not usr_file.exists() or demo_mode else usr_cfg
    for item in [x for x in ucfg.scripts if x.proc_enable]:
        proc_list = [item.proc_label]
        if demo_mode:
            if getattr(sys, 'frozen', False):
                scripts_path = os.path.join(os.path.dirname(sys.executable), 'procman')
            else:
                scripts_path = importlib_resources.files('procman')
            proc_str = (
                f'{item.proc_runner} ' if item.proc_runner else ''
            ) + f'{os.path.join(scripts_path, item.proc_dir, item.proc_name)}'
        else:
            if ucfg.scripts_path:
                proc_str = (
                    (f'{item.proc_runner} ' if item.proc_runner else '')
                    + f'{os.path.join(ucfg.scripts_path, item.proc_dir, item.proc_name)}'
                )
            else:
                proc_str = (
                    f'{item.proc_runner} ' if item.proc_runner else ''
                ) + f'{os.path.join(item.proc_dir, item.proc_name)}'
        logging.debug('Demo mode is %s', demo_mode)
        for opt in item.proc_opts:
            proc_str = proc_str + f' {opt}'
        proc_list.append(proc_str)
        uscripts.append(proc_list)
    return uscripts


def load_base_config():
    """
    Load initial procman config with our baseline example values. This is
    used to both run the example flask app and provide a user-facing example
    configuration.

    :return: Munch config obj
    """

    proc_cfg = Munch.fromYAML(
        """
        file_encoding: 'utf-8'
        default_yml_ext: '.yaml'
        scripts_path: null
        scripts:
          - proc_name: 'app.py'
            proc_dir: examples
            proc_label: web
            proc_opts: []
            proc_enable: true
            proc_runner: python
          - proc_name: 'run_redis.sh'
            proc_dir: examples
            proc_label: redis
            proc_opts:
              - 'run'
            proc_enable: true
            proc_runner: bash
        """
    )

    return proc_cfg
