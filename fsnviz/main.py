# -*- coding: utf-8 -*-
"""
    fsnviz.main
    ~~~~~~~~~~~

    Main entry point for command line invocation.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import os
from tempfile import gettempdir

import click

from . import __version__
from . import star_fusion as m_star_fusion
from .utils import which_circos


__all__ = []


@click.group()
@click.version_option(__version__)
@click.option("--out-dir", type=click.Path(),
              default=os.getcwd(),
              help="Output directory. Default: current directory.")
@click.option("--circos-exe", type=str, default="circos",
              help="Circos executable. Default: circos "
                   "(the one accessible via PATH).")
@click.option("--tmp-dir",
              type=click.Path(exists=True, file_okay=False, writable=True,
                              readable=True),
              default=gettempdir(),
              help="Working directory in which fsnviz will write circos "
                   "configuration files and data files. Default: "
                   "{0}".format(gettempdir()))
@click.pass_context
def cli(ctx, out_dir, circos_exe, tmp_dir):
    """Plots gene fusion finding tools' output using circos."""
    ctx.params["out_dir"] = out_dir
    ctx.params["circos_exe"] = which_circos(circos_exe)
    ctx.params["tmp_dir"] = tmp_dir


@cli.command(name="star-fusion")
@click.argument("input", type=click.File("r"))
@click.pass_context
def star_fusion(ctx, input):
    """Plots output of STAR-Fusion."""
    m_star_fusion.plot(input)
