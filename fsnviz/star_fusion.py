# -*- coding: utf-8 -*-
"""
    fsnviz.star_fusion
    ~~~~~~~~~~~~~~~~~~

    STAR-Fusion output plotting.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from crimson.star_fusion import parse

from .models import CircosEntry, CircosLabel, CircosLink, FusionToolResults
from .utils import adjust_chrom


__all__ = ["STARFusionResults"]


class STARFusionResults(FusionToolResults):

    """Class representing a STAR-Fusion run result."""

    mito_names = ("chrM", "M", "MT")

    def __init__(self, results_fname, config, circos_config, tpl_params):
        super().__init__(results_fname, config, circos_config, tpl_params)
        self.payload = parse(results_fname)

    def _make_circos_entry(self, raw_entry):
        left = raw_entry["left"]
        right = raw_entry["right"]
        if left["chromosome"] in self.mito_names:
            return
        if right["chromosome"] in self.mito_names:
            return
        lchrom = adjust_chrom(left["chromosome"])
        rchrom = adjust_chrom(right["chromosome"])

        link = CircosLink(lchrom, left["position"], left["position"] + 1,
                          rchrom, right["position"], right["position"] + 1)

        geneA = CircosLabel(lchrom, left["position"], left["position"] + 1,
                            left["geneName"])
        geneB = CircosLabel(rchrom, right["position"], right["position"] + 1,
                            right["geneName"])

        njr = raw_entry["nJunctionReads"]
        nsf = raw_entry["nSpanningFrags"]

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
