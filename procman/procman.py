"""
procman main init, run, and self-test functions.
"""

import argparse
import importlib
import sys
from threading import Timer

from honcho.manager import Manager

from . import utils
from ._version import __version__


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
        assert cfg_file.exists()

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
        print(mod.get_userdirs())
        print("\nUser cfg files:")
        print(mod.get_userfiles())
        print("\nUser scripts:")
        print(mod.get_userscripts())

    except (NameError, KeyError, ModuleNotFoundError) as exc:
        print(f"FAILED: {repr(exc)}")

    print("-" * 80)


def main(argv=None):
    """
    Collect and process command options/arguments and init app dirs
    if needed, launch the process manager.
    """
    if argv is None:
        argv = sys.argv

    dirs = utils.get_userdirs()
    init(dirs)
    ucfg, ufile = utils.load_cfg_file()
    uscripts = utils.get_userscripts()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Process manager for user scripts',
    )
    parser.add_argument(
        '-d',
        '--dump-config',
        help="dump active yaml configuration to stdout",
        action='store_true',
        dest="dump",
    )
    parser.add_argument(
        "--countdown",
        type=int,
        default='0',
        dest="runfor",
        help="Runtime STOP timer in seconds - 0 means run until whenever",
    )
    parser.add_argument('-t', '--test', help='Run sanity checks', action='store_true')
    parser.add_argument('--version', action="version", version=f"procman {__version__}")
    parser.add_argument(
        '-s', '--show', help='Display user data paths', action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose', help='Switch from quiet to verbose', action='store_true'
    )

    args = parser.parse_args()

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
    main()
