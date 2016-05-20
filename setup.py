#!/usr/bin/env python

from setuptools import setup, find_packages

CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Topic :: Games/Entertainment :: Turn Based Strategy",
]

_tests_require = ["pytest", "hypothesis", "pytest-benchmark"]

setup(
    name="pymcts",
    version=0.1,
    packages=find_packages(exclude="tests"),
    tests_require=_tests_require,
    extras_require={"tests": _tests_require, "drawing": ["python-igraph"]},
    author="smallnamespace",
    author_email="smallnamespace@gmail.com",
    description="Python implementation of Monte Carlo Tree Search (MCTS)",
    classifiers=CLASSIFIERS,
    download_url="https://github.com/smallnamespace/pymcts/tarball/master",
    license="ASL v2",
    url="https://github.com/smallnamespace/pymcts",
    zip_safe=True,
)
