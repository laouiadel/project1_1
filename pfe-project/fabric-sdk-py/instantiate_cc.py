import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()

cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")
org1_admin = cli.get_user('org1.dz', 'Admin')



org1_admin = cli.get_user(org_name='org1.dz', name='Admin')
# Make the client know there is a channel in the network
cli.new_channel('firstchannel')


# Instantiate Chaincode in Channel, the response should be true if succeed
args = ['a', '200', 'b', '300']

# policy, see https://hyperledger-fabric.readthedocs.io/en/release-1.4/endorsement-policies.html

policy = {
            "identities": [{"role": {"name": "member", "mspId": "PeerOrg1MSP"}}],
                "policy": {"1-of": [{"signed-by": 0}]},
                }



response = loop.run_until_complete(cli.chaincode_instantiate(
                   requestor=org1_admin,
                   channel_name='firstchannel',
                   peers=['peer0.org1.dz', 'peer1.org1.dz', 'peer2.org1.dz', 'peer3.org1.dz'],
                   args=args,
                   cc_name='first_chaincode',
                   cc_version='v1.0',
                   cc_endorsement_policy=policy, # optional, but recommended
                   collections_config=None, # optional, for private data policy
                   transient_map=None, # optional, for private data
                   wait_for_event=True # optional, for being sure chaincode is instantiated
                                                ))


print(response)

