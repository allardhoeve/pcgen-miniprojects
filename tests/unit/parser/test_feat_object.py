from pcgen.parser import FeatParser
from pcgenminiprojects.testcase import TestCase


class TestFeatObject(TestCase):

    def test_featobject_parses_acrobatic(self):
        definition = "\t".join([
            'Acrobatic',
            'TYPE:General',
            'DESC:You are skilled at leaping, jumping, and flying.',
            'BONUS:SKILL|Acrobatics|if(skillinfo("RANK","Acrobatics")>=10,4,2)',
            'BONUS:SKILL|Fly|if(skillinfo("RANK","Fly")>=10,4,2)',
            'SOURCEPAGE:p.113',
            'BENEFIT:You get a +2 bonus on all Acrobatics and Fly skill checks.'
        ])

        feat = FeatParser(definition)
        self.assertEqual(feat.name, "Acrobatic")
        self.assertEqual(feat.type, "General")
