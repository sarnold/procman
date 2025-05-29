"""
procman utils for file handling and config parsing.
"""

import logging
import os
import sys
from pathlib import Path
from typing import List, Tuple

from munch import Munch

if sys.version_info < (3, 10):
    import importlib_resources  # type: ignore[import-not-found]
else:
    import importlib.resources as importlib_resources


class FileTypeError(Exception):
    """Raise when the file extension is not '.yml' or '.yaml'"""

    __module__ = Exception.__module__


def load_config(
    file_encoding: str = 'utf-8', file_extension: str = '.yaml'
) -> Tuple[Munch, Path]:
    """
    Load yaml configuration file and munchify the data. If ENV path or local
    file is not found in current directory, the default cfg will be loaded.

    :param file_encoding: file encoding of config file
    :type file_encoding: str
    :param file_extension: file extension with leading separator
    :type file_extension: str
    :return: Munch and Path objects
    :raises FileTypeError: if the input file is not yml
    """
    proc_cfg = os.getenv('PROCMAN_CFG', default='')
    defconfig_file = f'.procman{file_extension}'

    cfgfile = Path(proc_cfg) if proc_cfg else Path(defconfig_file)
    if not cfgfile.name.lower().endswith(('.yml', '.yaml')):
        msg = 'invalid YAML extension: %s' % cfgfile.name
        raise (FileTypeError(msg))
    if not cfgfile.exists():
        cfgobj = load_base_config()
    else:
        cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))
    logging.debug('Using config: %s', str(cfgfile.resolve()))

    return cfgobj, cfgfile.resolve()


def get_userscripts(
    demo_mode: bool = False, file_encoding: str = 'utf-8', file_extension: str = '.yaml'
) -> List[str]:
    """
    Get user scripts from Munchified user cfg.

    :return: list of scripts
    """
    uscripts: List = []
    usr_cfg, usr_file = load_config(file_encoding, file_extension)
    ucfg = load_base_config() if not usr_file.exists() or demo_mode else usr_cfg
    for item in [x for x in ucfg.scripts if x.proc_enable]:
        proc_list = [item.proc_label]
        if demo_mode:
            if getattr(sys, 'frozen', False):
                scripts_path = os.path.join(os.path.dirname(sys.executable), 'procman')
            else:
                pkg_path = importlib_resources.files('procman')
                with importlib_resources.as_file(pkg_path) as path:
                    scripts_path = str(path)
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


def load_base_config() -> Munch:
    """
    Load initial procman config with our baseline example values. This is
    used to both run the example flask app and provide a user-facing example
    configuration.

    :return: Munch config obj
    """

    proc_cfg = Munch.fromYAML(
        """
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
