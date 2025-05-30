=========
 Procman
=========

**A lightweight process manager for user scripts**.

|ci| |wheels| |bandit| |release|

|pre| |cov| |pylint|

|tag| |license| |python|


But what is it, really?
=======================

Procman is a tool for running multiple external processes and multiplexing
their output to the console. It also cleans up and stops the whole stack
if any one of the running processes stops or dies on its own.

Procman is loosely based on Honcho_ and uses Honcho's process manager API.
Honcho (and Foreman_, and Heroku_) parses a Procfile_ to run an application
stack, usually with a specific ``.env`` file.  See the Introduction_ in the
Honcho documentation for an overview with an example ``Procfile``.

Procman provides an easy way to run such applications using a single YAML_
configuration file instead.  Procman includes a functional example config
with a small demo Flask_ app that uses redis_ to store a web counter (I
did say small/simple...).  The example app requires both redis-py_ (which
in turn requires redis) and flask.  Note installing Procman with the
``[examples]`` flag will install the python deps but you must install
redis using your own platform tools (eg, ``apt`` or ``brew``).

Procman is tested on the 3 primary GH runner platforms, so as long as you
have a new-ish Python and a sane shell environment it should Just Work.

Note Procman only supports Python 3.6+.


.. _Honcho: https://honcho.readthedocs.io/en/latest/index.html
.. _Heroku: https://heroku.com/
.. _Foreman: https://ddollar.github.io/foreman/
.. _Procfile: https://devcenter.heroku.com/articles/procfile
.. _Introduction: https://honcho.readthedocs.io/en/latest/index.html#what-are-procfiles
.. _YAML: https://en.wikipedia.org/wiki/YAML
.. _Flask: https://pypi.org/project/flask/
.. _redis: https://redis.io/docs/getting-started/
.. _redis-py: https://pypi.org/project/redis/


Quick Start
===========

Procman is mainly configuration-driven via YAML config files; the included
example can be displayed and copied via command-line options (see the Usage_
section below).  To create your own configuration, you need at least one
script to run and a place to put it (see `Configuration settings`_ for more
details).

The current version supports minimal command options and there are no
required arguments::

  (dev) user@host $ procman -h
  usage: procman [-h] [--version] [-D] [-S] [-t] [-v] [-d] [-c RUNFOR] [FILE]

  Process manager for user scripts

  positional arguments:
    FILE                  path to user-defined yaml configuration (default:
                          None)

  options:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -D, --demo            run demo config (default: False)
    -S, --show            display user config (default: False)
    -t, --test            run sanity checks (default: False)
    -v, --verbose         display more processing info (default: False)
    -d, --dump-config     dump active yaml configuration to stdout (default:
                          False)
    -c, --countdown RUNFOR
                          runtime STOP timer in seconds - 0 means run forever
                          (default: 0)

Configuration options
---------------------

There are several ways to apply your own configuration:

* use default filename pattern in project root, either ``.procman`` or
  ``procman`` with a YAML extension of ``.yml`` or ``.yaml``

* use any filename with YAML extension passed as positional argument, eg
  something like ``procman custom_config.yaml``

* set the ``PROCMAN_CFG`` environment variable to something like
  ``my/path/to/config.yaml``


Usage
-----

To get started, clone this repository, then follow the virtual
environment install steps below. Procman uses ``pathlib`` to find user
paths, which you can view below after running ``procman --show``.  Run
``procman --dump-config`` to view the active YAML configuration.

To create your own default config file in the working directory, the local
copy must be named ``.procman.yaml``.  To get a copy of the example
configuration file, do::

  $ cd path/to/work/dir/
  $ procman --dump-config > .procman.yaml
  $ $EDITOR .procman.yaml
  $ procman --dump-config  # you should see your config settings

If needed, you can also create additional ``procman`` config files to
override your default project configuration. These alternate config files
can have arbitrary names (ending in '.yml' or '.yaml') but we recommend
using something like ``procman-dev-myproject.yml`` or similar. Since only
one configuration can be "active", the non-default config file must be set
via the environment variable ``PROCMAN_CFG``, eg::

  $ procman --dump-config > procman-develop.yml
  $ $EDITOR procman-develop.yml  # set alternate scripts, other options
  $ PROCMAN_CFG="procman-develop.yml" procman --verbose

Configuration settings
----------------------

Using your preferred editor, edit/add process blocks to ``scripts`` as shown in the
example configuration (each "block" is a list element).

Note there can be only one default configuration in a given project tree
named ``.procman.yaml``, however, you can override the default name via the
environment variable PROCMAN_CFG=path/to/procman_othername.yaml. Additional
config file guidance includes:

:scripts_path: the path to the script containing directory, ie, ``proc_dir``,
               which can be relative, absolute, or ``null``, depending on
               where the script directory is
:scripts: at least one process block with ``proc_enable: true`` should be present
          (under *scripts*)
:proc_label: is the process label for the script (see log display below)
:proc_name: the actual (file)name of the script
:proc_dir: the directory name where the script lives
:proc_runner: the name of the script interpreter, eg, ``python`` or ``ruby``,
              or ``null`` if calling an executable directly
