sudo docker rm -f meic_solr

sudo docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate true_crime

sleep 5

curl http://localhost:8983/solr/true_crime/config -d '{"set-user-property": {"update.autoCreateFields":"false"}}'

curl -X POST -H 'Content-type:application/json' \
--data-binary "@schema_fixed.json" \
http://localhost:8983/solr/true_crime/schema

sudo docker exec -it meic_solr bin/solr post -c true_crime /data/true_crime_semantics_with_id.json
#sudo docker exec -it meic_solr bin/solr post -c true_crime data/true_crime_flattened.json
