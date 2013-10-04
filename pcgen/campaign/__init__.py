from unipath import Path
from pcgen import settings


class Campaign(object):

    name = None
    root = None
    pcc = None

    def find_spell_files(self, pcc):
        spell_files = []

        with open(pcc) as pccfh:
            pccdata = pccfh.read()

            for line in pccdata.split("\n"):
                elements = line.split(":", 1)

                if len(elements) != 2:  # skip line if there was no colon
                    continue

                type = elements[0]
                data = elements[1]

                if type == "SPELL":
                    spell_files.append(pcc.parent.child(data))

                if type == "PCC":
                    # recurse through te new PCC
                    # remove "@/" from string
                    if data.startswith("@/"):
                        data = data[2:]

                    pccpath = Path(pcc.parent, data)
                    pccspells = self.find_spell_files(pccpath)
                    spell_files = spell_files + pccspells

        return spell_files


class PathfinderCampaign(Campaign):

    def __init__(self):

        self.name = "pathfinder"
        self.root = settings.DATADIR
        self.pcc = self.root.child("pathfinder_rpg_complete.pcc")
