# -*- coding: utf-8 -*-
"""
    fsnviz.star_fusion
    ~~~~~~~~~~~~~~~~~~

    STAR-Fusion output plotting.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from crimson.star_fusion import parse

from .utils import render_config


__all__ = ["plot"]


def plot(input_fname, tpl_params):
    """Creates a circos plot of the given STAR-Fusion results file."""
    payload = parse(input_fname)
    print(render_config(**tpl_params))
