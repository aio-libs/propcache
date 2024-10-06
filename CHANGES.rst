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

1.0.0
=====

*(2024-10-05)*


Removals and backward incompatible breaking changes
---------------------------------------------------

- Moved :func:`propcache.api.under_cached_property` and :func:`propcache.api.cached_property` to ``propcache.api`` -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`19`.


Improved documentation
----------------------

- Added API documentation for the :func:`propcache.api.cached_property` and :func:`propcache.api.under_cached_property` decorators -- by :user:`bdraco`.

  *Related issues and pull requests on GitHub:*
  :issue:`16`.


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
