import re
from urlparse import urlparse
from fuzzywuzzy import process


class QASpellSourceWeb(object):

    pattern = "(?<=SOURCEWEB:)[^\t]+"

    def __init__(self):
        self.pattern = re.compile(self.pattern)

    def correct(self, spell, srdspells):
        """
        Autocorrect the sourceweb and lstline of a Spell object if needed

        The spell is fixed in-place. The field spell.sourceweb is updated and
        spell.lstline is updated. Invalid SOURCEWEB: is fixed if not there.
        SOURCEWEB:url is appended if missing.

        Positional arguments:
          - spell: SpellObject to be corrected
          - srdspells: an dict of known spells and their URL (prd.get_prd_spell_links)

        Returns:
          - boolean: has the entry been updated?

        """
        # If the sourceweb tests ok, don't touch it
        if self.testlink(spell) is False:  # no errors
            return False

        # Try to find correct link in srdspells
        if spell.name in srdspells:
            spell.sourceweb = srdspells[spell.name]
        else:
            candidate, probability = process.extractOne(spell.name, srdspells)

            if probability < 80:
                return False

            spell.sourceweb = srdspells[candidate]

        # Add or correct SOURCEWEB in lstline
        if self.pattern.search(spell.lstline):
            spell.lstline = self.pattern.sub(spell.sourceweb, spell.lstline)
        else:
            spell.lstline = "%s\t\tSOURCEWEB:%s" % (spell.lstline, spell.sourceweb)

        return True

    def test(self, collection):
        result = []

        for spell in collection:
            error = self.testlink(spell)

            if error:
                result.append((spell, error))

        return result

    def testlink(self, spell):

        if spell.sourceweb is None:
            return "Missing SOURCEWEB"

        result = urlparse(spell.sourceweb)
        if result.scheme and result.netloc and result.path:
            return False

        # Missing or invalid link
        return "URL is not a valid HTTP link"