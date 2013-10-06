from urlparse import urlparse


class QASpellSourceWeb(object):

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