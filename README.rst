FsnViz
======

|ci| |coverage| |pypi|

.. |ci| image:: https://travis-ci.org/bow/fsnviz.svg?branch=master
    :target: https://travis-ci.org/bow/fsnviz

.. |coverage| image:: https://codecov.io/gh/bow/fsnviz/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bow/fsnviz

.. |pypi| image:: https://badge.fury.io/py/FsnViz.svg
    :target: http://badge.fury.io/py/fsnviz


FsnViz is a Python tool for plotting RNA-seq fusion events using Circos plots.
It parses outputs of gene fusion finding tools and creates Circos plots out of
it.

Currently it accepts outputs of the following gene fusion finding tool:

* `STAR-Fusion <https://github.com/STAR-Fusion/STAR-Fusion>`_ hits table
  (``star-fusion``)
* `FusionCatcher <https://github.com/ndaniel/fusioncatcher>`_ final table
  (``fusioncatcher``)


Requirements
------------

FsnViz is tested on the following Python versions:
    * 3.5
    * 3.6

and the following Circos versions:
    * 0.69-2

Other Circos versions may be used but they are not guaranteed to work.

Installation
------------

You can download the latest version via pip:

    $ pip install fsnviz

Circos needs to be installed separately.


Usage
-----

FsnViz needs only a result file of the gene fusion finding tool:

    $ fsnviz star-fusion /path/to/result/file

With the invocation above, it will create the Circos plot as an SVG image
called ``fsnviz.svg`` in the current directory. You can adjust the output
behavior using some flags such as:

    * The ``--output-dir`` flag to set the output directory. If it does not
      exist, it will be created for you.
    * The ``--base-name`` flag to set the base name of the Circos plot
      (the default is ``fsnviz``). Filename extensions are added accordingly.
    * The ``--karyotype`` flag to set the Circos reference karyotype.
      Currently only ``human.hg19`` and ``human.hg38`` are available.

For a complete list, check out the help via ``fsnviz --help``.


Credits
-------

* Initial circos templates were based on the Circos templates of
  `viewFusion <https://github.com/riverlee/viewFusion>`_, written by Jiang Li.


License
-------

FsnViz is BSD-licensed. Refer to the ``LICENSE`` file for the full license.
