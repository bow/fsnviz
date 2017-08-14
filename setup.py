#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from fsnviz import __author__, __contact__, \
        __homepage__, __version__


with open("README.rst") as src:
    readme = src.read()

with open("CHANGELOG.rst") as src:
    changelog = src.read().replace(".. :changelog:", "").strip()

with open("requirements.txt") as src:
    requirements = [line.strip() for line in src]

with open("requirements-dev.txt") as src:
    test_requirements = [line.strip() for line in src]


setup(
    name="FsnViz",
    version=__version__,
    description="Tool for plotting gene fusion events detected by"
                " various tools using Circos.",
    long_description=readme + "\n\n" + changelog,
    author=__author__,
    author_email=__contact__,
    url=__homepage__,
    packages=find_packages(exclude=["*.tests", "*.tests.*",
                                    "tests.*", "tests"]),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    entry_points="""
    [console_scripts]
    fsnviz=fsnviz.cli:main
    """,
    keywords="rnaseq fusion circos plot bioinformatics visualization",
    tests_require=test_requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
