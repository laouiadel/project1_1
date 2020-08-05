#!/bin/bash

read -p "Enter the number of users, and peers respectivly" USERS PEERSS

head -n 23  MyNetwork-origine.json > MyNetwork.json

cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/ordererOrganizations/org1.dz/users/Admin@org1.dz/msp/keystore
fileKeyAdminOrderer=$(ls)
#echo "$fileKeyAdminOrderer"
cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk

echo "          \"private_key\": \"/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/ordererOrganizations/org1.dz/users/Admin@org1.dz/msp/keystore/$fileKeyAdminOrderer\"" >> MyNetwork.json

awk 'FNR>=25 && FNR<=30'  MyNetwork-origine.json >> MyNetwork.json

VAL=`expr $PEERSS - 1`
PEERS=""
for i in `seq 0 $VAL`;
do
	PEER="\"peer$i.org1.dz\","
	PEERS=$PEERS$PEER	
#	echo $PEERS
done
	echo "[${PEERS%?}]," >> MyNetwork.json

awk 'FNR>=32 && FNR<=36'  MyNetwork-origine.json >> MyNetwork.json

cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/peerOrganizations/org1.dz/users/Admin@org1.dz/msp/keystore
fileKeyAdminOrderer=$(ls)
cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk

echo "        \"Admin\": {
	        \"cert\": \"/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/peerOrganizations/org1.dz/users/Admin@org1.dz/msp/signcerts/Admin@org1.dz-cert.pem\",
		\"private_key\": \"/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/peerOrganizations/org1.dz/users/Admin@org1.dz/msp/keystore/$fileKeyAdminOrderer\"
		}," >> MyNetwork.json


for i in `seq 1 $USERS`;
do
	cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/peerOrganizations/org1.dz/users/User$i@org1.dz/msp/keystore
	file=$(ls)
	cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk
 	x="        \"User$i\": {
                     \"cert\": \"/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/peerOrganizations/org1.dz/users/User$i@org1.dz/msp/signcerts/User$i@org1.dz-cert.pem\",
		     \"private_key\": \"/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/peerOrganizations/org1.dz/users/User$i@org1.dz/msp/keystore/$file\"
		},"
	if [ $i == $USERS ]
	then	
		echo "${x%?}" >> MyNetwork.json
	else
		echo "$x" >> MyNetwork.json
	fi
done

echo "} 
} 
}," >> MyNetwork.json


awk 'FNR>=85 && FNR<=97'  MyNetwork-origine.json >> MyNetwork.json

PORT=7051

for i in `seq 0 $VAL`;
do
	y="    \"peer$i.org1.dz\": {
	      \"url\": \"localhost:$PORT\",
	      \"eventUrl\": \"localhost:`expr $PORT + 2`\",
	      \"grpcOptions\": {
      	        \"grpc.ssl_target_name_override\": \"peer$i.org1.dz\",
	        \"grpc.http2.keepalive_time\": 15
	      },
	      \"tlsCACerts\": {
	        \"path\": \"/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/crypto-config/peerOrganizations/org1.dz/peers/peer$i.org1.dz/msp/tlscacerts/tlsca.org1.dz-cert.pem\"
}},"

	if [ $i == $VAL ]
	then
		echo "${y%?}" >> MyNetwork.json
	else
		echo "$y" >> MyNetwork.json
	fi
	
	
	PORT=`expr $PORT + 1000`
done


tail -n 20  MyNetwork-origine.json >> MyNetwork.json
