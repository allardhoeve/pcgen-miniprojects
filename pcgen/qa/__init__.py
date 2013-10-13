import re
from urlparse import urlparse
from pcgen import fuzzy


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
          - False if spell not updated
          - dict if spell updated (can be tested against boolean operaters as True):
            - method: "match" or "fuzzy"
            - match: matched spell name
            - certainty: integer - how probable is the fuzzy match on scale 0-100
            - lst: "add" or "correct" to see how the SOURCEWEB string was handled

        """
        # If the sourceweb tests ok, don't touch it
        if self.testlink(spell) is False:  # no errors
            return False

        correction = {
            "method": None,
            "match": None,
            "certainty": 0,
            "lst": None
        }

        canonicalname = self.get_canonical_name(spell)

        # Try to find correct link in srdspells
        if spell.name in srdspells:
            spell.sourceweb = srdspells[spell.name]
            correction["method"] = "match"
            correction["match"] = spell.name
            correction["certainty"] = 100

        elif canonicalname in srdspells:
            spell.sourceweb = srdspells[canonicalname]
            correction["method"] = "match"
            correction["match"] = canonicalname
            correction["certainty"] = 100

        else:
            candidate, probability, method = fuzzy.match_spell(
                spell.name,
                srdspells,
            )
            correction["method"] = "fuzzy"
            correction["match"] = candidate
            correction["certainty"] = probability

            if probability < 80:
                return False

            spell.sourceweb = srdspells[candidate]

        # Add or correct SOURCEWEB in lstline
        if self.pattern.search(spell.lstline):
            correction["lst"] = "correct"
            spell.lstline = self.pattern.sub(spell.sourceweb, spell.lstline)
        else:
            correction["lst"] = "add"
            spell.lstline = "%s\t\tSOURCEWEB:%s" % (spell.lstline, spell.sourceweb)

        return correction

    def get_canonical_name(self, spell):
        canon = spell.name.strip()
        canon = re.sub(' \((Communal|Greater|Lesser|Mass)\)', r', \1', canon)

        return canon

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