#!/usr/bin/env python
from pcgen import find_all_pathfinder_spells


def domain_spell_but_not_cleric_spell(spell):
    return spell.domains and spell.classes and not "Cleric" in spell.classes


def spell_is_wizard_spell(spell):
    return "Wizard" in spell.classes


spells = find_all_pathfinder_spells()
domain_spells = filter(spell_is_wizard_spell, filter(domain_spell_but_not_cleric_spell, spells))


for spell in sorted(domain_spells, key=lambda spell: (spell.school, spell.name)):
    print "%s [%s] is level %s: available at %s" % (spell.name, spell.school.lower(), spell.classes['Wizard'], spell.domains)
