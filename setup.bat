docker build -t liroygenkins/test-task:v1 .
docker network create searcher-net
docker run -d --name es --net searcher-net -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -t docker.elastic.co/elasticsearch/elasticsearch:7.17.7
docker run -d --net searcher-net -p 8000:8000 --name app -t liroygenkins/test-task:v1
pause