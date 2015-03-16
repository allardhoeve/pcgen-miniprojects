from defusedxml import lxml
from pcgen import settings


with open(settings.PROJECTROOT.child("Saenvan level 12.xml")) as file:
    xml = file.read()

root = lxml.fromstring(xml)

for klass in root.xpath('//known_spells/class'):
    for level in klass.xpath('level'):
        if level.attrib['cast'] != '0':
            print "%s level %s, %s per day" % (klass.attrib['spelllistclass'], level.attrib['number'], level.attrib['cast'])
