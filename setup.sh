#!/bin/bash

# build the app container
docker build -t ... .

# create the network
docker network create searcher-net

# start the ES container
docker run -d --name es --net searcher-net -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2

# start the app container
docker run -d --net searcher-net -p 5000:5000 --name searcher-service ...