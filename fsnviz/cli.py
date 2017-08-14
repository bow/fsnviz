# -*- coding: utf-8 -*-
"""
    fsnviz.cli
    ~~~~~~~~~~

    Main entry point for command line invocation.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import os

import click

from . import __version__
from .models import FsnVizConfig
from .fusioncatcher import FusionCatcherResults
from .star_fusion import STARFusionResults
from .utils import which_circos, get_karyotype_file as gkf


__all__ = []


@click.group()
@click.version_option(__version__)
@click.option("--out-dir", type=click.Path(),
              default=None,
              help="Output directory. Default: current run directory.")
@click.option("-n", "--base-name", type=str,
              default="fsnviz",
              help="Base file name of the image output. "
                   "Filename extensions will be added accordingly.")
@click.option("-k", "--karyotype",
              type=click.Choice(["human.hg19", "human.hg38"]),
              default="human.hg19",
              help="Karyotype to use. Must be supported by circos. "
                   "If the `--karyotype-file` parameter is defined, "
                   "this parameter is ignored. Default: human.hg19.")
@click.option("-c", "--circos-conf",
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help="Circos configuration file. If not supplied, "
                   "fsnviz generates a default one.")
@click.option("--png/--no-png", default=False,
              help="Whether to create PNG plots or not. Default: no.")
@click.option("--svg/--no-svg", default=True,
              help="Whether to create SVG plots or not. Default: yes.")
@click.option("--karyotype-file",
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Karyotype file to use. This parameter takes precedence "
                   "over the `--karyotype` parameter.")
@click.option("--circos-exe", type=str, default="circos",
              help="Circos executable. Default: circos "
                   "(the one accessible via PATH).")
@click.pass_context
def main(ctx, out_dir, base_name, karyotype, circos_conf, png, svg,
         karyotype_file, circos_exe):
    """Plots gene fusion finding tools' output using circos."""
    if out_dir is None:
        out_dir = os.getcwd()
    ctx.params["_config"] = \
        FsnVizConfig(which_circos(circos_exe), base_name, out_dir)

    kfile = karyotype_file if karyotype_file is not None else gkf(karyotype)
    # Parameters passable directly to our jinja template
    ctx.params["circos_config"] = circos_conf
    ctx.params["_j2"] = {
        "karyotype": kfile,
        "image_dir": out_dir,
        "image_file": base_name,
        "image_png": "yes" if png else "no",
        "image_svg": "yes" if svg else "no",
    }


@main.command(name="star-fusion")
@click.argument("input", type=click.File("r"))
@click.pass_context
def star_fusion(ctx, input):
    """Plots output of STAR-Fusion."""
    res = STARFusionResults(input, ctx.parent.params["_config"],
                            ctx.parent.params["circos_config"],
                            ctx.parent.params["_j2"])
    res.plot()


@main.command(name="fusioncatcher")
@click.argument("input", type=click.File("r"))
@click.pass_context
def fusioncatcher(ctx, input):
    """Plots output of FusionCatcher."""
    res = FusionCatcherResults(input, ctx.parent.params["_config"],
                               ctx.parent.params["circos_config"],
                               ctx.parent.params["_j2"])
    res.plot()
