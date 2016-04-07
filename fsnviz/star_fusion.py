# -*- coding: utf-8 -*-
"""
    fsnviz.star_fusion
    ~~~~~~~~~~~~~~~~~~

    STAR-Fusion output plotting.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from crimson.star_fusion import parse


__all__ = ["plot"]


def plot(results_fname):
    """Creates a circos plot of the given STAR-Fusion results file."""
    payload = parse(results_fname)
