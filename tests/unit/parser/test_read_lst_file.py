import re
import mock
from pcgen.parser import read_lst_file
from pcgen.testcase import TestCase


class TestReadLstFile(TestCase):

    def setUp(self):
        self.fixture = "# CVS $Revision$ $Author$ -- Sat Oct 13 13:49:23 2012 -- reformated by prettylst.pl v1.39 (build 15052)\nSOURCELONG:Core Rulebook\n \n\t\n# Original Entry by: Eddy Anthony\n# Incorporated 11/22/2011 errata (Stefan Radermacher)\n\n###Block: A\n# Spell Name\nAcid Arrow\nAcid Fog\nAcid Splash\nAcid Splash.MOD\n"
        self.mock_open = self.setUpPatch("__builtin__.open", mock.mock_open(read_data=self.fixture))

    def test_read_lst_file_opens_designated_file(self):
        read_lst_file("testnaam")
        self.mock_open.assert_called_once_with("testnaam")

    def test_read_lst_file_croaks_when_file_does_not_exist_or_ioerror(self):
        self.mock_open.side_effect = IOError
        self.assertRaises(IOError, read_lst_file, "testnaam")

    def test_read_lst_file_returns_a_list_of_lines_in_file(self):
        ret = read_lst_file("Testnaam")
        ret[0]

    def test_read_lst_file_filters_mods(self):
        ret = read_lst_file("Testnaam")
        for line in ret:
            self.assertFalse(re.search(r'^[^\t]*\.MOD', line), "line is a MOD line: %s" % line)

    def test_read_lst_file_filters_lines_starting_with_hash(self):
        ret = read_lst_file("Testnaam")
        for line in ret:
            self.assertFalse(line.startswith("#"), "line starts with hash: %s" % line)

    def test_read_lst_file_filters_source_lines(self):
        ret = read_lst_file("Testnaam")
        for line in ret:
            self.assertFalse(line.startswith("SOURCELONG:"), "line starts with source token: '%s'" % line)

    def test_read_lst_file_filters_empty_lines(self):
        ret = read_lst_file("Testnaam")
        for line in ret:
            self.assertTrue(len(line) > 0, "line has zero length")

    def test_read_lst_file_filters_lines_starting_with_whitespace(self):
        ret = read_lst_file("Testnaam")
        for line in ret:
            self.assertFalse(re.search(r'^\s', line), "line starts with white-space: '%s'" % line)