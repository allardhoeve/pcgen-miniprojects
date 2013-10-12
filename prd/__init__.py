from lxml import etree
import requests


def get_prd_spell_links(html=None):

    if not html:
        html = fetch_prd_spell_index()

    root = etree.HTML(html)
    links = root.xpath("//div[@id='spell-index-wrapper']/ul/li/a")

    ret = {}

    for link in links:
        name = link.text
        url = "http://paizo.com" + link.attrib['href']
        ret[name] = url

    return ret


def fetch_prd_spell_index():
    index = requests.get("http://paizo.com/pathfinderRPG/prd/indices/spells.html")
    return index