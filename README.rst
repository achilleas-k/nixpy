.. image:: https://travis-ci.org/G-Node/nixpy.svg?branch=master
    :target: https://travis-ci.org/G-Node/nixpy
.. image:: https://ci.appveyor.com/api/projects/status/nrsgupr9ura3vli3?svg=true
    :target: https://ci.appveyor.com/project/achilleas-k/nixpy-um2sy
.. image:: https://coveralls.io/repos/github/G-Node/nixpy/badge.svg?branch=master
    :target: https://coveralls.io/github/G-Node/nixpy?branch=master


----

Versions
--------

This repository's `master` is the development branch of *NIXPY*.
It is not guaranteed to build or work properly.
At times it may not even work at all.
We strongly recommend using the latest stable version, which can be found on PyPI as nixio_.

About NIXPY
-----------

*NIXPY* is a reimplementation of NIX_ in Python.

Getting Started
---------------

The simplest way to install *NIXPY* is from PyPI using pip. The name of the package is nixio_::

    pip install nixio

Bindings for C++ NIX
--------------------

Originally, *NIXPY* served as a set of Python bindings to the C++ (reference) implementation of NIX_.
For a while, the bindings and a full reimplementation of NIX in Python were both included in this module.
Now, since v1.5, the bindings have been removed and only the reimplementation is supported and maintained.
This was done to make deployment simpler for Python users and to make the library simpler to maintain for the developers and contributors.

To check if installed properly
------------------------------

Try importing nixio::

    >>> import nixio
    >>>

If python successfully executes :code:`import nixio`, the installation went well.
Check out the API documentation for further tutorials.


NIXPY API Documentation
-----------------------

The API documentation can be found `here <http://g-node.github.io/nixpy/>`_.


.. _nixio: https://pypi.python.org/pypi/nixio
.. _NIX: https://github.com/G-Node/nix
