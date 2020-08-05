#!/bin/bash


mv "/home/Adel/go/src/chaincodes/test_cc2.go" "/home/Adel/go/src/"
mv "/home/Adel/go/src/first_chaincode.go" "/home/Adel/go/src/chaincodes/"

files=( create_join install_cc instantiate_cc install_cc2 instantiate_cc2 invoke )

cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/fabric-sdk-py

for i in "${files[@]}"
do
if [ $i = install_cc2 ]
then
	cd /home/Adel/go/src/chaincodes
	mv "/home/Adel/go/src/chaincodes/first_chaincode.go" "/home/Adel/go/src/"
	mv "/home/Adel/go/src/test_cc2.go" "/home/Adel/go/src/chaincodes/"
        cd /home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/fabric-sdk-py
fi

	python ${i}.py &
	BACK_PID=$!
	wait $BACK_PID
done