:proc_enable: enable/disable this process block
:proc_opts: any required script args (default is an empty list)

Install with pip
================

This package is *not* yet published on PyPI, thus use one of the following
to install procman on any platform. Install from the main branch::

  $ pip install https://github.com/sarnold/procman/archive/refs/heads/master.tar.gz

or use this command to install a specific release version::

  $ pip install https://github.com/sarnold/procman/releases/download/0.1.0/procman-0.1.0.tar.gz

The full package provides the ``procman`` executable as well as a working
demo with a reference configuration with defaults for all values.

.. note:: To run the example application, you need to first install
          ``redis`` via your system package manager.

If you'd rather work from the source repository, it supports the common
idiom to install it on your system in a virtual env after cloning::

  $ python -m venv env
  $ source env/bin/activate
  (env) $ pip install .[examples]
  (env) $ procman --version
  procman 0.1.1.dev16+g3b96476.d20230922
  (env) $ deactivate

The alternative to python venv is the Tox_ test driver.  If you have it
installed already, clone this repository and try the following commands
from the procman source directory.

To install the package with examples and run the checks::

  $ tox -e py

To run pylint::

  $ tox -e lint

To install in developer mode::

  $ tox -e dev

To actually run the active configuration file for 30 seconds, run::

  $ tox -e serv -- 30

Running the following command will install the package and then run the
(built-in) example config via the ``--demo`` option for 10 seconds using
the tox serv environment; note you can override the ``--demo`` option by
providing the timeout value as shown above::

  $ tox -e serv
  serv: install_deps> python -I -m pip install 'pip>=21.1' 'setuptools_scm[toml]' '.[examples]'
  serv: commands[0]> procman --countdown 10 --demo
  14:02:15 system | redis started (pid=15356)
  14:02:15 system | web started (pid=15355)
  14:02:15 redis  | Using socket runtime dir: /tmp/redis-ipc
  14:02:15 redis  | 15361:C 22 Sep 2023 14:02:15.793 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
  14:02:15 redis  | 15361:C 22 Sep 2023 14:02:15.793 # Redis version=7.0.11, bits=64, commit=00000000, modified=0, pid=15361, just started
  14:02:15 redis  | 15361:C 22 Sep 2023 14:02:15.793 # Configuration loaded
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.794 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.794 # Server can't set maximum open files to 10032 because of OS error: Operation not permitted.
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.794 # Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.794 * monotonic clock: POSIX clock_gettime
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.795 * Running mode=standalone, port=0.
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.795 # Server initialized
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.795 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
  14:02:15 redis  | 15361:M 22 Sep 2023 14:02:15.796 * The server is now ready to accept connections at /tmp/redis-ipc/socket
  14:02:15 web    |  * Serving Flask app 'app'
  14:02:15 web    |  * Debug mode: on
  14:02:15 web    | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  14:02:15 web    |  * Running on http://localhost:8000
  14:02:15 web    | Press CTRL+C to quit
  14:02:15 web    |  * Restarting with stat
  14:02:16 web    |  * Debugger is active!
  14:02:16 web    |  * Debugger PIN: 112-588-591
  14:02:25 system | sending SIGTERM to web (pid 15355)
  14:02:25 system | sending SIGTERM to redis (pid 15356)
  14:02:25 redis  | 15361:signal-handler (1695416545) Received SIGTERM scheduling shutdown...
  14:02:25 system | web stopped (rc=0)
  14:02:25 redis  | 15361:M 22 Sep 2023 14:02:25.853 # User requested shutdown...
  14:02:25 redis  | 15361:M 22 Sep 2023 14:02:25.853 * Saving the final RDB snapshot before exiting.
  14:02:25 redis  | 15361:M 22 Sep 2023 14:02:25.859 * DB saved on disk
  14:02:25 redis  | 15361:M 22 Sep 2023 14:02:25.859 * Removing the pid file.
  14:02:25 redis  | 15361:M 22 Sep 2023 14:02:25.859 * Removing the unix socket file.
  14:02:25 redis  | 15361:M 22 Sep 2023 14:02:25.859 # Redis is now ready to exit, bye bye...
  14:02:25 system | redis stopped (rc=-15)
    serv: OK (16.17=setup[5.88]+cmd[10.29] seconds)
    congratulations :) (16.22 seconds)

.. note:: After running the serv command, use the environment created by
          Tox just like any other Python virtual environment. As shown,
          the dev install mode of Pip allows you to edit the code and run
          it again while inside the virtual environment. By default Tox
          environments are created under ``.tox/`` and named after the
          env argument (eg, dev).

Full list of additional ``tox`` commands:

* ``tox -e dev`` pip "developer" install
* ``tox -e serv`` will run the active configuration then stop (default: 10 sec)
* ``tox -e style`` will run flake8 style checks
* ``tox -e lint`` will run pylint (somewhat less permissive than PEP8/flake8 checks)
* ``tox -e mypy`` will run mypy import and type checking
* ``tox -e isort`` will run isort import checks
* ``tox -e clean`` will remove all generated/temporary files

