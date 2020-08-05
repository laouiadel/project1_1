#!/bin/bash

head -37 docker-compose-base-origine.yaml > docker-compose-base.yaml

PORT1=7051
PORT2=8051
VAL=`expr $1 - 1`
k=1
PORT3=9443
#TYPE=ORDERER
for i in `seq 0 $VAL`;
do
		
	echo "  peer$i.org1.dz:
    container_name: peer$i.org1.dz
    image: hyperledger/fabric-peer
    environment:
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=\${COMPOSE_PROJECT_NAME}_MyNetwork 
      - CORE_PEER_ID=peer$i.org1.dz
      - CORE_PEER_ADDRESS=peer$i.org1.dz:$PORT1
      - CORE_PEER_LISTENADDRESS=0.0.0.0:$PORT1
      - CORE_PEER_CHAINCODEADDRESS=peer$i.org1.dz:`expr $PORT1 + 1`
      - CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:`expr $PORT1 + 1`
      - CORE_PEER_GOSSIP_BOOTSTRAP=peer$k.org1.dz:$PORT2
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer$i.org1.dz:$PORT1
      - CORE_PEER_LOCALMSPID=PeerOrg1MSP
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_GOSSIP_USELEADERELECTION=true
      - CORE_PEER_GOSSIP_ORGLEADER=false
      - CORE_OPERATIONS_LISTENADDRESS=0.0.0.0:$PORT3  # operation RESTful API
      - CORE_METRICS_PROVIDER=prometheus  # prometheus will pull metrics from orderer/peer via /metric
      # - CORE_PEER_PROFILE_ENABLED=true
      - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt
    working_dir: /opt/working-dir/src/hyperledger/fabric/peer

    volumes:
        - /var/run/:/host/var/run/
        - ../shared-folder:/etc/shared-folder
        - ../crypto-config/peerOrganizations/org1.dz/peers/peer$i.org1.dz/msp:/etc/hyperledger/fabric/msp
        - ../crypto-config/peerOrganizations/org1.dz/peers/peer$i.org1.dz/tls:/etc/hyperledger/fabric/tls
        # - peer$i.org1.dz:/var/hyperledger/production
    ports:
      - $PORT1:$PORT1
      - $PORT3:$PORT3
    command: peer node start" >> docker-compose-base.yaml
	PORT1=`expr $PORT1 + 1000`
	PORT2=7051
	k=0
	PORT3=`expr $PORT3 + 1`
	#TYPE=CORE
done







