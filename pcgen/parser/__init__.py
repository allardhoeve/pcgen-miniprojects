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
            spell = SpellObject(line, source)
        except Exception as e:
            raise RuntimeError("Error parsing line: '%s'\n\nLine is:\n\n%s" % (e, line))

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

    sources = filter(lambda x: x.startswith("SOURCELONG"), entries)
    sourcelong = None

    if sources:
        sourcelongtoken = sources[0].split("\t", 1)[0]
        sourcelong = sourcelongtoken.split(":", 1)[1]

    # parse sources
    sourcedef = {
        'filename': filename,
        'sourcelong': sourcelong
    }

    # other entries
    entries = filter(lambda x: not x.startswith("#"), entries)
    entries = filter(lambda x: not x.startswith("SOURCELONG"), entries)
    entries = filter(lambda x: not re.search(r'^\s', x), entries)
    entries = filter(lambda x: not re.search(r'^[^\t]*\.MOD', x), entries)
    entries = filter(lambda x: len(x) > 0, entries)

    return entries, sourcedef