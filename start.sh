#! /bin/bash
docker run -it \
    --rm \
    --net="host"\
    -v $PWD:/documentation-wiki \
    --name="documentation_wiki"\
    --env-file .env\
    jhpiedrahitao/document_wiki:latest
