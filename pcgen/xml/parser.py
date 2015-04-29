

def parse_domain_spells(per_day):
    """Parse 6+1 style numbers
    :param str per_day: number of spells and domain spells per day: 6+1 or 4
    :return: number of spells per day and number of domain spells per day
    :rtype: (int, int)
    """
    return tuple(int(n) for n in per_day.split("+", 2)) \
        if "+" in per_day \
        else (int(per_day), 0)


def parse_class(class_el):
    """Parse an XML element representing a spell-casting class
    :param `lxml.Element` class_el: The XML class element to parse
    :return: a tuple containing the class name and a dict containing the levels and number of spells per level
    :rtype: dict[int, (int, int)]
    """
    levels = [parse_level(level) for level in class_el.xpath('level')]
    return {level: spells for level, spells in levels}


def parse_level(level_el):
    """Parse an XML element representing a spell-casting class level
    :param `lxml.Element` level_el: The XML class element to parse
    :return: a tuple containing the level and another tuple containing spells per day and domain spells per day
    :rtype: (int, (int, int))
    """
    level = int(level_el.attrib['number'])
    return level, parse_domain_spells(level_el.attrib['cast'])


def parse_spells_per_day(tree):
    def get_class_name(class_el):
        return class_el.attrib['spelllistclass'].lower()

    return {get_class_name(el): parse_class(el) for el in tree.xpath('//known_spells/class')}
