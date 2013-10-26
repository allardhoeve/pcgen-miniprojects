from pcgen.testcase import TestCase
from pcgen.parser import describes_lst_global as lstglobal


class TestLineDescribesObject(TestCase):

    def test_describes_lst_global_matches_only_globals(self):
        self.assertFalse(lstglobal(""))
        self.assertFalse(lstglobal("Aid\t\tDESC:Aid"))
        self.assertFalse(lstglobal("#SOURCELONG:Ultimate Magic"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic\t\tSOURCESHORT:UM"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic\t\tSOURCESHORT:UM\t\tSOURCEWEB:http://paizo.com/pathfinderRPG/v5748btpy8g7s"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic\t\tSOURCESHORT:UM\t\tSOURCEWEB:http://paizo.com/pathfinderRPG/v5748btpy8g7s#magic-missile"))