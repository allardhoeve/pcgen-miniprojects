from pcgenminiprojects.testcase import TestCase
from pcgen.parser import describes_lst_global as lstglobal
from pcgen.parser import remove_sourcelink_from_lst_global as rmglobal


class TestLstGlobalObject(TestCase):

    def test_describes_lst_global_matches_only_globals(self):
        self.assertFalse(lstglobal(""))
        self.assertFalse(lstglobal("Aid\t\tDESC:Aid"))
        self.assertFalse(lstglobal("#SOURCELONG:Ultimate Magic"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic\t\tSOURCESHORT:UM"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic\t\tSOURCESHORT:UM\t\tSOURCELINK:http://paizo.com/pathfinderRPG/v5748btpy8g7s"))
        self.assertTrue(lstglobal("SOURCELONG:Ultimate Magic\t\tSOURCESHORT:UM\t\tSOURCELINK:http://paizo.com/pathfinderRPG/v5748btpy8g7s#magic-missile"))

    def test_remove_sourcelink_from_global_removes_any_sourcelink_global_tags_from_line(self):
        globals = "SOURCELONG:Ultimate Magic"
        self.assertEquals(rmglobal(globals), globals)

        globals = "SOURCELONG:Ultimate Magic\tSOURCESHORT:UM"
        self.assertEqual(rmglobal(globals), globals)

        globals = "SOURCELONG:Ultimate Magic\tSOURCESHORT:UM\tSOURCELINK:http://paizo.com/pathfinderRPG/v5748btpy8g7s"
        self.assertEqual(rmglobal(globals), "SOURCELONG:Ultimate Magic\tSOURCESHORT:UM")

        globals = "SOURCELONG:Ultimate Magic\tSOURCESHORT:UM\tSOURCELINK:http://paizo.com/pathfinderRPG/v5748btpy8g7s\tSOURCEDATE:2011-05"
        self.assertEqual(rmglobal(globals), "SOURCELONG:Ultimate Magic\tSOURCESHORT:UM\tSOURCEDATE:2011-05")
