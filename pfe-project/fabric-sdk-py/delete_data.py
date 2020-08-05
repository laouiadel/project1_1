
# import modules
import asyncio
import ast
from hfc.fabric import Client
import json
import random
from merkletools import MerkleTools
import time


loop = asyncio.get_event_loop()
cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

org1_admin = cli.get_user('org1.dz', 'Admin')  # user = User1 or User2 ...
# Make the client know there is a channel in the network
cli.new_channel('secondchannel')


SMs = ['SM0', 'SM1', 'SM2', 'SM3', 'SM4', 'SM5', 'SM6', 'SM7', 'SM8', 'SM9', 'SM10', 'SM11', 'B1_votes', 'B2_votes', 'hash_reputations']



for key in SMs:

    args = [key]
 #   print(args)
    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
         requestor=org1_admin,
         fcn='Delete',
         channel_name='secondchannel',
         peers=['peer0.org1.dz', 'peer1.org1.dz', 'peer2.org1.dz', 'peer3.org1.dz'], # the peer of the leader "not necessarly"
         args=args,
         cc_name='test_cc2',
         transient_map=None, 
         wait_for_event=True,
        ))
#    print(response)
