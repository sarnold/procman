=========
 Procman
=========

**A Process manager for user scripts**.

|ci| |wheels| |release| |badge| |bandit|

|pre| |pylint|

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

The (hopefully) 2-minute version...

Usage
-----

Clone this repository, then follow the virtual environment install steps below.
Procman uses ``pathlib`` to find user paths, which you can view below after
running ``procman --show``.  Run ``procman --dump-config`` to view the active
YAML configuration.

In your own project directory, use one of the ``pip install`` commands shown
below to install Procman in a virtual environment.

Make sure the name of your custom config file starts with ``.procman`` and ends
with a valid YAML extension, ie, either ``.yml`` or ``.yaml``.

* Valid - ``.procman.yaml`` or ``.procman_myproject.yml`` or ``.procman_pelican.yaml``
* Invalid - ``.procman.yl`` or ``.proc_foobar.yaml`` or ``.proc_man.yml``

Using your preferred editor, edit/add process blocks to ``scripts`` as shown in the
example configuration (each "block" is a list element).

Note there can be only one default configuration in a given project tree named
``.procman.yaml``, however, you can override the default name via the environment
variable PROCMAN_CFG= path/to/.procman_othername.yaml. Additional config file
guidance includes:

* *default_yml_ext* must be ``.yml`` or ``.yaml``
* *scripts_path* should be ``null`` for relative paths *inside your project tree*
* at least one process block with ``proc_enable: true`` should be present
  (under *scripts*)
* *proc_runner* should be the name of the interpreter, eg, ``python`` or ``ruby``
  (can be ``null`` if calling an executable directly)


Install with pip
----------------

This package is *not* yet published on PyPI, thus use one of the following
to install procman on any platform. Install from the main branch::

  $ pip install https://github.com/sarnold/procman/archive/refs/heads/master.tar.gz

or use this command to install a specific release version::

  $ pip install https://github.com/sarnold/procman/releases/download/0.1.0/procman-0.1.0.tar.gz

The full package provides the ``procman`` executable as well as a working
demo with a reference configuration file with defaults for all values.

.. note:: To run the demo/example application, you need to first install
          ``redis`` via your system package manager.

If you'd rather work from the source repository, it supports the common
idiom to install it on your system in a virtual env after cloning::

  $ python -m venv env
  $ source env/bin/activate
  (env) $ pip install .[examples]
  (env) $ procman -h
  usage: procman [-h] [-d] [--countdown RUNFOR] [-t] [--version] [-s] [-v]

  Process manager for user scripts

  options:
    -h, --help          show this help message and exit
    -d, --dump-config   dump active yaml configuration to stdout
    --countdown RUNFOR  Runtime STOP timer in seconds - 0 means run until whenever
    -t, --test          Run sanity checks
    --version           show program's version number and exit
    -s, --show          Display user data paths
    -v, --verbose       Switch from quiet to verbose
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

To actually run the active configuration file with tox, use something like::

  $ tox -e serv -- 10

