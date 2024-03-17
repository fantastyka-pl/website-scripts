#!/usr/bin/env bash

CWD="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

IMAGE_NAME=$(grep -m 1 NAME "$CWD/Makefile" | sed 's/^.*= //g')
IMAGE_VERSION=$(grep -m 1 VER "$CWD/Makefile" | sed 's/^.*= //g')

IMAGE="$IMAGE_NAME:$IMAGE_VERSION"

docker run -it --rm --user="$(id -u)" --name "social-graph-generator-env" -v "$CWD:/app" -w "/app" -e "MPLCONFIGDIR=/tmp" "$IMAGE" "./run.sh" "$@"
