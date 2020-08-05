# for more information look fabric-samples/first-network/scripts
ORDERER1_ROOT_CF="/opt/working-dir/src/hyperledger/fabric/peer/crypto/ordererOrganizations/org1.dz/orderers/orderer1.org1.dz/msp/tlscacerts/tlsca.org1.dz-cert.pem"
ORDERER1_ADDRESS=orderer1.org1.dz:7050

# CORE_PEER_TLS_ROOTCERT_FILE of the peers
PEER0_ROOT_CF="/opt/working-dir/src/hyperledger/fabric/peer/crypto/peerOrganizations/org1.dz/peers/peer0.org1.dz/tls/ca.crt"
PEER1_ROOT_CF="/opt/working-dir/src/hyperledger/fabric/peer/crypto/peerOrganizations/org1.dz/peers/peer1.org1.dz/tls/ca.crt"
PEER2_ROOT_CF="/opt/working-dir/src/hyperledger/fabric/peer/crypto/peerOrganizations/org1.dz/peers/peer2.org1.dz/tls/ca.crt"

# CORE_PEER_ADDRESS of the peers
PEER0_ADDRESS=peer0.org1.dz:7051
PEER1_ADDRESS=peer1.org1.dz:8051
PEER2_ADDRESS=peer2.org1.dz:9051

# ADMIN certificat !!!??? i forgot!!!!
DFLT_CORE_PEER_MSPCONFIGPATH=/opt/working-dir/src/hyperledger/fabric/peer/crypto/peerOrganizations/org1.dz/users/Admin@org1.dz/msp

# organisation mspid
DFLT_CORE_PEER_LOCALMSPID=PeerOrg1MSP

# Other DEFAULT VALUES:
FIRST_CHANNEL_ARTIFACTS=channel-artifacts/FirstChan/firstchannel.tx #path the artifacts of the first channel
SECOND_CHANNEL_ARTIFACTS=channel-artifacts/SecondChan/secondchannel.tx #path the artifacts of the second channel
DFLT_FIRST_CHAINCODE_NAME=firstcc # the name of the first channel chaincode.
DFLT_SECOND_CHAINCODE_NAME=secondcc # the name of the second channel chaincode.
DFLT_FIRST_CHAINCODE_PATH=chaincode/firstcc # the path to the first channel chaincode.
DFLT_SECOND_CHAINCODE_PATH=chaincode/secondcc # the path to the second channel chaincode.
DFLT_CHAINCODE_VERSION=1.0 # version of the chaincode
########################
# Constructor message for the chaincode in JSON format (default "{}")
DFLT_FIRST_CONSTRUCTOR_MESSAGE='{"Args":[]}'   # Constructor message for the first channel 
DFLT_SECOND_CONSTRUCTOR_MESSAGE='{"Args":[]}' # Constructor message for the second channel
#######################
DFLT_FIRST_CHANNEL_BLOCK=firstchannel.block
DFLT_SECOND_CHANNEL_BLOCK=secondchannel.block
DFLT_FIRST_CHANNEL_NAME=firstchannel
DFLT_SECOND_CHANNEL_NAME=secondchannel



# Exported variables
export CHANNEL_NAME=" " # we will use it later

function CreateChannel() {
    # Create a channel using cli???, parametres:
    # $1==> the orderer address
    # $2==> the channel name
    # $3==> the path to the channel artifacts
    # $4==> the orderer certificat

    ORDERER_ADDRESS=$1
    CHANNEL_NAME=$2
    CHANNEL_ARTIFACTS=$3
    ORDERER_CERTIFICAT=$4
    
 peer channel create -o $ORDERER_ADDRESS -c $CHANNEL_NAME -f $CHANNEL_ARTIFACTS  --tls --cafile $ORDERER_CERTIFICAT
}

