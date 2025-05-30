"""
procman main init, run, and self-test functions.
"""

import argparse
import importlib
import logging
import sys
import warnings
from pathlib import Path
from threading import Timer

from honcho.manager import Manager
from munch import Munch

from . import __version__ as VERSION
from .utils import get_userscripts, load_config

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

    _, cfg_file = load_config()
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

        print("User cfg file:")
        ucfg, cfg = mod.load_config()
        cfgfile = cfg.resolve() if cfg.exists() else None
        print(f'  {cfgfile}')
        print("User scripts:")
        for item in mod.get_userscripts(ucfg, cfg):
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
    parser.add_argument('--version', action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument('-D', '--demo', help='run demo config', action='store_true')
    parser.add_argument('-S', '--show', help='display user config', action='store_true')
    parser.add_argument('-t', '--test', help='run sanity checks', action='store_true')
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="display more processing info",
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
        help="runtime STOP timer in seconds - 0 means run forever",
    )
    parser.add_argument(
        'file',
        nargs='?',
        metavar="FILE",
        type=str,
        help="path to user-defined yaml configuration",
    )

    args = parser.parse_args()

    # basic logging setup must come before any other logging calls
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=log_level)
    # printout()  # logging_tree

    if args.show:
        show_paths()
        sys.exit(0)
    if args.test:
        self_test()
        sys.exit(0)
    infile = args.file
    if infile and not Path(infile).exists():
        print(f'Input file {infile} not found!')
        sys.exit(1)
    if infile:
        ufile = Path(infile)
        ucfg, _ = load_config(ufile=infile)
    else:
        ucfg, ufile = load_config()
    uscripts = get_userscripts(ucfg, ufile, demo_mode=args.demo)

    if args.dump:
        sys.stdout.write(Munch.toYAML(ucfg))
        sys.exit(0)
    if len(argv) == 1 and not ufile.exists():
        parser.print_help()
        print('\nNo cfg file found; use the --demo arg or create a cfg file')
        sys.exit(1)

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
