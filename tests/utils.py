# -*- coding: utf-8 -*-
"""
    General test utilities
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from os.path import abspath, dirname, join


TEST_CASE_DIR = abspath(join(dirname(__file__), "cases"))


def get_test_path(bname, test_dir=TEST_CASE_DIR):
    """Helper method to return the path of a test case file or directory.

    :param bname: Test case base name.
    :type bname: str
    :param test_dir: Test case directory name.
    :type test_dir: str
    :returns: Absolute path to the test case file or directory.
    :rtype: str

    """
    return abspath(join(test_dir, bname))
