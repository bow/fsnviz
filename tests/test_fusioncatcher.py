# -*- coding: utf-8 -*-
"""
    fusioncatcher subcommand tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from os import path

from click.testing import CliRunner

from fsnviz.cli import main
from .utils import get_test_path


FNAME1 = get_test_path("fusioncatcher_v0995a_01.txt")


def test_fusioncatcher_ok():
    runner = CliRunner()
    with runner.isolated_filesystem():
        cmd = runner.invoke(main, ["fusioncatcher", FNAME1])
        assert cmd.exit_code == 0
        assert path.exists("fsnviz.svg")


def test_fusioncatcher_circos_exe_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        params = ["--circos-exe", "/nonexistent/file"]
        cmd = runner.invoke(main, params + ["fusioncatcher", FNAME1])
        assert cmd.exit_code != 0
        assert "Could not find an executable circos at '/nonexistent/file'" \
            in cmd.output
        assert not path.exists("fsnviz.svg")


def test_fusioncatcher_out_dir_ok():
    runner = CliRunner()
    with runner.isolated_filesystem():
        out_dir = "my_dir"
        params = ["--out-dir", out_dir]
        cmd = runner.invoke(main, params + ["fusioncatcher", FNAME1])
        assert cmd.exit_code == 0
        assert path.exists(path.join(out_dir, "fsnviz.svg"))
        assert not path.exists("fsnviz.svg")


def test_fusioncatcher_base_name_ok():
    runner = CliRunner()
    with runner.isolated_filesystem():
        base_name = "my_stuff"
        params = ["--base-name", base_name]
        cmd = runner.invoke(main, params + ["fusioncatcher", FNAME1])
        assert cmd.exit_code == 0
        assert path.exists("{0}.svg".format(base_name))
        assert not path.exists("fsnviz.svg")


def test_fusioncatcher_karyotype_ok():
    runner = CliRunner()
    with runner.isolated_filesystem():
        params = ["--karyotype", "human.hg19"]
        cmd = runner.invoke(main, params + ["fusioncatcher", FNAME1])
        assert cmd.exit_code == 0
        assert path.exists("fsnviz.svg")


def test_fusioncatcher_karyotype_png_ok():
    runner = CliRunner()
    with runner.isolated_filesystem():
        params = ["--png"]
        cmd = runner.invoke(main, params + ["fusioncatcher", FNAME1])
        assert cmd.exit_code == 0
        assert path.exists("fsnviz.svg")
        assert path.exists("fsnviz.png")
