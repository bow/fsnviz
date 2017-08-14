# -*- coding: utf-8 -*-
"""
    fsnviz.fusioncatcher
    ~~~~~~~~~~~~~~~~~~~~

    FusionCatcher output plotting.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from crimson.fusioncatcher import parse

from .models import CircosEntry, CircosLabel, CircosLink, FusionToolResults
from .utils import adjust_chrom


__all__ = ["FusionCatcherResults"]


class FusionCatcherResults(FusionToolResults):

    """Class representing a FusionCatcher run result."""

    mito_names = ("chrM", "M", "MT")

    def __init__(self, results_fname, config, circos_config, tpl_params):
        super().__init__(results_fname, config, circos_config, tpl_params)
        self.payload = parse(results_fname)

    def _make_circos_entry(self, raw_entry):
        left = raw_entry["5end"]
        right = raw_entry["3end"]
        if left["chromosome"] in self.mito_names:
            return
        if right["chromosome"] in self.mito_names:
            return
        lchrom = adjust_chrom(left["chromosome"])
        rchrom = adjust_chrom(right["chromosome"])

        link = CircosLink(lchrom, left["position"], left["position"] + 1,
                          rchrom, right["position"], right["position"] + 1)

        geneA = CircosLabel(lchrom, left["position"], left["position"] + 1,
                            left["geneSymbol"])
        geneB = CircosLabel(rchrom, right["position"], right["position"] + 1,
                            right["geneSymbol"])

        njr = raw_entry["nSpanningUniqueReads"]
        nsf = raw_entry["nSpanningPairs"]

        jrA = CircosLabel(lchrom, left["position"], left["position"] + 1,
                          njr)
        jrB = CircosLabel(rchrom, right["position"], right["position"] + 1,
                          njr)

        sfA = CircosLabel(lchrom, left["position"], left["position"] + 1,
                          nsf)
        sfB = CircosLabel(rchrom, right["position"], right["position"] + 1,
                          nsf)

        return CircosEntry(link, [geneA, geneB], [jrA, jrB], [sfA, sfB])

    @property
    def circos_entries(self):
        if not hasattr(self, "_circos_entries"):
            entries = [self._make_circos_entry(x) for x in self.payload]
            self._circos_entries = list(filter(None, entries))
        return self._circos_entries
