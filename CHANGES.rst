=========
Changelog
=========

..
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://pip.pypa.io/en/latest/development/#adding-a-news-entry
    we named the news folder "changes".

    WARNING: Don't drop the next directive!

.. towncrier release notes start

0.3.0
=====

*(2025-02-20)*


Features
--------

- Implemented support for the free-threaded build of CPython 3.13 -- by :user:`lysnikolaou`.

  *Related issues and pull requests on GitHub:*
  :issue:`84`.


Packaging updates and notes for downstreams
-------------------------------------------

- Started building wheels for the free-threaded build of CPython 3.13 -- by :user:`lysnikolaou`.

  *Related issues and pull requests on GitHub:*
  :issue:`84`.


Contributor-facing changes
--------------------------

- GitHub Actions CI/CD is now configured to manage caching pip-ecosystem
  dependencies using `re-actors/cache-python-deps`_ -- an action by
  :user:`webknjaz` that takes into account ABI stability and the exact
  version of Python runtime.

  .. _`re-actors/cache-python-deps`:
     https://github.com/marketplace/actions/cache-python-deps

  *Related issues and pull requests on GitHub:*
  :issue:`93`.


----


0.2.1
=====

*(2024-12-01)*


Bug fixes
---------

- Stopped implicitly allowing the use of Cython pre-release versions when
  building the distribution package -- by :user:`ajsanchezsanz` and
  :user:`markgreene74`.

  *Related commits on GitHub:*
  :commit:`64df0a6`.

- Fixed ``wrapped`` and ``func`` not being accessible in the Cython versions of :func:`propcache.api.cached_property` and :func:`propcache.api.under_cached_property` decorators -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`72`.


Removals and backward incompatible breaking changes
---------------------------------------------------

- Removed support for Python 3.8 as it has reached end of life -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`57`.


Packaging updates and notes for downstreams
-------------------------------------------

- Stopped implicitly allowing the use of Cython pre-release versions when
  building the distribution package -- by :user:`ajsanchezsanz` and
  :user:`markgreene74`.

  *Related commits on GitHub:*
  :commit:`64df0a6`.


----


0.2.0
=====

*(2024-10-07)*


Bug fixes
---------

- Fixed loading the C-extensions on Python 3.8 -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`26`.


Features
--------

- Improved typing for the :func:`propcache.api.under_cached_property` decorator -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`38`.


Improved documentation
----------------------

- Added API documentation for the :func:`propcache.api.cached_property` and :func:`propcache.api.under_cached_property` decorators -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`16`.


Packaging updates and notes for downstreams
-------------------------------------------

- Moved :func:`propcache.api.under_cached_property` and :func:`propcache.api.cached_property` to `propcache.api` -- by :user:`bdraco`.

  Both decorators remain importable from the top-level package, however importing from `propcache.api` is now the recommended way to use them.

  *Related issues and pull requests on GitHub:*
  :issue:`19`, :issue:`24`, :issue:`32`.

- Converted project to use a src layout -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`22`, :issue:`29`, :issue:`37`.


----


0.1.0
=====

*(2024-10-03)*


Features
--------

- Added ``armv7l`` wheels -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`5`.


----


0.0.0
=====

*(2024-10-02)*


- Initial release.
