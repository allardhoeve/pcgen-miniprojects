
from spell import SpellObject


def parse_spells(filename):
    """
    Parse spells in a spells filename

    :arg filename string

    :rtype: A list of SpellObjects
    """

    try:
        with open(filename) as f:
            lstfile = f.read()

    except Exception as e:
        print("Could not open file '%s': %s!\n" % (filename, e))
        raise

    spellobjs = []

    for line in lstfile.split('\n'):
        try:
            spell = SpellObject(line)
        except Exception as e:
            continue

        spellobjs.append(spell)

    return spellobjs
