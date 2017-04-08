#!/bin/sh

rules_directory=${RULES_FOLDER:-/opt/elastalert/examples_rules}
es_port=${ELASTICSEARCH_PORT:-9200}

# Render rules files
for file in $(find . -name 'config.yaml' -or -name 'config.yml');
do
    cat $file | sed "s|es_host: [[:print:]]*|es_host: ${ELASTICSEARCH_HOST}|g" | sed "s|es_port: [[:print:]]*|es_port: $es_port|g" | sed "s|rules_folder: [[:print:]]*|rules_folder: $rules_directory|g" > config
    cat config > $file
    rm config
done

echo "Creating Elastalert index in Elasticsearch..."
elastalert-create-index --index elastalert_status --old-index "" --no-auth;

exec "$@"