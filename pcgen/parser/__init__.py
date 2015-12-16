import re
from pcgen.parser.feat import FeatFactory
from pcgen.parser.spell import SpellFactory


def parse_feats(filename, source=None):
    return parse_objects(filename, source, FeatFactory)


def parse_spells(filename, source=None):
    return parse_objects(filename, source, SpellFactory)


def parse_objects(filename, source=None, myObject=None):
    """
    Parse spells in a spells filename

    :arg filename string

    :rtype: A list of SpellObjects
    """

    (valid_lines, lstsource) = read_lst_file(filename)

    # not all lst files define a source, take it from pcc if missing
    if not lstsource['sourcelong']:
        lstsource['sourcelong'] = source['sourcelong']

    objs = []

    for line in valid_lines:
        try:
            obj = myObject(line, source)
        except Exception as e:
            raise RuntimeError("Error parsing line: '%s'\n\nLine is:\n\n%s" % (e, line))

        objs.append(obj)

    return objs


def read_lst_file(filename):
    """
    Reads and filters an LST file

    :arg filename string

    :rtype: A list of LST entries in text
    """
    with open(filename) as f:
        content = f.read()

    entries = content.split('\n')

    sources = filter(lambda x: x.startswith("SOURCELONG") or x.startswith("#SOURCELONG"), entries)
    sourcelong = None

    if sources:
        sourcelongtoken = sources[0].split("\t", 1)[0]
        sourcelong = sourcelongtoken.split(":", 1)[1]

    # parse sources
    sourcedef = {
        'sourcefile': filename,
        'sourcelong': sourcelong
    }

    # other entries
    entries = filter(describes_valid_lst_object, entries)

    return entries, sourcedef


re_lst_global = re.compile(r"^[A-Z]+:[\w ']+(?:\t|$)")


def describes_lst_global(line):
    return re_lst_global.search(line)


def remove_sourcelink_from_lst_global(line):
    return re.sub(r'SOURCELINK:[^\t]+\t*', '', line).rstrip()


def describes_valid_lst_object(line):
    return (not line.startswith("#") and
            not describes_lst_global(line) and
            not re.search(r'^\s', line) and
            not re.search(r'^[^\t]*\.MOD', line) and
            not re.search(r'^[^\t]*\.COPY', line) and
            len(line) > 0)
