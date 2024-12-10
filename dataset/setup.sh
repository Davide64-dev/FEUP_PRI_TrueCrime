sudo docker rm meic_solr
sudo docker rm -f meic_solr

sudo docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate true_crime
sudo docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d \
-e SOLR_OPTS="-Dsolr.cors.enabled=true -Dsolr.cors.allow-origin=* -Dsolr.cors.allow-methods=GET,POST,PUT,DELETE -Dsolr.cors.allow-headers=Content-Type,Authorization" \
solr:9 solr-precreate true_crime

sleep 5

curl -X POST -H 'Content-type:application/json' \
--data-binary "@schema.json" \
http://localhost:8983/solr/true_crime/schema

sudo docker exec -it meic_solr bin/post -c true_crime /data/true_crime_flattened.json
sudo docker exec -it meic_solr bin/solr post -c true_crime /data/true_crime_flattened.json
