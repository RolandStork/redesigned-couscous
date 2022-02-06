#!/bin/bash
container='redesigned-couscous'
docker container stop $container 
docker container rm $container
docker run --name=$container -t -d $container:latest 
