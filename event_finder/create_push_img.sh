#!/bin/bash

aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 654654516734.dkr.ecr.eu-west-2.amazonaws.com
docker build -t event-finder .
docker tag event-finder:latest 654654516734.dkr.ecr.eu-west-2.amazonaws.com/event-finder:latest