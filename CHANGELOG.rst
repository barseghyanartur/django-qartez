Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.8.1
---
2020-02-20

- Tested against Django 3.0.

0.8
---
2020-02-19

- Tested against Django 2.0, 2.1, 2.2.
- Tested against Python 3.7 and 3.8.
- Drop support for Django versions prior 1.11.

0.7.1
-----
2017-11-27

- Fixes in docs.

0.7
---
2017-11-27

- Django 1.8, 1.9, 1.10 and 1.11 support. Drop support for older Django
  versions.
- Minor fixes.
- Improved tests, PyTest test runner, coverage, introduce factories.

0.6
---
2014-10-12

- Django 1.7 support.
- Softened `six` requirements.

0.5
---
2013-09-09

- Python 3 support.

0.1
---
2013-02-04

- Initial.
