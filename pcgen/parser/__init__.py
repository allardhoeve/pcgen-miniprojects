import re

from pcgen.parser.spell import SpellObject


def parse_spells(filename):
    """
    Parse spells in a spells filename

    :arg filename string

    :rtype: A list of SpellObjects
    """

    (valid_lines, source) = read_lst_file(filename)

    spellobjs = []

    for line in valid_lines:
        try:
            spell = SpellObject(line)
        except Exception as e:
            continue

        spellobjs.append(spell)

    return spellobjs


def read_lst_file(filename):
    """
    Reads and filters an LST file

    :arg filename string

    :rtype: A list of LST entries in text
    """
    with open(filename) as f:
        content = f.read()

    entries = content.split('\n')

    sourcedef = filter(lambda x: x.startswith("SOURCELONG"), entries)

    # other entries
    entries = filter(lambda x: not x.startswith("#"), entries)
    entries = filter(lambda x: not x.startswith("SOURCELONG"), entries)
    entries = filter(lambda x: not re.search(r'^\s', x), entries)
    entries = filter(lambda x: not re.search(r'^[^\t]*\.MOD', x), entries)
    entries = filter(lambda x: len(x) > 0, entries)

    return entries, sourcedef