Running the above command will install the package and then run the active
config, (by default the flask/redis demo) in the tox serv environment for 10
seconds::

  $ tox -e serv -- 10
  serv: commands[0]> procman --demo --countdown 10
  Adding ['web', 'python /home/user/src/procman/.tox/serv/lib/python3.11/site-packages/procman/examples/app.py'] to manager...
  Adding ['redis', 'bash /home/user/src/procman/.tox/serv/lib/python3.11/site-packages/procman/examples/run_redis.sh run'] to manager...
  Running for 10 seconds only...
  21:04:54 system | web started (pid=26678)
  21:04:54 system | redis started (pid=26680)
  21:04:54 redis  | Using socket runtime dir: /tmp/redis-ipc
  21:04:54 redis  | 26684:C 07 Sep 2023 21:04:54.046 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
  21:04:54 redis  | 26684:C 07 Sep 2023 21:04:54.046 # Redis version=7.0.11, bits=64, commit=00000000, modified=0, pid=26684, just started
  21:04:54 redis  | 26684:C 07 Sep 2023 21:04:54.046 # Configuration loaded
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.046 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.046 # Server can't set maximum open files to 10032 because of OS error: Operation not permitted.
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.046 # Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.046 * monotonic clock: POSIX clock_gettime
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.047 * Running mode=standalone, port=0.
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.047 # Server initialized
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.047 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.048 * Loading RDB produced by version 7.0.11
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.048 * RDB age 595 seconds
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.048 * RDB memory usage when created 0.59 Mb
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.048 * Done loading RDB, keys loaded: 0, keys expired: 0.
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.048 * DB loaded from disk: 0.000 seconds
  21:04:54 redis  | 26684:M 07 Sep 2023 21:04:54.048 * The server is now ready to accept connections at /tmp/redis-ipc/socket
  21:04:54 web    |  * Serving Flask app 'app'
  21:04:54 web    |  * Debug mode: on
  21:04:54 web    | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  21:04:54 web    |  * Running on http://localhost:8000
  21:04:54 web    | Press CTRL+C to quit
  21:04:54 web    |  * Restarting with stat
  21:04:54 web    |  * Debugger is active!
  21:04:54 web    |  * Debugger PIN: 112-588-591
  21:05:04 system | sending SIGTERM to web (pid 26678)
  21:05:04 system | sending SIGTERM to redis (pid 26680)
  21:05:04 redis  | 26684:signal-handler (1694145904) Received SIGTERM scheduling shutdown...
  21:05:04 system | web stopped (rc=0)
  21:05:04 redis  | 26684:M 07 Sep 2023 21:05:04.089 # User requested shutdown...
  21:05:04 redis  | 26684:M 07 Sep 2023 21:05:04.089 * Saving the final RDB snapshot before exiting.
  21:05:04 redis  | 26684:M 07 Sep 2023 21:05:04.093 * DB saved on disk
  21:05:04 redis  | 26684:M 07 Sep 2023 21:05:04.093 * Removing the pid file.
  21:05:04 redis  | 26684:M 07 Sep 2023 21:05:04.093 * Removing the unix socket file.
  21:05:04 redis  | 26684:M 07 Sep 2023 21:05:04.093 # Redis is now ready to exit, bye bye...
  21:05:04 system | redis stopped (rc=-15)
    serv: OK (10.46=setup[0.05]+cmd[10.41] seconds)
    congratulations :) (10.51 seconds)

.. note:: After running the serv command, use the environment created by
          Tox just like any other Python virtual environment. As shown,
          the dev install mode of Pip allows you to edit the code and run
          it again while inside the virtual environment. By default Tox
          environments are created under ``.tox/`` and named after the
          env argument (eg, py).

Full list of additional ``tox`` commands:

* ``tox -e dev`` pip "developer" install
* ``tox -e serv`` will run the active configuration then stop (default: 5 sec)
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

  $ pip install -U https://github.com/sarnold/procman/releases/download/0.1.0/procman-0.1.0-py3-none-any.whl


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

  $ git clone https://github.com/sarnold/ymltoxml
  $ cd ymltoxml/
  $ pre-commit install

It's usually a good idea to update the hooks to the latest version::

    pre-commit autoupdate

.. _gitchangelog: https://github.com/sarnold/gitchangelog-action
.. _pre-commit: http://pre-commit.com/


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

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/procman/badges/master/pylint-score.svg
    :target: https://github.com/sarnold/procman/actions/workflows/pylint.yml
    :alt: Pylint Score

.. |license| image:: https://img.shields.io/badge/license-LGPL_2.1-blue
    :target: https://github.com/sarnold/procman/blob/master/LICENSE
    :alt: License

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/procman?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/procman/releases
    :alt: GitHub tag

.. |python| image:: https://img.shields.io/badge/python-3.6+-blue.svg
    :target: https://www.python.org/downloads/
    :alt: Python

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
