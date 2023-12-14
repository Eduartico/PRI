#!/bin/bash

# This script expects a container started with the following command.
# docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9.3 solr-precreate movies

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./semantic_schema.json" \
    http://localhost:8983/solr/movies/schema

# Populate collection using mapped path inside container.
curl -X POST -H 'Content-type:application/json' \
--data-binary "@./semantic_movies.json" \
http://localhost:8983/solr/movies/update?commit=true