function JoinPeer(){
    # join a peer to a channel
    # $1=CORE_PEER_MSPCONFIGPATH
    # $2=CORE_PEER_TLS_ROOTCERT_FILE
    # $3=CORE_PEER_ADDRESS
    # $4=CORE_PEER_LOCALMSPID
    # $5=channel block !!!
    
    CORE_PEER_MSPCONFIGPATH=$1 
    CORE_PEER_TLS_ROOTCERT_FILE=$2 
    CORE_PEER_ADDRESS=$3
    CORE_PEER_LOCALMSPID=$4 # PeerOrg1MSP
    CHANNEL_BLOCK=$5

    peer channel join -b  $CHANNEL_BLOCK 

    }

function InstallChaincode() {
    # Install the chaincode in peer, parameters:
    # $1=chaincode name.
    # $2=chaincode version
    # $3=path to the chaincode
    # $4=CORE_PEER_TLS_ROOTCERT_FILE
    # $5=CORE_PEER_ADDRESS

    CHAINCODE_NAME=$1
    CHAINCODE_VERSION=$2
    CHAINCODE_PATH=$3
    CORE_PEER_TLS_ROOTCERT_FILE=$4
    CORE_PEER_ADDRESS=$5



peer chaincode install -n $CHAINCODE_NAME -v $CHAINCODE_VERSION -p $CHAINCODE_PATH

}
function InstantiateChaincode() {
    # Parametres:
    # $1=channel name
    # $2=Orderer address
    # $3=orderer certificat
    # $4=chaincode name
    # $5=chaincode varsion
    # $6=Constructor message for the chaincode in JSON format (default "{}")

    CHANNEL_NAME=$1
    ORDERER_ADDRESS=$2
    ORDERER_CF=$3
    CHAINCODE_NAME=$4
    CHAINCODE_VERSION=$5
    CONSTRUCTOR_MESSAGE=$6

peer chaincode instantiate -o $ORDERER_ADDRESS --tls --cafile $ORDERER_CF -C $CHANNEL_NAME -n $CHAINCODE_NAME -v $CHAINCODE_VERSION -c "$CONSTRUCTOR_MESSAGE"
}


# function QueryChaincode(){
# }
function InvokeChaincode(){


    ORDERER_ADDRESS=$1
    ORDERER_CF=$2
    CHANNEL_NAME=$3
    CHAINCODE_NAME=$4
peer chaincode invoke -o $ORDERER_ADDRESS --tls true --cafile $ORDERER_CF -C $CHANNEL_NAME -n $CHAINCODE_NAME --peerAddresses  $PEER0_ADDRESS --tlsRootCertFiles $PEER0_ROOT_CF  --peerAddresses  $PEER1_ADDRESS --tlsRootCertFiles $PEER1_ROOT_CF --peerAddresses  $PEER2_ADDRESS --tlsRootCertFiles $PEER2_ROOT_CF -c $INVOKE_MESSAGE
}


###########################################################
# START
#########################
# Creating the two channels
export CHANNEL_NAME=" "
## first channel
echo "Creating the first channel"
CreateChannel $ORDERER1_ADDRESS $DFLT_FIRST_CHANNEL_NAME $FIRST_CHANNEL_ARTIFACTS $ORDERER1_ROOT_CF

## second channel
echo "Creating the second channel"
CreateChannel $ORDERER1_ADDRESS $DFLT_SECOND_CHANNEL_NAME $SECOND_CHANNEL_ARTIFACTS $ORDERER1_ROOT_CF

# JoinPeer
## first channel
### peer0
echo "Join peer0 to the first channel"
JoinPeer  $DFLT_CORE_PEER_MSPCONFIGPATH  $PEER0_ROOT_CF $PEER0_ADDRESS $DFLT_CORE_PEER_LOCALMSPID $DFLT_FIRST_CHANNEL_BLOCK
### peer1
echo "Join peer1 to the first channel"
JoinPeer  $DFLT_CORE_PEER_MSPCONFIGPATH  $PEER1_ROOT_CF $PEER1_ADDRESS $DFLT_CORE_PEER_LOCALMSPID $DFLT_FIRST_CHANNEL_BLOCK
### peer2
echo "Join peer2 to the first channel"
JoinPeer  $DFLT_CORE_PEER_MSPCONFIGPATH  $PEER2_ROOT_CF $PEER2_ADDRESS $DFLT_CORE_PEER_LOCALMSPID $DFLT_FIRST_CHANNEL_BLOCK

