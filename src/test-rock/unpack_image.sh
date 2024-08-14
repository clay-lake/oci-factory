#! /bin/bash


set -e


function usage(){
    echo
    echo "$(basename "$0") -i <image name>[:<image tag>]"
    echo
    echo "Unpack local image"
    echo
    echo -e "-i \\t docker image to unpack. "
}

while getopts "i:" opt
do
    case $opt in
        d)
            IMAGE="$OPTARG"
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done

if [ -z "$IMAGE" ]
then
    echo "Error: Missing image argument (-i)"
    usage
    exit 1
fi

sudo umoci unpack --keep-dirlinks --image $IMAGE bundle

# umoci list --layout $IMAGE

# python3 ${rocks_toolbox}/rockcraft_lpci_build/rockcraft_lpci_build.py \
#     --lp-credentials-b64 "$LC_CREDENTIALS_B64" \
#     --launchpad-accept-public-upload
    