# Look sdk-py docs for more info!!!
# use a python shell for your tests

from hfc.fabric import Client
import asyncio


loop = asyncio.get_event_loop()

cli = Client(
    net_profile="/*****************YOUR_PATH*****************/sdk/MyNetwork.json"
)

print(cli.organizations)  # orgs in the network
print(cli.peers)  # peers in the network
print(cli.orderers)  # orderers in the network
print(cli.CAs)  # ca nodes in the network


orderer_admin = cli.get_user(org_name="orderer1.org1.dz", name="Admin")
org1_admin = cli.get_user(org_name="org1.dz", name="Admin")
org1_user1 = cli.get_user(org_name="org1.dz", name="User1")

# your policy
policy = {
    "identities": [{"role": {"name": "member", "mspId": "PeerOrg1MSP"}}],
    "policy": {"1-of": [{"signed-by": 0}]},
}


cli.new_channel("firstchannel")
cli.new_channel("secondchannel")


# Creating the two channels
response = loop.run_until_complete(
    cli.channel_create(
        orderer="orderer1.org1.dz",
        channel_name="firstchannel",
        requestor=org1_admin,
        config_yaml="/*****************YOUR_PATH*****************/",
        channel_profile="firstchannel",
    )
)


response = loop.run_until_complete(
    cli.channel_create(
        orderer="orderer1.org1.dz",
        channel_name="secondchannel",
        requestor=org1_admin,
        config_yaml="/*****************YOUR_PATH*****************/",
        channel_profile="secondchannel",
    )
)


# Join Peers into Channel, the response should be true if succeed

responses = loop.run_until_complete(
    cli.channel_join(
        requestor=org1_admin,
        channel_name="firstchannel",
        peers=["peer0.org1.dz", "peer1.org1.dz", "peer2.org1.dz"],
        orderer="orderer1.org1.dz",
    )
)


responses = loop.run_until_complete(
    cli.channel_join(
        requestor=org1_admin,
        channel_name="secondchannel",
        peers=["peer0.org1.dz", "peer1.org1.dz", "peer2.org1.dz"],
        orderer="orderer1.org1.dz",
    )
)


# The response should be true if succeed
responses = loop.run_until_complete(
    cli.chaincode_install(
        requestor=org1_admin,
        peers=["peer0.org1.dz", "peer1.org1.dz", "peer2.org1.dz"],
        cc_path="firstcc",
        cc_name="firstcc",
        cc_version="v1.0",
    )
)
responses = loop.run_until_complete(
    cli.chaincode_install(
        requestor=org1_admin,
        peers=["peer0.org1.dz", "peer1.org1.dz", "peer2.org1.dz"],
        cc_path="secondcc",
        cc_name="secondcc",
        cc_version="v1.0",
    )
)

########################

cli.new_channel("firstchannel")
cli.new_channel("secondchannel")

args = ["data1", "value1"]


response = loop.run_until_complete(
    cli.chaincode_instantiate(
        requestor=org1_admin,
        channel_name="firstchannel",
        peers=["peer0.org1.dz", "peer1.org1.dz", "peer2.org1.dz"],
        args=args,
        # fcn="NewData",
        cc_name="firstcc",
        cc_version="v1.0",
        cc_endorsement_policy=policy,  # optional, but recommended
        collections_config=None,  # optional, for private data policy
        transient_map=None,  # optional, for private data
        wait_for_event=True,  # optional, for being sure chaincode is → instantiated
    )
)


response = loop.run_until_complete(
    cli.chaincode_instantiate(
        requestor=org1_admin,
        channel_name="secondchannel",
        peers=["peer0.org1.dz", "peer1.org1.dz", "peer2.org1.dz"],
        args=args,
        # fcn="NewData",
        cc_name="secondcc",
        cc_version="v1.0",
        cc_endorsement_policy=policy,  # optional, but recommended
        collections_config=None,  # optional, for private data policy
        transient_map=None,  # optional, for private data
        wait_for_event=True,  # optional, for being sure chaincode is → instantiated
    )
)


# Invoke the chaincode
args = ["Data2", "value2"]

# The response should be true if succeed
response = loop.run_until_complete(
    cli.chaincode_invoke(
        requestor=org1_admin,
        channel_name="firstchannel",
        peers=["peer0.org1.dz"],
        args=args,
        fcn="NewData",
        cc_name="firstcc",
        transient_map=None,  # optional, for private data
        wait_for_event=True,  # for being sure chaincode invocation has been → commited in the ledger, default is on tx event
    )
)


response = loop.run_until_complete(
    cli.chaincode_invoke(
        requestor=org1_admin,
        channel_name="secondchannel",
        peers=["peer0.org1.dz"],
        args=args,
        fcn="NewData",
        cc_name="secondcc",
        transient_map=None,  # optional, for private data
        wait_for_event=True,  # for being sure chaincode invocation has been → commited in the ledger, default is on tx event
    )
)


####################
# Query the chaincode
args = ["Data2"]
# The response should be true if succeed
response = loop.run_until_complete(
    cli.chaincode_query(
        requestor=org1_admin,
        fcn="GetData",
        channel_name="firstchannel",
        peers=["peer0.org1.dz"],
        args=args,
        cc_name="firstcc",
    )
)


response = loop.run_until_complete(
    cli.chaincode_query(
        requestor=org1_admin,
        fcn="GetData",
        channel_name="secondchannel",
        peers=["peer0.org1.dz"],
        args=args,
        cc_name="secondcc",
    )
)


##########
