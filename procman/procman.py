"""
procman main init, run, and self-test functions.
"""

import argparse
import importlib
import logging
import sys
import warnings
from threading import Timer

from honcho.manager import Manager

from . import utils

# from logging_tree import printout  # debug logger environment


def init(dirs):
    """
    Check and create user and config dirs as needed. Also create the
    initial demo/example config file if not present.
    :param: list of Path objs
    """
    for app_path in dirs:
        if not app_path.exists():
            app_path.mkdir(parents=True, exist_ok=True)

    utils.init_cfg_file()


def self_test():
    """
    Basic sanity check using ``import_module``.
    """
    print("Python version:", sys.version)
    print("-" * 80)

    modlist = ['procman.__init__', 'procman.utils']
    for modname in modlist:
        try:
            print(f'Checking module {modname}')
            mod = importlib.import_module(modname)
            print(mod.__doc__)

        except (NameError, KeyError, ModuleNotFoundError) as exc:
            print(f"FAILED: {repr(exc)}")

    for cfg_file in mod.get_userfiles():
        if not cfg_file.exists():
            warnings.warn("Cannot verify user file %s", cfg_file, stacklevel=2)

    print("-" * 80)


def show_paths():
    """
    Display host platform user paths, config file, and configured scripts.
    """
    print("Python version:", sys.version)
    print("-" * 80)

    modname = 'procman.utils'
    try:
        mod = importlib.import_module(modname)
        print(mod.__doc__)

        print("User app dirs:")
        for item in mod.get_userdirs():
            print(f'  {item}')
        print("\nUser cfg files:")
        for item in mod.get_userfiles():
            print(f'  {item}')
        print("\nUser scripts:")
        for item in mod.get_userscripts():
            print(f'  {item}')

    except (NameError, KeyError, ModuleNotFoundError) as exc:
        print(f"FAILED: {repr(exc)}")

    print("-" * 80)


def main(argv=None):  # pragma: no cover
    """
    Collect and process command options/arguments and init app dirs,
    then launch the process manager.
    """
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Process manager for user scripts',
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display more processing info",
    )
    parser.add_argument(
        '-d',
        '--dump-config',
        help="dump active yaml configuration to stdout",
        action='store_true',
        dest="dump",
    )
    parser.add_argument(
        '-c',
        "--countdown",
        type=int,
        default='0',
        dest="runfor",
        help="Runtime STOP timer in seconds - 0 means run until whenever",
    )
    parser.add_argument('-t', '--test', help='Run sanity checks', action='store_true')
    parser.add_argument(
        '--version', action="version", version=f"%(prog)s {utils.VERSION}"
    )
    parser.add_argument(
        '-s', '--show', help='Display user data paths', action='store_true'
    )

    args = parser.parse_args()

    # basic logging setup must come before any other logging calls
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=log_level)
    # printout()  # logging_tree

    dirs = utils.get_userdirs()
    init(dirs)
    ucfg, ufile = utils.load_cfg_file()
    uscripts = utils.get_userscripts()

    if args.show:
        show_paths()
        sys.exit(0)
    if args.dump:
        sys.stdout.write(ufile.read_text(encoding=ucfg.file_encoding))
        sys.exit(0)
    if args.test:
        self_test()
        sys.exit(0)

    mgr = Manager()
    for user_proc in uscripts:
        print(f'Adding {user_proc} to manager...')
        mgr.add_process(user_proc[0], user_proc[1])

    stopme = Timer(args.runfor, mgr.terminate)
    if args.runfor:
        print(f'Running for {args.runfor} seconds only...')
        stopme.start()

    try:
        mgr.loop()
    except (KeyboardInterrupt, RuntimeError):
        print("\nExiting ...")
    finally:
        sys.exit(mgr.returncode)


if __name__ == "__main__":
    main()  # pragma: no cover
