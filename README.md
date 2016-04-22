PyMCTS: Monte Carlo Tree Search for Python
==========================================

[![Build Status](https://travis-ci.org/smallnamespace/pymcts.svg)](https://travis-ci.org/smallnamespace/pymcts)


What is PyMCTS?
-------------

PyMCTS is a Python implementation of [Monte Carlo Tree Search]
(https://en.wikipedia.org/wiki/Monte_Carlo_tree_search), which is a
heuristic technique for discrete decision processes, most notably
in game AI and in planning.

PyMCTS aims for a simple, clean framework for MCTS so that particular
variants, such as UCT (Upper Confidence Trees) can be easily worked in.
PyMCTS will also have a basic toolkit for evaluating quality of search
trees, and visualization tools to aid the user.

PyMCTS is in early development. Features are still in flux, and
are being implemented.
See 'Development status' below.


Requirements
------------

PyMCTS requires Python 3.5.1 or later to run. Users are strongly urged to
consider Continuum Analytics' [Anaconda]
(https://www.continuum.io/downloads) Python distribution, as it contains
packages likely to be of interest to PyMCTS users and contributors.


Quick start
-----------

You can install the latest version from git:

    $ pip3 install git+git://github.com/smallnamespace/pymcts.git


Development status and Issue Tracker
------------------------------------

PyMCTS is an early work in progress; the API is still in flux and additional
features are being discussed and implemented.

Please see [open issues](https://github.com/smallnamespace/pymcts/issues)
for development progress and upcoming features.


Contributing
------------

Any help would be appreciated. Please reach out directly, or send pull
requests.

License
-------

PyMCTS is licensed under the Apache v2 License (see LICENSE).
