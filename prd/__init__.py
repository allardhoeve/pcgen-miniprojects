import re
from lxml import etree
import requests
from prd.dict import CaseInsensitiveDict


def get_prd_feat_links(html=None):
    if not html:
        html = fetch_prd_feat_index()

    # Clean (Combat, Teamwork) from the feat name
    def clean_feat_name(name, link):
        name = re.sub(r'\s+\([^)]+\)$', '', name)
        return name, link

    # yes, really, spell :(
    return get_prd_object_links(html, "spell", "Feats", filter=clean_feat_name)


def get_prd_spell_links(html=None):

    if not html:
        html = fetch_prd_spell_index()

    return get_prd_object_links(html, "spell", "Spells")


def get_prd_object_links(html, type, header, filter=None):
    root = etree.HTML(html)
    links = root.xpath("//div[@id='%s-index-wrapper']/ul/li/a" % type)

    ret = CaseInsensitiveDict()

    for link in links:
        name = link.text.strip()

        # skip all index links
        if re.match(r"^[A-Z] %s$" % header, name):
            continue

        url = "http://paizo.com" + link.attrib['href']

        if filter:
            name, url = filter(name, url)

        ret[name] = url

    return ret


def fetch_prd_feat_index():
    index = requests.get("http://paizo.com/pathfinderRPG/prd/indices/feats.html")
    return index


def fetch_prd_spell_index():
    index = requests.get("http://paizo.com/pathfinderRPG/prd/indices/spells.html")
    return index