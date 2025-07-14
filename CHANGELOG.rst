Changelog
=========


0.5.3 (2025-07-13)
------------------

Changes
~~~~~~~
- Update readme and docs build, set min python version to 3.8. [Stephen
  L Arnold]
- Update deps, keep munch but swap pyyaml for ruamel.yaml. [Stephen L
  Arnold]

  * change example config from yaml string to dict, update munches
    to use Dict attributes instead of yaml
  * update tox and project files, bump pre-commit hooks

Fixes
~~~~~
- Address codeql warning in example app. [Stephen L Arnold]

Other
~~~~~
- Merge pull request #24 from sarnold/compat-yaml. [Steve Arnold]

  el9 compat yaml


0.5.2 (2025-06-18)
------------------

Fixes
~~~~~
- Cleanup typing and misc lint, ignore pytest warnings. [Stephen L
  Arnold]

  * cleanup tox commands, add an assert to make return type even
    more obvious

Other
~~~~~
- Merge pull request #22 from sarnold/lint-cleanup. [Steve Arnold]

  cleanup lint


0.5.1 (2025-05-31)
------------------

Changes
~~~~~~~
- Add py.typed marker and 2 type:ignore, remove mypy cfg. [Stephen L
  Arnold]

  * cleanup some docstrings and lint
- Cleanup config file documentation bits. [Stephen L Arnold]
- Cleanup old runner environments, fix some typos. [Stephen L Arnold]

Other
~~~~~
- Merge pull request #19 from sarnold/changelogs. [Steve Arnold]

  update changelog
- Merge pull request #18 from sarnold/ci-runners. [Steve Arnold]

  CI runner cleanup


0.5.0 (2025-05-30)
------------------

Changes
~~~~~~~
- Update changelog for new release, update pre-commit hooks. [Stephen L
  Arnold]
- Update readme and help strings, cleanup project files. [Stephen L
  Arnold]
- Refactor part 2, wire up config file as positional arg. [Stephen L
  Arnold]

  * add file arg to load_config, update test and entry point
- Refactor part 1, decouple util funcs, add user config arg. [Stephen L
  Arnold]

  * tests and entrypoint are updated, but config arg is not wired up yet
- Update docs config and deps. [Stephen L Arnold]

Fixes
~~~~~
- Cleanup old runners in coverage workflow, update project files.
  [Stephen L Arnold]
- Add type annotations and cleanup imports, add mypy config. [Stephen L
  Arnold]

Other
~~~~~
- Merge pull request #17 from sarnold/doc-updates. [Steve Arnold]

  pre-release cleanup
- Merge pull request #16 from sarnold/cleanup-bits. [Steve Arnold]

  more config


0.4.1 (2025-03-18)
------------------

Changes
~~~~~~~
- Update to latest bandit action for testing, fix readme. [Stephen L
  Arnold]

Other
~~~~~
- Merge pull request #12 from sarnold/doc-nits. [Steve Arnold]

  Action update


0.4.0 (2025-03-16)
------------------

Changes
~~~~~~~
- Apply recommended actions hardening, add PR approval. [Stephen L
  Arnold]

  * the latter auto-approve workflow is owner-only for CI checks
  * update .pre-commit-config.yaml
- Add explicit job permissions, bump runner version. [Stephen L Arnold]
- Add REUSE.toml config and become reuse spec 3.3 compliant. [Stephen L
  Arnold]

  * procman-sdist-sbom.txt was generated using ``reuse spdx`` cmd
  * COPYING is now a symlink pointing to LICENSES/LGPL-2.1-or-later.txt
  * add readme section on SBOM and licensing info
  * add reuse cmd and bump python versions in tox file
- Update all workflow actions and python versions. [Stephen L Arnold]

Fixes
~~~~~
- Make sure release workflow has the right job permissions. [Stephen L
  Arnold]
- Update gitchangelog and add config, fix readme URI. [Stephen L Arnold]
- Move description text and add version. [Stephen L Arnold]

Other
~~~~~
- Merge pull request #11 from sarnold/release-docs. [Steve Arnold]

  release workflow fixes
- Merge pull request #10 from sarnold/changelog-fix. [Steve Arnold]

  changelog fixes
- Merge pull request #9 from sarnold/action-hashes. [Steve Arnold]

  workflow linting
