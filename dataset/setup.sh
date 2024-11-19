sudo docker rm meic_solr

sudo docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate true_crime

# sudo docker exec -it meic_solr bin/post -c true_crime /data/true_crime_flattened.json

curl -X POST -H 'Content-type:application/json' \
--data-binary "@schema.json" \
http://localhost:8983/solr/true_crime/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@true_crime_flattened.json" \
http://localhost:8983/solr/true_crime/update?commit=true

