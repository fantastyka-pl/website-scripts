.ONESHELL:
.PHONY: $(MAKECMDGOALS)
SHELL = /bin/bash

ROOT = $(shell pwd -P)

NAME = calculate_commenters-env
VER = latest
IMAGE = ${NAME}:${VER}

build:
	docker buildx build -f ${ROOT}/Dockerfile --rm -t ${IMAGE} .
