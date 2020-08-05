import asyncio
import ast
from hfc.fabric import Client
import json
loop = asyncio.get_event_loop()
cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")
org1_admin = cli.get_user('org1.dz', 'User1')

cli.new_channel("firstchannel")
# first get the hash by calling 'query_info'
response = loop.run_until_complete(cli.query_info(
             requestor=org1_admin,
             channel_name='firstchannel',
             peers=['peer0.org1.dz'],
             decode=True
                       ))

print(response)
test_hash = response.currentBlockHash

response = loop.run_until_complete(cli.query_block_by_hash(
               requestor=org1_admin,
               channel_name='firstchannel',
               peers=['peer0.org1.dz'],
               block_hash=test_hash,
               decode=True
               ))

List_rep_bloc_byte = response.get('data').get('data')[0].get('payload').get('data').get('actions')[0].get('payload').get('action').get('proposal_response_payload').get('extension').get('results').get('ns_rwset')[0].get('rwset').get('writes')[0].get('value')


List_rep_bloc_str = List_rep_bloc_byte.decode("UTF-8") # convert byte to string
# using ast.literal_eval()

List_rep_bloc_dic = ast.literal_eval(List_rep_bloc_str) # convert dictionary string to dictionary
print(List_rep_bloc_dic)

for k, v in List_rep_bloc_dic.items():
    if k == 'Liste des reputations':
    	List_rep_bloc = v

print(List_rep_bloc)
#cli.new_channel('secondchannel')
#tx_id = response.get('data').get('data')[0].get(
 #   'payload').get('header').get(
  #  'channel_header').get('tx_id')


