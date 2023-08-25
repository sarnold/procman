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
Honcho (and Foreman_, and Heroku_) parse a Procfile_ to run an application
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
Procman uses the XDG standard for user paths, which you can view below after
running ``procman --show``.  Run ``procman --dump-config`` to view the default
YAML configuration.

In your own project directory, use one of the ``pip install`` commands shown
below to install Procman in your own environment.  Copy the default config file
from the above path to your project directory and set ``demo_mode`` to false.
Make sure your custom config file starts with ``.procman`` and ends with a valid
YAML extension, ie, either ``.yml`` or ``.yaml``.

* Valid - ``.procman.yaml`` or ``.procman_myproject.yml`` or ``.procman_pelican.yaml``
* Invalid - ``.procman.yl`` or ``.proc_foobar.yaml`` or ``.proc_man.yml``

Using your preferred editor, edit/add process blocks to ``scripts`` as shown in the
example configuration (each "block" is a list element).

Note there should only be one Procman configuration file in a given project
source tree.  Additional config file requirements include:

* *demo_mode* must be false or removed
* *default_yml_ext* must be ``.yml`` or ``.yaml``
* *scripts_path* should be ``null`` for relative paths *inside your project tree*
* at least one process block with ``proc_enable: true`` should be present
  (under *scripts*)
* *proc_runner* should be the name of the interpreter, eg, ``python`` or ``ruby``
  (can be ``null`` if calling an executable directly)

.. note:: This project uses versioningit_ to generate and maintain the
          version file, which only gets included in the sdist/wheel
          packages. In a fresh clone, running any of the tox_ commands
          should generate the current version file.

.. _versioningit: https://github.com/jwodder/versioningit


Install with pip
----------------

This package is *not* yet published on PyPI, thus use one of the following
to install procman on any platform. Install from the main branch::

  $ https://github.com/sarnold/procman/archive/refs/heads/master.tar.gz

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
  serv: install_deps> python -I -m pip install 'pip>=21.1' versioningit '.[examples]'
  serv: commands[0]> procman --countdown 10
  Adding ['web', 'python /home/user/src/procman/procman/examples/app.py'] to manager...
  Adding ['redis', 'bash /home/user/src/procman/procman/examples/run_redis.sh run'] to manager...
  Running for 5 seconds only...
  11:32:56 system | redis started (pid=15576)
  11:32:56 system | web started (pid=15575)
  11:32:56 redis  | Using socket runtime dir: /tmp/redis-ipc
  11:32:56 redis  | 15581:C 25 Aug 2023 11:32:56.921 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
  11:32:56 redis  | 15581:C 25 Aug 2023 11:32:56.921 # Redis version=7.0.11, bits=64, commit=00000000, modified=0, pid=15581, just started
  11:32:56 redis  | 15581:C 25 Aug 2023 11:32:56.921 # Configuration loaded
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.921 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.921 # Server can't set maximum open files to 10032 because of OS error: Operation not permitted.
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.921 # Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.921 * monotonic clock: POSIX clock_gettime
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.922 * Running mode=standalone, port=0.
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.922 # Server initialized
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.922 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
  11:32:56 redis  | 15581:M 25 Aug 2023 11:32:56.923 * The server is now ready to accept connections at /tmp/redis-ipc/socket
  11:32:57 web    |  * Serving Flask app 'app'
  11:32:57 web    |  * Debug mode: on
  11:32:57 web    | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  11:32:57 web    |  * Running on http://localhost:8000
  11:32:57 web    | Press CTRL+C to quit
  11:32:57 web    |  * Restarting with stat
  11:32:57 web    |  * Debugger is active!
  11:32:57 web    |  * Debugger PIN: 650-499-885
  11:33:01 system | sending SIGTERM to web (pid 15575)
  11:33:01 system | sending SIGTERM to redis (pid 15576)
  11:33:01 redis  | 15581:signal-handler (1692988381) Received SIGTERM scheduling shutdown...
  11:33:01 redis  | 15581:M 25 Aug 2023 11:33:01.946 # User requested shutdown...
  11:33:01 redis  | 15581:M 25 Aug 2023 11:33:01.946 * Saving the final RDB snapshot before exiting.
  11:33:01 system | web stopped (rc=0)
  11:33:01 redis  | 15581:M 25 Aug 2023 11:33:01.950 * DB saved on disk
  11:33:01 redis  | 15581:M 25 Aug 2023 11:33:01.950 * Removing the pid file.
  11:33:01 redis  | 15581:M 25 Aug 2023 11:33:01.950 * Removing the unix socket file.
  11:33:01 redis  | 15581:M 25 Aug 2023 11:33:01.950 # Redis is now ready to exit, bye bye...
  11:33:01 system | redis stopped (rc=-15)
    dev: OK (14.87=setup[9.32]+cmd[0.12,0.14,5.29] seconds)
    congratulations :) (14.92 seconds)


.. note:: After installing in dev mode, use the environment created by
          Tox just like any other Python virtual environment.  The dev
          install mode of Pip allows you to edit the code and run it
          again while inside the virtual environment. By default Tox
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


Pre-commit
----------

This repository is pre-commit_ enabled for python/rst source and file-type
linting. The checks run automatically on commit and will fail the commit
(if not clean) and perform simple file corrections.  For example, if the
mypy check fails on commit, you must first fix any fatal errors for the
commit to succeed. That said, pre-commit does nothing if you don't install
it first (both the program itself and the hooks in your local repository
copy).

You will need to install pre-commit before contributing any changes;
installing it using your system's package manager is recommended,
otherwise install with pip into your local user environment using
something like::

  $ sudo emerge pre-commit  --or--
  $ sudo apt install pre-commit  --or--
  $ pip install pre-commit

then install the hooks into the repo you just cloned::

  $ git clone https://github.com/sarnold/procman
  $ cd procman/
  $ pre-commit install

It's usually a good idea to update the hooks to the latest version::

    $ pre-commit autoupdate

Most (but not all) of the pre-commit checks will make corrections for you,
however, some will only report errors, so these you will need to correct
manually.

Automatic-fix checks include black, isort, autoflake, and miscellaneous
file fixers. If any of these fail, you can review the changes with
``git diff`` and just add them to your commit and continue.

If any of the mypy, bandit, or rst source checks fail, you will get a report,
and you must fix any errors before you can continue adding/committing.

To see a "replay" of any ``rst`` check errors, run::

  $ pre-commit run rst-backticks -a
  $ pre-commit run rst-directive-colons -a
  $ pre-commit run rst-inline-touching-normal -a

To run all ``pre-commit`` checks manually, try::

  $ pre-commit run -a

.. _pre-commit: https://pre-commit.com/index.html


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
