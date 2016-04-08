# -*- coding: utf-8 -*-
"""
    fsnviz.models
    ~~~~~~~~~~~~~

    Common object model.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import abc
from collections import namedtuple

from .utils import render_config


__all__ = ["CircosEntry", "CircosLink", "CircosLabel", "FusionToolResults"]


BaseCircosLabel = namedtuple("BaseCircosLabel",
                             ["chrom", "start", "end", "value"])


BaseCircosLink = namedtuple("BaseCircosLink",
                            ["chromA", "startA", "endA",
                             "chromB", "startB", "endB"])


class CircosLabel(BaseCircosLabel):

    """Class representing a circos label."""

    def make_entry(self, **kwargs):
        base = " ".join([str(x) for x in [self.chrom, self.start,
                                          self.end, self.value]])
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

    def __init__(self, link, genes, link_params={}, genes_params={}):
        self.link = link
        self.genes = genes
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

    def __init__(self, results_fname, tpl_params):
        self._tpl_params = tpl_params

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
    def tpl_params(self):
        """Parameters for rendering circos config file."""
        return self._tpl_params

    def plot(self):
        """Plots the fusion tool results."""
        print(render_config(**self.tpl_params))
        print()
        for link in self.link_entries:
            print(link)
        print()
        for gene in self.gene_entries:
            print(gene)
