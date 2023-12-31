Changelog
=========


0.2.0 (2023-09-25)
------------------

New
~~~
- Add a changelog, update docs build, readme and pkg cleanup. [Stephen L
  Arnold]

Changes
~~~~~~~
- Refactor docs, cleanup imports, sync up extension bits. [Stephen L
  Arnold]

  * document the full config block, cleanup serv example
- More readme and logging cleanup, print help if no cfg file. [Stephen L
  Arnold]
- Add simple tests, start refactoring readme. [Stephen L Arnold]

  * yank old cfg handling, make it simpler

Other
~~~~~
- Merge pull request #3 from sarnold/import-ref. [Steve Arnold]

  Import refactor, docs cleanup


0.1.1 (2023-08-25)
------------------

New
~~~
- Add runtime countdown-to-terminate argument, use 5 sec in tox.
  [Stephen L Arnold]

  * tox dev mode will start the demo stack for 5 seconds then terminate

Changes
~~~~~~~
- Cleanup rst formatting. [Stephen L Arnold]
- Add new tox command to run active config, update readme. [Stephen L
  Arnold]
- Replace assert with UserWarning in self-check. [Stephen L Arnold]
- Show some output in the readme, cleanup self-checks. [Stephen L
  Arnold]

Fix
~~~
- Cleanup formatting, docs and docstrings, remove static default_tag.
  [Stephen L Arnold]

Other
~~~~~
- Merge pull request #2 from sarnold/nit-cleanup. [Steve Arnold]

  Doc and nit cleanup


0.1.0 (2023-08-21)
------------------

New
~~~
- Add basic sphinx docs build and some GH workflows. [Stephen L Arnold]

  * more cleanup in readne/tox/setup files

Changes
~~~~~~~
- Ci: get more verbose with bandit workflow permissions. [Stephen L
  Arnold]

Fix
~~~
- Add missing pylint score. [Stephen L Arnold]
- Use correct license in badge text. [Stephen L Arnold]
- Allow proc_runner to be null if no interpreter. [Stephen L Arnold]

  * cleanup example app, docstrings, and tox file
- Add missing license file. [Stephen L Arnold]

Other
~~~~~
- Merge pull request #1 from sarnold/early-chores. [Steve Arnold]

  add docs and workflows
- Fix silly typo in badge string. [Stephen L Arnold]
- Cleanup initial cruft, flesh out base cfgs and user scripts. [Stephen
  L Arnold]
- Initial commit, new app shell with some yaml foo and an example.
  [Stephen L Arnold]
