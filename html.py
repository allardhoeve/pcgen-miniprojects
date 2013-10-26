#!/usr/bin/env python
from jinja2 import Template
from pcgen import find_all_pathfinder_spells

spells = find_all_pathfinder_spells()

with open("templates/spells.html") as tmplfh:
    template = tmplfh.read()
    template = Template(template)

sortedspells = sorted(spells, key=lambda s: s.name)

html = template.render(spells=sortedspells)

with open("spells.html", "w") as htmlfh:
    htmlfh.write(html)
