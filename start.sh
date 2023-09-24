#! /bin/bash
docker run -it \
    --rm \
    --net="host"\
    --name="documentation_wiki"\
    --env-file .env\
    -v .:/documentation_wiki \
    jhpiedrahitao/document_wiki:latest
