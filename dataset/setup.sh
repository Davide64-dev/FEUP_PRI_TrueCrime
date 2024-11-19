sudo docker rm meic_solr

sudo docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate true_crime

sudo docker exec -it meic_solr bin/post -c true_crime /data/true_crime_flattened.json

