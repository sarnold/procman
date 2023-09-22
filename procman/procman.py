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
from munch import Munch

from . import utils

# from logging_tree import printout  # debug logger environment


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
            logging.error("FAILED: %s", repr(exc))

    _, cfg_file = utils.load_config()
    if not cfg_file.exists():
        warnings.warn(f"Cannot verify user file {cfg_file}", RuntimeWarning, stacklevel=2)

    print("-" * 80)


def show_paths():
    """
    Display user config path and configured scripts.
    """
    print("Python version:", sys.version)
    print("-" * 80)

    modname = 'procman.utils'
    try:
        mod = importlib.import_module(modname)
        print(mod.__doc__)

        print("\nUser cfg file:")
        _, cfg = mod.load_config()
        print(f'  {cfg}')
        print("\nUser scripts:")
        for item in mod.get_userscripts():
            print(f'  {item}')

    except (NameError, KeyError, ModuleNotFoundError) as exc:
        logging.error("FAILED: %s", repr(exc))

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
    parser.add_argument('-D', '--demo', help='Run demo config', action='store_true')
    parser.add_argument('-t', '--test', help='Run sanity checks', action='store_true')
    parser.add_argument(
        '--version', action="version", version=f"%(prog)s {utils.VERSION}"
    )
    parser.add_argument(
        '-S', '--show', help='Display user data paths', action='store_true'
    )

    args = parser.parse_args()

    # basic logging setup must come before any other logging calls
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=log_level)
    # printout()  # logging_tree

    ucfg, ufile = utils.load_config()
    uscripts = utils.get_userscripts(demo_mode=args.demo)

    if len(argv) == 1 and not ufile.exists():
        parser.print_help()
        print('\nDid you create a config file yet?')
        sys.exit(1)
    if args.show:
        show_paths()
        sys.exit(0)
    if args.dump:
        sys.stdout.write(Munch.toYAML(ucfg))
        sys.exit(0)
    if args.test:
        self_test()
        sys.exit(0)

    mgr = Manager()
    for user_proc in uscripts:
        logging.debug('Adding %s to manager', user_proc)
        mgr.add_process(user_proc[0], user_proc[1])

    stopme = Timer(args.runfor, mgr.terminate)
    if args.runfor:
        logging.debug('Running for %d seconds then shutdown', args.runfor)
        stopme.start()

    try:
        mgr.loop()
    except (KeyboardInterrupt, RuntimeError):
        print("\nExiting ...")
    finally:
        sys.exit(mgr.returncode)


if __name__ == "__main__":
    main()  # pragma: no cover
