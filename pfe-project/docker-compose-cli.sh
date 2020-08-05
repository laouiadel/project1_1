#!/bin/bash

head -16 docker-compose-cli-origine.yaml > docker-compose-cli.yaml

VAL=`expr $1 - 1`
for i in `seq 0 $VAL`;
do
  echo "  peer$i.org1.dz:
    container_name: peer$i.org1.dz
    extends:
      file:  base/docker-compose-base.yaml
      service: peer$i.org1.dz
    networks:
      - MyNetwork" >> docker-compose-cli.yaml

done