echo -e "\n-------------------------------------"
echo "-------------------------------------\n"

## second channel
### peer0
echo "Join peer0 to the second channel"
JoinPeer  $DFLT_CORE_PEER_MSPCONFIGPATH  $PEER0_ROOT_CF $PEER0_ADDRESS $DFLT_CORE_PEER_LOCALMSPID $DFLT_SECOND_CHANNEL_BLOCK
### peer1
echo "Join peer1 to the second channel"
JoinPeer  $DFLT_CORE_PEER_MSPCONFIGPATH  $PEER1_ROOT_CF $PEER1_ADDRESS $DFLT_CORE_PEER_LOCALMSPID $DFLT_SECOND_CHANNEL_BLOCK
### peer2
echo "Join peer2 to the second channel"
JoinPeer  $DFLT_CORE_PEER_MSPCONFIGPATH  $PEER2_ROOT_CF $PEER2_ADDRESS $DFLT_CORE_PEER_LOCALMSPID $DFLT_SECOND_CHANNEL_BLOCK

echo -e "\n-------------------------------------"
echo "-------------------------------------\n"

# InstallChaincode
## peer0
echo "Install the chaincodes in peer0"
InstallChaincode $DFLT_FIRST_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_FIRST_CHAINCODE_PATH $PEER0_ROOT_CF $PEER0_ADDRESS
InstallChaincode $DFLT_SECOND_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_SECOND_CHAINCODE_PATH $PEER0_ROOT_CF $PEER0_ADDRESS
## peer1
echo "Install the chaincodes in peer0"
InstallChaincode $DFLT_SECOND_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_SECOND_CHAINCODE_PATH $PEER1_ROOT_CF $PEER1_ADDRESS
InstallChaincode $DFLT_FIRST_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_FIRST_CHAINCODE_PATH $PEER1_ROOT_CF $PEER1_ADDRESS
## peer2
echo "Install the chaincodes in peer0"
InstallChaincode $DFLT_FIRST_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_FIRST_CHAINCODE_PATH $PEER2_ROOT_CF $PEER2_ADDRESS
InstallChaincode $DFLT_SECOND_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_SECOND_CHAINCODE_PATH $PEER2_ROOT_CF $PEER2_ADDRESS

echo -e "\n-------------------------------------"
echo "-------------------------------------\n"

# InstantiateChaincode
## First channel
echo "Instantiating the Chaincode on the first channel "
InstantiateChaincode $DFLT_FIRST_CHANNEL_NAME $ORDERER1_ADDRESS $ORDERER1_ROOT_CF $DFLT_FIRST_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_FIRST_CONSTRUCTOR_MESSAGE
## Second Channel
echo "Instantiating the Chaincode on the second channel "
InstantiateChaincode $DFLT_SECOND_CHANNEL_NAME $ORDERER1_ADDRESS $ORDERER1_ROOT_CF $DFLT_SECOND_CHAINCODE_NAME $DFLT_CHAINCODE_VERSION $DFLT_SECOND_CONSTRUCTOR_MESSAGE

echo -e "\n-------------------------------------"
echo "-------------------------------------\n"













# peer chaincode invoke -o $ORDERER1_ADDRESS  --tls true --cafile $ORDERER1_ROOT_CF -C $DFLT_SECOND_CHANNEL_NAME -n $DFLT_SECOND_CHAINCODE_NAME --peerAddresses  $PEER0_ADDRESS --tlsRootCertFiles $PEER0_ROOT_CF  --peerAddresses  $PEER1_ADDRESS --tlsRootCertFiles $PEER1_ROOT_CF --peerAddresses  $PEER2_ADDRESS --tlsRootCertFiles $PEER2_ROOT_CF -c '{"Args":["NewData","data1","value1"]}' 

