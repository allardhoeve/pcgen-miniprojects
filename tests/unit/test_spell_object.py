
from unittest import TestCase
from objectparse import SpellObject

class TestSpellObject(TestCase):

    def setUp(self):
        self.testline = "Acid Splash\tSCHOOL:Evocation"
        self.fixture = SpellObject(self.testline)

    def test_spell_object_is_spell_object(self):
        self.assertIsInstance(self.fixture, SpellObject)

    def test_spell_object_has_correct_name_attribute(self):
        self.assertEquals(self.fixture.name, 'Acid Splash')

    def test_spell_object_has_correct_school_attribute(self):
        self.assertEquals(self.fixture.school, 'Evocation')

    def test_parse_keyword_returns_correct_tuple(self):
        tuple = self.fixture.parseKeyword("SCHOOL:Evocation")
        self.assertEquals(tuple, ("SCHOOL", "Evocation"))

    def test_parse_keyvalue_sets_school_when_given(self):
        fixture = SpellObject()
        fixture.processKeyValue(("SCHOOL", "Evocation"))
        self.assertEquals(fixture.school, "Evocation")



