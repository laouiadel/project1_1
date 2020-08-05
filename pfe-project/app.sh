#!/bin/bash

### Default values:
DFLT_crypto_config_file="crypto-config.yaml" # it is used to create the certificats, the architecture is found in this file
DFLT_crypto_config_folder="crypto-config" #this is where the certificats are stored
DFLT_OrdererGenesisFolder=./channel-artifacts # this where the genesis block is found
DFLT_ChannelFolder=./channel-artifacts  # default channel for the artifacts(channels artifacts, genesis block) (look configtx.yaml)
DFLT_FirstChannelId=firstchannel # the default channel id for the first blockchain #must be lowercase
DFLT_SecondChannelId=secondschannel        # the default channel id for the second blockchain  #must be lowercase
DFLT_OrdererGenesisProfile=FirstOrdererGenesis  #default profile to create the genesis block (look configtx.yaml)
DFLT_FirstChannelProfile=firstchannel #default profile to create the first channel  (look configtx.yaml)
DFLT_SecondChannelProfile=secondchannel         #default profile to create the second channel  (look configtx.yaml)

DFLT_GenerateGenesisBlock=true              #We used the same function to create the different artifacts, that is why we have a boolean value to specify if we create or not the genesis block
DFLT_GenesisForSpecificChannel=false    # used in function 'GenerateArtifacts', true means we generate a genesis block for a specific channel.
DFLT_message="Execute Step??? (y/n)" # default message to show before each step
DFLT_docker_compose_file="docker-compose-cli.yaml" # The docker comopose file to use to generate the containers.

PROJECT_NAME=net
export COMPOSE_PROJECT_NAME=net
function usage {
    echo 'My fabric app :' 
    echo 'usage: app <action>'
    echo '<action> could be:'
    echo '      "generate"  : to generate the crypto material, channels...'
    echo '      "up"        : to bring up the network'
    echo '      "down"      : to shutdown the network and remove the containers'
    echo '      "clean"     : to remove the file and folders created using the script(app)'
    echo '      "help"      : show this help message'
    echo ''
    echo 'Proper use:'
    echo '  app generate '
    echo '  app up '
    echo '  app down '
    echo '  app clean '
}


function NextStepYN()
{
    # Usage: NextStepYN [message]
    # Parametres:
    # $1==>message:default message to show before each step.
    message=$1
    echo $message
    read rep
    if [ $rep = "n" ]
    then
	exit -2
    fi
    
}

function GenerateCerts()
{
    # This functions is used to create the certificats for the different entities.
    # Usage: GenerateCerts [crypto_config_file] [crypto_config_folder]
    # Parametres:
    crypto_config_file=$1   #(look #Default values) it is used to create the certificats, the architecture is found in this file.
    crypto_config_folder=$2 #(look #Default values) this is where the certificats are stored.
    
    echo "-----------------STEP: GENERATE CERTFICATS, START--------------------"
    echo "Using the 'cryptogen' tool to generate certificats..."
    if test -d $crypto_config_folder
    then
	echo "Crypto folder exists, deleting folder"
	rm -r $crypto_config_folder
    fi
    
    cryptogen generate --config=$crypto_config_file --output=$crypto_config_folder 

    if [ $? -ne 0 ] # Verifying if the execution is a success
    then
	echo "Failed to create Certificats, quiting"
	exit -1
    fi

    echo "Certificats generated successfully."
    echo "-----------------STEP: GENERATE CERTIFICATS, END--------------------"
    
}

