from hfc.fabric import Client
import asyncio

loop = asyncio.get_event_loop()

cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

org1_admin = cli.get_user(org_name='org1.dz', name='Admin')


# Create a New Channel, the response should be true if succeed
response = loop.run_until_complete(cli.channel_create(
                orderer='orderer.org1.dz',
                channel_name='firstchannel',
                requestor=org1_admin,
                config_yaml='/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project',
                channel_profile='firstchannel'
                                                       ))


print(response == True)


# Join Peers into Channel, the response should be true if succeed

responses = loop.run_until_complete(cli.channel_join(
                   requestor=org1_admin,
                   channel_name='firstchannel',
                   peers=['peer0.org1.dz',
                          'peer1.org1.dz',
                          'peer2.org1.dz',
                          'peer3.org1.dz'],
                   orderer='orderer.org1.dz'
                                                                                                         ))

print(len(responses) == 4)


# Create a Second Channel, the response should be true if succeed
response = loop.run_until_complete(cli.channel_create(
                orderer='orderer.org1.dz',
                channel_name='secondchannel',
                requestor=org1_admin,
                config_yaml='/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project',
                channel_profile='secondchannel'
                                                       ))


print(response == True)


# Join Peers into Second Channel, the response should be true if succeed

responses = loop.run_until_complete(cli.channel_join(
                   requestor=org1_admin,
                   channel_name='secondchannel',
                   peers=['peer0.org1.dz',
                          'peer1.org1.dz',
                          'peer2.org1.dz',
                          'peer3.org1.dz'],
                   orderer='orderer.org1.dz'
                              ))
print(len(responses) == 4)
