#!/usr/bin/env python
from pcgen import find_all_pathfinder_spells


def domain_spell_but_not_cleric_spell(spell):
    print spell.domains
    return spell.domains and spell.classes and not "Cleric" in spell.classes

spells = find_all_pathfinder_spells()
domain_spells = filter(domain_spell_but_not_cleric_spell, spells)

for spell in domain_spells:
    print "%s: domains=%s, classes=%s" % (spell.name, spell.domains, spell.classes)