function GenerateArtifacts()
{
    # This function is used the create the different artifacts for our networks: channels artifacts and the genesis block, the profiles and definition of the organisations... are found in the file 'configtx.yaml'.
    #####################
    # the function has six parametres:
    OrdererGenesisFolder=$1  #(look #Default values), this where the genesis block is found.
    ChannelFolder=$2         #(look #Default values), folder of the artifacts(channels artifacts, genesis block) (look configtx.yaml).
    ChannelId=$3             # the channel id,(we can say the blockchain id), there is two defaults values:
    #      -SecondChannelId=(look #Default values), the channel id of the second blockchain.
    #      -FirstChannelId=(look #Default values), the channel id of the first blockchain.
    OrdererGenesisProfile=$4 #(look #Default values), the profile used to create the genesis block (look configtx.yaml)
    ChannelProfile=$5        # the profile used to create the channels,there is two defaults values:
    #     -FirstChannelProfile=(look #Default values), the profile used to create the first channel  (look configtx.yaml)
    #     -SecondChannelProfile=SecondChannel, the profile used to create the second channel  (look configtx.yaml)
    GenerateGenesisBlock=$6 #(look #Default values)  #We used the same function to create the different artifacts, that is why we have a boolean value to specify if we create or not the genesis block
    GenesisForSpecificChannel=$7    #(look #Default values), true means we the '-channelID' flage (i.e generate a genesis block for a specific channel).
    
    echo "-----------------STEP: GENERATE ARTIFACTS(CHANNELS AND ORDERER GENESIS BLOCK), START--------------------"
    echo "Using the 'configtxgen' tool to generate artifacts..."

    if [ "$GenerateGenesisBlock" = "true" ] # this can be replaced with ( if $GenerateGenesisBlockBool)
    then	    	
	echo "-----------------(a) generate the orderer genesis block--------------------"

	#Creating the folder for the genesis Block if it does not exists
	if ! test -d $OrdererGenesisFolder
	then
	   mkdir -p $OrdererGenesisFolder
	fi
	#Removing the genesis Block if it exists
	if test -f $OrdererGenesisFolder/genesis.block
	then
	    rm  $OrdererGenesisFolder/genesis.block
	fi
	#Generating the genesis block

	if [ "$GenesisForSpecificChannel" = "true" ] # generate a genesis block of a specific channel??? if true then yes.
	then
	    
	    configtxgen -profile $OrdererGenesisProfile -channelID $ChannelId -outputBlock $OrdererGenesisFolder/genesis.block
	else
	    configtxgen -profile $OrdererGenesisProfile -outputBlock $OrdererGenesisFolder/genesis.block
	fi
	
	if [ $? -ne 0 ] # Verifying if the execution is a success
	then
	    echo "Failed to generate orderer genesis block, quiting"
	    exit -1
	fi
	echo "-(a) orderer genesis block generated successfully."
    fi


    echo "-----------------(b) generate channel artifact for : $ChannelId --------------------"
    #Creating the folder for the channel artifacts  if it does not exists
    if ! test -d $ChannelFolder
    then
	mkdir -p $ChannelFolder
    fi

    #Removing the channel file if it exists
    if test -f $ChannelFolder/$ChannelId
    then
	rm  $ChannelFolder/$ChannelId
    fi
    #Generating the channel artifacts
    configtxgen -profile $ChannelProfile -outputCreateChannelTx $ChannelFolder/$ChannelId.tx  -channelID $ChannelId 

    if [ $? -ne 0 ] # Verifying if the execution is a success
    then
	echo "Failed to generate channel artifact for $ChannelId , quiting"
	exit -1
    fi

    echo "(b) Channel artifact for $ChannelId generated successfully."
    echo "Artificats generated successfully."
    echo "-----------------STEP: GENERATE ARTIFACTS(CHANNELS AND ORDERER GENESIS BLOCK), END--------------------"

    }



function StartNetwork()
{   # This function generate the containers and start the network of our architecture: orederer and peer nodes
    # Parametres:
    # $1= the docker compose file
    docker_compose_file=$1 # (look #Default values),  the docker comopose file to use to generate the containers
    
    docker-compose -f $docker_compose_file -p $PROJECT_NAME  up

    # echo "Sleeping for 10s, waiting for the network!!!"
    # sleep 10
    #
}

#this is the main function, to be deleted later, a main script to be used


function TearDown(){
    # This function shutdown and clean(remove containers) after the network.
    # Parametres:
    # $1= the docker compose file
    docker_compose_file=$1 # (look #Default values),  the docker comopose file to use to generate the containers

    echo "Shutting down the network..."
    docker-compose -f $docker_compose_file -p $PROJECT_NAME  down
    echo "Removing the containers..."
    docker rm $(docker ps -aq)
}

function CleanArtifacts(){
    # This function delete all the files and folders created with the application, ex: certificats.
    # Parametres:
    # $1= the crypto config folder
    # $2=the artifacts folder
    crypto_config_folder=$1 #(look #Default values) this is where the certificats are stored.
    ArtifactsFolder=$2         #(look #Default values), folder of the artifacts(channels artifacts, genesis block) (look configtx.yaml).
echo "Removing the artifacts folder::: $ArtifactsFolder."
rm -R $ArtifactsFolder
echo "Removing the crypto-config folder::: $crypto_config_folder."
    rm -R $crypto_config_folder
}



action=$1
shift
# what action to exectute, depends on the first parametre:
if [ "$action" == "up" ]; then
    StartNetwork   $DFLT_docker_compose_file
    exit 1
elif [ "$action" == "down" ]; then
    TearDown    $DFLT_docker_compose_file
    exit 1
elif [ "$action" == "clean" ]; then
    CleanArtifacts $DFLT_crypto_config_folder $DFLT_ChannelFolder
    exit 1
elif [ "$action" == "generate" ]; then
    GenerateCerts $DFLT_crypto_config_file $DFLT_crypto_config_folder
    GenerateArtifacts "$DFLT_OrdererGenesisFolder" "$DFLT_ChannelFolder/FirstChan" $DFLT_FirstChannelId $DFLT_OrdererGenesisProfile $DFLT_FirstChannelProfile "true" "false"
    GenerateArtifacts "$DFLT_OrdererGenesisFolder" "$DFLT_ChannelFolder/SecondChan" $DFLT_SecondChannelId $DFLT_OrdererGenesisProfile $DFLT_SecondChannelProfile "false" "false"
    exit 1

elif [ "$action" == "help" ]; then
    usage
    exit 1
else
  usage
  exit 1
fi

