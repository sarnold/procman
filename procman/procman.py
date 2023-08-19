"""
procman main init, run, and self-test functions.
"""

import os
import sys
import argparse
import importlib

from procman import utils
from procman import __version__


def init(dirs):
    """
    Check and create user and config dirs as needed. Also create the
    initial proxy/user config files if not present.
    :param: list of Path objs
    """
    for app_path in dirs:
        if not app_path.exists():
            app_path.mkdir(parents=True, exist_ok=True)

    utils.init_cfg_file()


def self_test():
    """
    Basic sanity check using small test file.
    """
    print("Python version:", sys.version)
    print("-" * 80)

    modname = 'procman.__init__'
    try:
        mod = importlib.import_module(modname)
        print(mod.__doc__)

    except Exception as exc:
        print("FAILED:", repr(exc))

    print("-" * 80)


def show_paths():
    """
    Display host platform user paths, config files
    """
    print("Python version:", sys.version)
    print("-" * 80)

    modname = 'procman.utils'
    try:
        mod = importlib.import_module(modname)
        print(mod.__doc__)

        print("User app dirs:")
        print(mod.get_userdirs())
        print("\nUser cfg files:")
        print(mod.get_userfiles())
        print("\nUser scripts:")
        print(mod.get_userscripts())

    except Exception as exc:
        print("FAILED:", repr(exc))

    print("-" * 80)


def main():
    """
    Collect and process command options/arguments and init app dirs
    if needed.
    """
    dirs = utils.get_userdirs()
    init(dirs)
    cfg = utils.load_cfg_file()
    uscripts = utils.get_userscripts()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--test', help='Run sanity checks',
                        action='store_true')
    parser.add_argument('-v', '--version', help='Display version info',
                        action='store_true')
    parser.add_argument('-s', '--show', help='Display user data paths',
                        action='store_true')
    parser.add_argument('-V', '--verbose', help='Switch from quiet to verbose',
                        action='store_true')

    options = parser.parse_args()

    if options.version:
        print('[procman {}]'.format(__version__))
        sys.exit(0)
    if options.show:
        show_paths()
        sys.exit(0)
    if options.test:
        self_test()
        sys.exit(0)

    try:
        print("This is a stub: %s %s", uscripts, options.verbose)

    except (KeyboardInterrupt, RuntimeError):
        pass
    except Exception as exc:
        print('[ERROR] {}'.format(exc))
