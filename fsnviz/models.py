# -*- coding: utf-8 -*-
"""
    fsnviz.models
    ~~~~~~~~~~~~~

    Common object model.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import abc
import os
from collections import namedtuple
from math import log
from os import path
from subprocess import run

import click

from .utils import render_config


__all__ = ["CircosEntry", "CircosLink", "CircosLabel", "FsnVizConfig",
           "FusionToolResults"]


FsnVizConfig = namedtuple("FsnVizConfig",
                          ["circos_exe", "base_name", "out_dir"])


BaseCircosLabel = namedtuple("BaseCircosLabel",
                             ["chrom", "start", "end", "value"])


BaseCircosLink = namedtuple("BaseCircosLink",
                            ["chromA", "startA", "endA",
                             "chromB", "startB", "endB"])


class CircosLabel(BaseCircosLabel):

    """Class representing a circos label."""

    def make_entry(self, vfunc=str, **kwargs):
        base = " ".join([str(x) for x in [self.chrom, self.start,
                                          self.end, vfunc(self.value)]])
        if not kwargs:
            return base

        return base + " " + ",".join(["{0}={1}".format(k, v)
                                      for k, v in kwargs.items()])


class CircosLink(BaseCircosLink):

    """Class representing a circos link."""

    def make_entry(self, **kwargs):
        base = " ".join([str(x)
                         for x in [self.chromA, self.startA, self.endA,
                                   self.chromB, self.startB, self.endB]])
        if not kwargs:
            return base

        return base + " " + ",".join(["{0}={1}".format(k, v)
                                      for k, v in kwargs.items()])


class CircosEntry(object):

    """Class representing a circos fusion plot entry."""

    def __init__(self, link, genes, junction_reads, spanning_frags,
                 link_params={}, genes_params={}):
        self.link = link
        self.genes = genes
        self.junction_reads = junction_reads
        self.spanning_frags = spanning_frags
        self.link_params = link_params
        self.genes_params = genes_params

    def make_link_entry(self):
        return self.link.make_entry(**self.link_params)

    def make_genes_entries(self):
        return [x.make_entry(**self.genes_params) for x in self.genes]


class FusionToolResults(metaclass=abc.ABCMeta):

    """Abstract class for representing fusion tool results."""

    @abc.abstractproperty
    def circos_entries(self):
        """Circos entries present in the tool results."""

    def __init__(self, results_fname, config, circos_config, tpl_params):
        self._tpl_params = tpl_params
        self._config = config
        out_dir = self.config.out_dir
        self._circos_config_file = circos_config or \
            path.join(out_dir, "circos.conf")
        self._config_supplied = bool(circos_config)
        self._links_file = path.join(out_dir, "links.txt")
        self._genes_file = path.join(out_dir, "genes.txt")
        self._junction_reads_file = path.join(out_dir, "junction_reads.txt")
        self._spanning_frags_file = path.join(out_dir, "spanning_frags.txt")

    @property
    def gene_entries(self):
        unique_genes = set([gene
                            for entry in self.circos_entries
                            for gene in entry.make_genes_entries()])
        for gene in unique_genes:
            yield gene

    @property
    def link_entries(self):
        for entry in self.circos_entries:
            yield entry.make_link_entry()

    @property
    def config(self):
        """Internal config values."""
        return self._config

    @property
    def tpl_params(self):
        """Parameters for rendering circos config file."""
        return self._tpl_params

    def _prep_dir(self):
        out_dir = self.config.out_dir
        if not path.exists(out_dir):
            os.makedirs(out_dir)
        elif path.exists(out_dir) and path.isfile(out_dir):
            msg = "Path '{0}' already exists as a file."
            raise click.BadParameter(msg.format(out_dir))

    def _write_circos_config(self):
        tpl_params = self.tpl_params
        tpl_params["fusion_links_file"] = self._links_file
        tpl_params["gene_labels_file"] = self._genes_file
        tpl_params["junction_reads_file"] = self._junction_reads_file
        tpl_params["spanning_frags_file"] = self._spanning_frags_file
        with open(self._circos_config_file, "w") as target:
            print(render_config(**tpl_params), file=target)

    def _write_links_file(self):
        with open(self._links_file, "w") as target:
            for link in self.link_entries:
                print(link, file=target)

    def _write_genes_file(self):
        with open(self._genes_file, "w") as target:
            for gene in self.gene_entries:
                print(gene, file=target)

    def _write_data_files(self):
        with open(self._junction_reads_file, "w") as target:
            for ce in self.circos_entries:
                for jr in ce.junction_reads:
                    if jr.value == 0:
                        continue
                    print(jr.make_entry(vfunc=log), file=target)

        with open(self._spanning_frags_file, "w") as target:
            for ce in self.circos_entries:
                for sf in ce.spanning_frags:
                    if sf.value == 0:
                        continue
                    print(sf.make_entry(vfunc=log), file=target)

    def _execute_circos(self):
        cmd_toks = [self.config.circos_exe, "-conf", self._circos_config_file]
        run(cmd_toks)

    def plot(self):
        """Plots the fusion tool results."""
        self._prep_dir()
        self._write_links_file()
        self._write_genes_file()
        self._write_data_files()
        if not self._config_supplied:
            self._write_circos_config()
        self._execute_circos()
