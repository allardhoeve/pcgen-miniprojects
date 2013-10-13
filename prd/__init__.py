from lxml import etree
import requests
from prd.dict import CaseInsensitiveDict


def get_prd_spell_links(html=None):

    if not html:
        html = fetch_prd_spell_index()

    root = etree.HTML(html)
    links = root.xpath("//div[@id='spell-index-wrapper']/ul/li/a")

    ret = CaseInsensitiveDict()

    for link in links:
        name = link.text.strip()
        url = "http://paizo.com" + link.attrib['href']
        ret[name] = url

    return ret


def fetch_prd_spell_index():
    index = requests.get("http://paizo.com/pathfinderRPG/prd/indices/spells.html")
    return index