#! /bin/bash


set -ex

# TODO: use getopt here
ROCKCRAFT_DIR=$1
LC_CREADENTIALS_B64=$2

cd "$ROCKCRAFT_DIR"
rocks_toolbox="$(mktemp -d)"

git clone --depth 1 --branch v1.1.2 https://github.com/canonical/rocks-toolbox $rocks_toolbox
${rocks_toolbox}/rockcraft_lpci_build/requirements.sh
pip3 install -r ${rocks_toolbox}/rockcraft_lpci_build/requirements.txt

python3 ${rocks_toolbox}/rockcraft_lpci_build/rockcraft_lpci_build.py \
    --lp-credentials-b64 "$LC_CREADENTIALS_B64}" \
    --launchpad-accept-public-upload