- Merge pull request #8 from sarnold/workflow-job-renames. [Steve
  Arnold]

  more workflow cleanup
- Merge pull request #6 from sarnold/metadata-cleanup. [Steve Arnold]

  metadata cleanup


0.3.0 (2024-01-12)
------------------

Changes
~~~~~~~
- Tighten up show output, use full path for cfg file. [Stephen L Arnold]

  * since the demo config is a string and not a file, the --show command
    will display a "fictitious" user file, and --test will warn about it

Fixes
~~~~~
- Use resolved paths for config and scripts. [Stephen L Arnold]

  * return resolved path obj from load_config, use it in get_userscripts
  * update tests for full script path in get_userscripts list

Other
~~~~~
- Merge pull request #5 from sarnold/full-cfg-path. [Steve Arnold]

  use resolved paths for config and scripts
- Merge pull request #4 from sarnold/more-nit-cleanup. [Steve Arnold]

  tighten up show output, use full path for cfg file


0.2.0 (2023-09-26)
------------------

New
~~~
- Add coverage workflow. [Stephen L Arnold]
- Add a changelog, update docs build, readme and pkg cleanup. [Stephen L
  Arnold]

Changes
~~~~~~~
- Refactor docs, cleanup imports, sync up extension bits. [Stephen L
  Arnold]

  * document the full config block, cleanup serv example
- Bump setuptools version for setuptools_scm, cleanup setup.py. [Stephen
  L Arnold]

  * according to other project bugs, eg, matplotlib, minimum should be 64
  * try 59 so we can keep python 3.6 for now
- More readme and logging cleanup, print help if no cfg file. [Stephen L
  Arnold]
- Add more connfig tests. [Stephen L Arnold]
- Cleanup imports and reqs, warnings, logging, and config handling.
  [Stephen L Arnold]

  * make demo-mode a command-line arg with default False
  * do NOT write the example config to a file automatically
  * use --dump-config and redirect to a file instead
- Refactor user cfg  handling, no more appdirs. [Stephen L Arnold]

  * support local/default project config file(s) with ENV override
  * if no defconfig is found, create one in working directory
- Add simple tests, start refactoring readme. [Stephen L Arnold]

  * still needs old cfg handling yanked, make it simpler
- Swap out version file, swap in setuptools-scm dynamic version.
  [Stephen L Arnold]

Other
~~~~~
- Fix silly branch typo in coverage workflow. [Stephen L Arnold]
- Update changelog for release, restore missing coverage in the readme.
  [Stephen L Arnold]
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

Fixes
~~~~~
- Add worrkaround for GH API bug, update readme. [Stephen L Arnold]

  * limit bandit workflow to push event only so comments get connected
    with the proper check run
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
- Add initial README doc and pre-commit config. [Stephen L Arnold]
- Initial process manager and example user script integration. [Stephen
  L Arnold]

  * uses default example flask-redis app

Changes
~~~~~~~
- Ci: get more verbose with bandit workflow permissions. [Stephen L
  Arnold]
- Restore pylint/bandit workflows, use explicit branch target. [Stephen
  L Arnold]
- Add explicit permissions block to bandit workflow. [Stephen L Arnold]
- Revert bandit workflow action branch to master, set path. [Stephen L
  Arnold]
- Switch bandit workflow to latest test branch. [Stephen L Arnold]

Fixes
~~~~~
- Restore missing release artifact name. [Stephen L Arnold]
- Add missing pylint score. [Stephen L Arnold]
- Use correct license in badge text. [Stephen L Arnold]
- Allow proc_runner to be null if no interpreter. [Stephen L Arnold]

  * cleanup example app, docstrings, and tox file
- Add missing license file. [Stephen L Arnold]
- Cleanup even more lint with pre-commit. [Stephen L Arnold]
- Cleanup some lint. [Stephen L Arnold]

Other
~~~~~
- Merge pull request #1 from sarnold/early-chores. [Steve Arnold]

  add docs and workflows
- Fix silly typo in badge string. [Stephen L Arnold]
- Cleanup initial cruft, flesh out base cfgs and user scripts. [Stephen
  L Arnold]
- Initial commit, new app shell with some yaml foo and an example.
  [Stephen L Arnold]
