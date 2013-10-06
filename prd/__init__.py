from io import StringIO
from lxml import etree
import requests


def get_prd_spell_links():
    index = requests.get("http://paizo.com/pathfinderRPG/prd/indices/spells.html")
    root = etree.HTML(index)
    links = root.xpath("//div[@id='spell-index-wrapper']/ul/li/a")

    ret = {}

    for link in links:
        name = link.text
        url = "http://paizo.com" + link.attrib['href']
        ret[name] = url

    return ret