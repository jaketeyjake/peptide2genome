========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/peptide2genome/badge/?style=flat
    :target: https://readthedocs.org/projects/peptide2genome
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/jaketeyjake/peptide2genome.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jaketeyjake/peptide2genome

.. |version| image:: https://img.shields.io/pypi/v/peptide2genome.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/peptide2genome

.. |commits-since| image:: https://img.shields.io/github/commits-since/jaketeyjake/peptide2genome/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jaketeyjake/peptide2genome/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/peptide2genome.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/peptide2genome

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/peptide2genome.svg
    :alt: Supported versions
    :target: https://pypi.org/project/peptide2genome

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/peptide2genome.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/peptide2genome


.. end-badges

Django-backed API for mapping peptides onto genomic coordinates.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install peptide2genome

Documentation
=============


https://peptide2genome.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
