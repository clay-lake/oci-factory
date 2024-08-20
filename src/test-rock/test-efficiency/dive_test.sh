#! /bin/bash


set -e

DIVE_IMAGE='wagoodman/dive:v0.12'

function usage(){
    echo
    echo "$(basename "$0") -d <image>[:<tag>] -c <dive configuration YAML>"
    echo
    echo "Test Image efficiency with dive"
    echo
    echo -e "-d \\t Docker image to test. "
    echo -e "-c \\t Dive configuration file. "
    echo -e "-o \\t Test results output path (optional). "
}

while getopts "c:d:o:" opt
do
    case $opt in
        d)
            DOCKER_IMAGE="$OPTARG"
            ;;
        c)
            DIVE_CONFIG="$(realpath "$OPTARG")"
            ;;
        o)
            TEST_RESULTS="$OPTARG"
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done

if [ -z "$DOCKER_IMAGE" ]
then
    echo "Error: Missing docker image (-d)"
    usage
    exit 1
fi

if [ -z "$DIVE_CONFIG" ]
then
    echo "Error: Missing dive config (-c)"
    usage
    exit 1
fi

docker run -e CI=true --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$DIVE_CONFIG":/dive-ci.yaml \
    $DIVE_IMAGE $DOCKER_IMAGE --ci-config /dive-ci.yaml \
    | tail -n +1 | tee $TEST_RESULTS

