import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()

cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")
org1_admin = cli.get_user('org1.dz', 'Admin')



org1_admin = cli.get_user(org_name='org1.dz', name='Admin')
# Make the client know there is a channel in the network
cli.new_channel('firstchannel')

# Install Example Chaincode to Peers
# The response should be true if succeed
responses = loop.run_until_complete(cli.chaincode_install(
                   requestor=org1_admin,
                   peers=['peer0.org1.dz',
                          'peer1.org1.dz',
                          'peer2.org1.dz',
                          'peer3.org1.dz'],
                   cc_path='chaincodes',
                   cc_name='first_chaincode',
                   cc_version='v1.0'
                             ))

print(responses)
