#!/bin/bash

# build the app container
docker build -t liroygenkins/test-task:v1 .

# create the network
docker network create searcher-net

# start the ES container
docker run -d --name es --net searcher-net -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:7.17.7

# start the app container
docker run -d --net searcher-net -p 8000:8000 --name app liroygenkins/test-task:v1