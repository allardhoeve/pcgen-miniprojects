#!/usr/bin/env python
from pcgen import find_all_pathfinder_spells


def domain_spell_but_not_cleric_spell(s):
    return s.domains and s.classes and "Cleric" not in s.classes


def spell_is_wizard_spell(s):
    return "Wizard" in s.classes


spells = find_all_pathfinder_spells()
domain_spells = filter(spell_is_wizard_spell, filter(domain_spell_but_not_cleric_spell, spells))


for spell in sorted(domain_spells, key=lambda s: (s.school, s.name)):
    print "%s [%s] is level %s: available at %s" % (spell.name, spell.school.lower(), spell.classes['Wizard'], spell.domains)
