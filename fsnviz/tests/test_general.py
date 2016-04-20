# -*- coding: utf-8 -*-
"""
    fsnviz.tests.test_general
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Main command tests.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from os import path

from click.testing import CliRunner

from fsnviz.main import cli
from .utils import get_test_path


def test_help():
    runner = CliRunner()
    cmd = runner.invoke(cli, ["--help"])
    assert cmd.exit_code == 0


def test_star_fusion_ok():
    runner = CliRunner()
    in_path = get_test_path("star_fusion_v060_01.txt")
    with runner.isolated_filesystem():
        cmd = runner.invoke(cli, ["star-fusion", in_path])
        assert cmd.exit_code == 0
        assert path.exists("fsnviz.svg")
