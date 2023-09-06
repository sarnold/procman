"""
procman utils for file handling and config parsing.
"""
import os
import sys
from pathlib import Path

from appdirs import AppDirs
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


def get_userdirs():
    """
    Set platform-agnostic user directory paths via appdirs, plus return
    working directory.

    :return: list of Path objs
    """
    dirs = AppDirs(appname='procman', version=VERSION)
    logdir = Path(dirs.user_log_dir)
    cachedir = Path(dirs.user_cache_dir)
    configdir = Path(dirs.user_config_dir)
    return [configdir, cachedir, logdir]


def get_userfiles(projfiles=True):
    """
    Get user-managed config file paths from both appdirs and working
    directory.  Note *we stop* after finding the first matching user
    filename.

    :return: list of Path objs
    """
    cfg_paths = []
    dirs = get_userdirs()
    p_cfg = dirs[0].joinpath('procman.yaml')
    cfg_paths.append(p_cfg)
    l_cfg = Path('.').glob('**/.procman*.y*ml')
    if projfiles:
        try:
            u_cfg = next(l_cfg)
        except StopIteration:
            return cfg_paths
        cfg_paths.append(u_cfg)
    return cfg_paths


def get_userscripts():
    """
    Get user scripts from Munchified user cfg.

    :return: list of scripts
    """
    uscripts = []
    ucfg, _ = load_cfg_file()
    for item in [x for x in ucfg.scripts if x.proc_enable]:
        proc_list = [item.proc_label]
        if hasattr(ucfg, 'demo_mode') and ucfg.demo_mode is not None:
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
        for opt in item.proc_opts:
            proc_str = proc_str + f' {opt}'
        proc_list.append(proc_str)
        uscripts.append(proc_list)
    return uscripts


def init_cfg_file():
    """
    Create initial procman/example configuration file.
    """
    files = get_userfiles(projfiles=False)
    pcfg = load_base_config()
    if not files[0].exists():
        files[0].write_text(Munch.toYAML(pcfg), encoding=pcfg.file_encoding)


def load_cfg_file():
    """
    Load user/procman configuration file and munchify the data.

    :return: Munch cfg obj
    """
    files = get_userfiles()
    uidx = 1 if len(files) > 1 else 0
    ufile = files[uidx]
    encoding = 'utf-8' if b'utf-8' in ufile.read_bytes() else None
    ucfg = Munch.fromYAML(ufile.read_text(encoding=encoding))
    return ucfg, ufile


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
        demo_mode: true
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


# usage
if __name__ == '__main__':
    print("User dirs:")
    print(get_userdirs())
    print("\nUser files:")
    print(get_userfiles())
    print("\nUser scripts:")
    print(get_userscripts())
