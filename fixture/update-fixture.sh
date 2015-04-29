#!/bin/bash

set -e

cd $(dirname $0)
wget 'http://paizo.com/pathfinderRPG/prd/indices/spells.html' -O spells.html
wget 'http://paizo.com/pathfinderRPG/prd/indices/feats.html' -O feats.html
