#!/usr/bin/env bash

image=apluslms-aplus-json-generation

docker build --rm -t ${image} .

#docker tag ${image} qianqianq/${image}:latest
#docker push qianqianq/${image}:latest