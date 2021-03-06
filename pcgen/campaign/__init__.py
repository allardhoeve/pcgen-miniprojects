from __future__ import absolute_import
from django.conf import settings
from unipath import Path
from pcgen.parser import read_lst_file, parse_feats


class Campaign(object):

    name = None
    root = None
    pcc = None

    def find_feat_listfiles(self, pcc=None):
        return self.find_listfiles("FEAT", pcc=pcc)

    def fetch_all_feats(self):
        listfiles = self.find_feat_listfiles()
        objects = []

        for (lst, source) in listfiles:
            objects = objects + parse_feats(lst, source)

        return objects

    def find_spell_listfiles(self, pcc=None):
        return self.find_listfiles("SPELL", pcc=pcc)

    def find_listfiles(self, filetype, pcc=None):
        files = []

        if not pcc:
            pcc = self.pcc

        (entries, source) = read_lst_file(pcc)

        for line in entries:
            elements = line.split(":", 1)
            type = elements[0]
            data = elements[1].rstrip()

            # PRE attributes on the .lst file
            if data.find("|") >= 0:
                elements = data.split("|", 1)
                data = elements[0]

            if type == filetype:
                files.append((pcc.parent.child(data), source))

            if type == "PCC":
                # relative paths start with @/
                if data.startswith("@/"):
                    pccpath = Path(settings.DATADIR, data[2:])
                else:
                    pccpath = Path(pcc.parent, data)

                pccfiles = self.find_listfiles(filetype, pccpath)
                files = files + pccfiles

        return files


class PathfinderCampaign(Campaign):

    def __init__(self):
        self.name = "pathfinder"
        self.root = Path(settings.DATADIR, "pathfinder/paizo")
        self.pcc = self.root.child("pathfinder_rpg_core.pcc")
