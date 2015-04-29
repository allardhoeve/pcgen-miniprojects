from unipath import Path
from pcgen import settings
from pcgen.parser import read_lst_file
from pcgen.parser.feat import FeatObject
from pcgen.testcase import TestCase


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

        FeatObject(definition)
