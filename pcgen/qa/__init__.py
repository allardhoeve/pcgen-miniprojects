import re
from urlparse import urlparse
from pcgen import matcher


class QASpellSourceLink(object):

    pattern = "(?<=SOURCELINK:)[^\t]+"

    def __init__(self):
        self.pattern = re.compile(self.pattern)

    def correct(self, spell, srdspells, suggestions=None):
        """
        Autocorrect the sourcelink and lstline of a Spell object if needed

        The spell is fixed in-place. The field spell.sourcelink is updated and
        spell.lstline is updated. Invalid SOURCELINK: is fixed if not there.
        SOURCELINK:url is appended if missing.

        Positional arguments:
          - spell: SpellObject to be corrected
          - srdspells: a dict of known spells and their URL (prd.get_prd_spell_links)
          - suggestions: a dict with two key-values containing dicts:
            - suggestions["links"]["Aid"] -> "http://pcgen.nl/aid.html"
            - suggestions["matcher"]["Aid (evil)"] -> "Aid"
            - this is optionally used to match spells that are normally missed so
              that the script can be run many times on the same data without intervention

        Returns:
          - False if spell not updated
          - dict if spell updated (can be tested against boolean operaters as True):
            - method: "match" or "fuzzy"
            - match: matched spell name
            - certainty: integer - how probable is the fuzzy match on scale 0-100
            - lst: "add" or "correct" to see how the SOURCELINK string was handled

        """
        # If the sourcelink tests ok, don't touch it
        if self.testlink(spell) is False:  # no errors
            return False

        query = spell.name

        # Look in suggestions table to see if a suggestion was provided
        if suggestions and "links" in suggestions and query in suggestions["links"]:
            candidate = query
            certainty = 100
            method = "suggestion"
            link = suggestions["links"][query]

        # Otherwise we use the matcher to find the spell
        else:
            matcher_suggestions = None
            if suggestions and "matcher" in suggestions:
                matcher_suggestions = suggestions["matcher"]

            candidate, certainty, method = matcher.match_spell(
                query,
                srdspells,
                suggestions=matcher_suggestions
            )

            # No match found
            if candidate is None:
                return False

            link = srdspells[candidate]

        # Set the link we found
        spell.sourcelink = link

        # Add or correct SOURCELINK in lstline
        lst = None
        if self.pattern.search(spell.lstline):
            lst = "correct"
            spell.lstline = self.pattern.sub(spell.sourcelink, spell.lstline)
        else:
            lst = "add"
            spell.lstline = "%s\t\tSOURCELINK:%s" % (spell.lstline, spell.sourcelink)

        return {
            "match": candidate,
            "certainty": certainty,
            "method": method,
            "lst": lst,
        }

    def test(self, collection):
        result = []

        for spell in collection:
            error = self.testlink(spell)

            if error:
                result.append((spell, error))

        return result

    def testlink(self, spell):

        if spell.sourcelink is None:
            return "Missing SOURCELINK"

        result = urlparse(spell.sourcelink)
        if result.scheme and result.netloc and result.path:
            return False

        # Missing or invalid link
        return "URL is not a valid HTTP link"