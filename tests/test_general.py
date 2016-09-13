# -*- coding: utf-8 -*-
"""
    Main command tests
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from click.testing import CliRunner

from fsnviz.cli import main


def test_help():
    runner = CliRunner()
    cmd = runner.invoke(main, ["--help"])
    assert cmd.exit_code == 0
