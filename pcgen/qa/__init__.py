import re
from urlparse import urlparse
from pcgen import matcher


class QASourceLink(object):

    pattern = "(?<=SOURCELINK:)[^\t]+"

    def __init__(self):
        self.pattern = re.compile(self.pattern)

    def correct(self, obj, srdobjects, suggestions=None):
        """
        Autocorrect the sourcelink and lstline of an object if needed

        The object is fixed in-place. The field object.sourcelink is updated and
        object.lstline is updated. Invalid SOURCELINK: is fixed if not there.
        SOURCELINK:url is appended if missing.

        NB: The object to be updated should have object.name filled.

        Positional arguments:
          - object: LstObject to be corrected
          - srdobjects: a dict of known objects and their URL (prd.get_prd_*_links)
          - suggestions: a dict with two key-values containing dicts:
            - suggestions["links"]["Aid"] -> "http://pcgen.nl/aid.html"
            - suggestions["matcher"]["Aid (evil)"] -> "Aid"
            - this is optionally used to match objects that are normally missed so
              that the script can be run many times on the same data without intervention

        Returns:
          - False if object not updated
          - dict if object updated (can be tested against boolean operators as True):
            - method: "match" or "fuzzy"
            - match: matched object name
            - certainty: integer - how probable is the fuzzy match on scale 0-100
            - lst: "add" or "correct" to see how the SOURCELINK string was handled

        """
        # If the sourcelink tests ok, don't touch it
        if self.testlink(obj) is False:  # no errors
            return False

        query = obj.name

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
                srdobjects,
                suggestions=matcher_suggestions
            )

            # No match found
            if candidate is None:
                return False

            link = srdobjects[candidate]

        # Set the link we found
        obj.sourcelink = link

        # Add or correct SOURCELINK in lstline
        lst = None
        if self.pattern.search(obj.lstline):
            lst = "correct"
            obj.lstline = self.pattern.sub(obj.sourcelink, obj.lstline)
        else:
            lst = "add"
            obj.lstline = obj.lstline.rstrip()  # remove any trailing carriage returns
            obj.lstline = "%s\t\tSOURCELINK:%s" % (obj.lstline, obj.sourcelink)

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