To build/lint the html docs, use the following tox commands:

* ``tox -e docs`` build the documentation using sphinx and the api-doc plugin
* ``tox -e docs-lint`` build the docs and run the sphinx link checking


To install the latest release, eg with your own ``tox.ini`` file in
another project, use something like this::

  $ pip install -U https://github.com/sarnold/procman/releases/download/0.1.0/procman-0.4.1-py3-none-any.whl


.. _Tox: https://github.com/tox-dev/tox

Making Changes & Contributing
=============================

We use the gitchangelog_ action to generate our changelog and GH Release
page, as well as the gitchangelog message format to help it categorize/filter
commits for a tidier changelog. Please use the appropriate ACTION modifiers
in any Pull Requests.

This repo is also pre-commit_ enabled for various linting and format
checks.  The checks run automatically on commit and will fail the
commit (if not clean) with some checks performing simple file corrections.

If other checks fail on commit, the failure display should explain the error
types and line numbers. Note you must fix any fatal errors for the
commit to succeed; some errors should be fixed automatically (use
``git status`` and ``git diff`` to review any changes).

See the following pages for more information on gitchangelog and pre-commit.

.. inclusion-marker-1

* generate-changelog_
* pre-commit-config_
* pre-commit-usage_

.. _generate-changelog:  docs/source/dev/generate-changelog.rst
.. _pre-commit-config: docs/source/dev/pre-commit-config.rst
.. _pre-commit-usage: docs/source/dev/pre-commit-usage.rst
.. inclusion-marker-2

You will need to install pre-commit before contributing any changes;
installing it using your system's package manager is recommended,
otherwise install with pip into your usual virtual environment using
something like::

  $ sudo emerge pre-commit  --or--
  $ pip install pre-commit

then install it into the repo you just cloned::

  $ git clone https://github.com/sarnold/procman
  $ cd procman/
  $ pre-commit install

It's usually a good idea to update the hooks to the latest version::

    pre-commit autoupdate


SBOM and license info
=====================

This project is now compliant the REUSE Specification Version 3.3, so the
corresponding license information for all files can be found in the ``REUSE.toml``
configuration file with license text(s) in the ``LICENSES/`` folder.

Related metadata can be (re)generated with the following tools and command
examples.

* reuse-tool_ - REUSE_ compliance linting and sdist (source files) SBOM generation
* sbom4python_ - generate SBOM with full dependency chain

Commands
--------

Use tox to create the environment and run the lint command::

  $ tox -e reuse                      # --or--
  $ tox -e reuse -- spdx > sbom.txt   # generate sdist files sbom

Note you can pass any of the other reuse commands after the ``--`` above.

Use the above environment to generate the full SBOM in text format::

  $ source .tox/reuse/bin/activate
  $ sbom4python --system --use-pip -o <file_name>.txt

Be patient; the last command above may take several minutes. See the
doc links above for more detailed information on the tools and
specifications.


.. _pre-commit: https://pre-commit.com/index.html
.. _gitchangelog: https://github.com/sarnold/gitchangelog-action
.. _reuse-tool: https://github.com/fsfe/reuse-tool
.. _REUSE: https://reuse.software/spec-3.3/
.. _sbom4python: https://github.com/anthonyharrison/sbom4python


.. |ci| image:: https://github.com/sarnold/procman/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/sarnold/procman/actions/workflows/ci.yml
    :alt: CI Status

.. |wheels| image:: https://github.com/sarnold/procman/actions/workflows/wheels.yml/badge.svg
    :target: https://github.com/sarnold/procman/actions/workflows/wheels.yml
    :alt: Wheel Status

.. |badge| image:: https://github.com/sarnold/procman/actions/workflows/pylint.yml/badge.svg
    :target: https://github.com/sarnold/procman/actions/workflows/pylint.yml
    :alt: Pylint Status

.. |release| image:: https://github.com/sarnold/procman/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/procman/actions/workflows/release.yml
    :alt: Release Status

.. |bandit| image:: https://github.com/sarnold/procman/actions/workflows/bandit.yml/badge.svg
    :target: https://github.com/sarnold/procman/actions/workflows/bandit.yml
    :alt: Security check - Bandit

.. |cov| image:: https://raw.githubusercontent.com/sarnold/procman/badges/master/test-coverage.svg
    :target: https://github.com/sarnold/procman/actions/workflows/coverage.yml
    :alt: Test coverage

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/procman/badges/master/pylint-score.svg
    :target: https://github.com/sarnold/procman/actions/workflows/pylint.yml
    :alt: Pylint Score

.. |license| image:: https://img.shields.io/badge/license-LGPL_2.1-blue
    :target: https://github.com/sarnold/procman/blob/master/COPYING
    :alt: License

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/procman?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/procman/releases
    :alt: GitHub tag

.. |python| image:: https://img.shields.io/badge/python-3.9+-blue.svg
    :target: https://www.python.org/downloads/
    :alt: Python

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
