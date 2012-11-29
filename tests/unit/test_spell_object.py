
from unittest import TestCase
from objectparse import SpellObject

class TestSpellObject(TestCase):

    def setUp(self):
        with open("../testdata/pfcr_spells.lst") as f:
            content = f.read()
            self.testlines = content.split('\n')
        # Try Acid Splash
        self.fixture = SpellObject(self.testlines[9])

    def test_spell_object_is_spell_object(self):
        self.assertIsInstance(self.fixture, SpellObject)

    def test_spell_object_has_correct_name_attribute(self):
        self.assertEquals(self.fixture.name, 'Acid Splash')

    def test_spell_object_has_correct_school_attribute(self):
        self.assertEquals(self.fixture.school, 'Conjuration')

    def test_spell_object_has_correct_descriptor_attribute(self):
        self.assertEquals(self.fixture.descriptor, 'Acid')

    def test_spell_object_has_correct_refdoc_attribute(self):
        self.assertEquals(self.fixture.refdoc, None)

    def test_parse_keyword_returns_correct_tuple(self):
        tuple = self.fixture.parseKeyword("SCHOOL:Evocation")
        self.assertEquals(tuple, ("SCHOOL", "Evocation"))

    def test_parse_keyvalue_sets_school_when_given(self):
        fixture = SpellObject()
        fixture.processKeyValue(("SCHOOL", "Evocation"))
        self.assertEquals(fixture.school, "Evocation")




