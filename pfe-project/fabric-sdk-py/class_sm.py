# import modules
import asyncio
import ast
from hfc.fabric import Client
import json
import random
from merkletools import MerkleTools
import time

class Smartmeter():
    '''A class define what each noeud can do in the consenus process'''

    def __init__(self, me):
        '''Initialisation some attributes'''
        self.me = me  # id of smart meter
        self.users = 12  # number of smart meters in the network
        # list_reputation = []
        self.peers = 4  # number of peers (P% best nodes)

    def get_list_from_bloc(self):

        ''' Get the reputation list from the last bloc in the blockchain '''

        self.loop = asyncio.get_event_loop()
        self.cli = Client(
            net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")
        self.org1_admin = self.cli.get_user('org1.dz', 'Admin')
        self.cli.new_channel("firstchannel")

        # first get the hash by calling 'query_info'
        self.response = self.loop.run_until_complete(self.cli.query_info(
            requestor=self.org1_admin,
            channel_name='firstchannel',
            peers=['peer0.org1.dz'],
            decode=True
        ))

        self.test_hash = self.response.currentBlockHash

        self.response = self.loop.run_until_complete(self.cli.query_block_by_hash(
            requestor=self.org1_admin,
            channel_name='firstchannel',
            peers=['peer0.org1.dz'],
            block_hash=self.test_hash,
            decode=True
        ))

        self.List_rep_bloc_byte = \
            self.response.get('data').get('data')[0].get('payload').get('data').get('actions')[0].get('payload').get(
                'action').get(
                'proposal_response_payload').get('extension').get('results').get('ns_rwset')[0].get('rwset').get(
                'writes')[
                0].get('value')
        self.List_rep_bloc_str = self.List_rep_bloc_byte.decode("UTF-8")  # convert byte to string
        self.List_rep_bloc_dic = ast.literal_eval(self.List_rep_bloc_str)  # convert dictionary string to dictionary
        
        for self.k, self.v in self.List_rep_bloc_dic.items():
            if self.k == 'Liste des reputations':
                self.List_rep_bloc = ast.literal_eval(self.v) # convert list from str -> list
        #str to int
        #for self.i in range(0, len(self.List_rep_bloc)):
         #   self.List_rep_bloc[self.i] = int(self.List_rep_bloc[self.i])

        return self.List_rep_bloc


    def get_leader_and_p(self, reputation_list_bloc):
        ''' return the leader and the P% nodes based on the reputation list in the last bloc in the blockchain '''
        self.list_reputation_slice = reputation_list_bloc[:]
        self.leader_id = self.list_reputation_slice.index(
            max(self.list_reputation_slice))  # 1er min id of node -leader- (men les P%) that has max reputation.
        self.list_p = []
        self.list_p.append(self.leader_id)
        self.list_reputation_slice[self.leader_id] = 0

        for i in range(0, self.peers - 1):
            self.p_id = self.list_reputation_slice.index(max(
                self.list_reputation_slice))  # p_1 i.e P%_1 - premier noeud du p% - (# 2eme min id of node (men les P%) that has max reputation.)
            self.list_p.append(self.p_id)  # list_p contient le id du leader et les id des P%.
            self.list_reputation_slice[self.p_id] = 0

        return self.list_p

    def send_mesure_to_p(self, user, list_p):
        '''Send data to all P% -normalment to all nodes-'''

        self.loop = asyncio.get_event_loop()

        self.cli = Client(
            net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")
        self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
        # Make the client know there is a channel in the network
        self.cli.new_channel('secondchannel')

        self.my_data = str(random.randint(2, 22)) + "kw"  # data consumed by the SM
        # my_reputation = str(list_reputation[Me])   #reputation of this SM.  On envoi pas la reputation.

        for i in range(0, self.peers):
            '''Send data consumed by this SM
                To all the peers in the network (P%)
                car c eux qui font la verification du bloc
                '''

            self.args = ['SM' + str(list_p[i]), str(self.me), str(self.my_data)]

            # The response should be true if succeed
            self.response = self.loop.run_until_complete(
                self.cli.chaincode_invoke(
                    requestor=self.org1_admin,
                    channel_name='secondchannel',
                    peers=['peer' + str(i) + '.org1.dz'],
                    args=self.args,
                    fcn='NewData',
                    cc_name='test_cc2',
                    transient_map=None,  # optional, for private data
                    wait_for_event=True,
                )
            )

    def retrieve_merkle_data(self, user, list_p):
        self.ret = ""
        self.loop = asyncio.get_event_loop()

        self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

        self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
        # Make the client know there is a channel in the network
        self.cli.new_channel('secondchannel')

        self.list_pp = list_p[:]
        self.list_data_retrived = []
        #del self.list_pp[0]
        if 1 == 1:
#            self.list_data_retrived = []
            self.args = ['SM' + str(self.list_pp[0])]
            self.lead_me = '0' # l'id du peer qui est relier avec le leader
            for i in range(0, 2):
                # The response should be true if succeed
                self.response = self.loop.run_until_complete(self.cli.chaincode_query(
                    requestor=self.org1_admin,
                    fcn="GetData",
                    channel_name='secondchannel',
                    peers=['peer' + self.lead_me + '.org1.dz'],
                    args=self.args,
                    cc_name='test_cc2'
                ))
                self.response = json.loads(self.response)
                self.list_data_retrived.append(self.response)
                if self.me == self.list_pp[0] or self.me not in self.list_pp:
                    break
                self.args = ['SM' + str(self.me)]
                self.lead_me = str(self.list_pp.index(self.me))  # mon id in str to use it in cli.chaincode_query "peers"


                #self.response = json.loads(self.response)
#
                #self.list_data_retrived.append(self.response)
#
           # print(self.list_data_retrived)
            

            if self.me in self.list_pp and self.me != self.list_pp[0]:
                if (self.list_data_retrived[0]['MerklerootDATA'] == self.list_data_retrived[1]['MerklerootDATA']):
                    self.ret = "true"
                else:
                    self.ret = "false"

        return (self.list_data_retrived[0]['Consommations'], self.list_data_retrived[0]['MerklerootDATA'], self.list_data_retrived[0]['Timestamp'], self.ret)


    def send_vote_b1(self, user, list_p, result_comparaison):
        
        ''' every user from P% send votes about the validation of B1 (merkle root local comparer avec merkle root du leader)'''

        self.list_pp = list_p[:]
        del self.list_pp[0]
        
        if self.me in self.list_pp:

            if result_comparaison == "true":
                self.vote = "accepter"
            elif result_comparaison == "false":
                self.vote = "rejeter"


            self.loop = asyncio.get_event_loop()

            self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

            self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
            # Make the client know there is a channel in the network
            self.cli.new_channel('secondchannel')

        
            self.args = ["B1_votes", str(self.me), self.vote]
    
            # The response should be true if succeed
            self.response = self.loop.run_until_complete(self.cli.chaincode_invoke(
                requestor=self.org1_admin,
                fcn='Votes',
                channel_name='secondchannel',
                peers=['peer0.org1.dz'], # the peer of the leader
                args=self.args,
                cc_name='test_cc2',
                transient_map=None, 
                wait_for_event=True,
                ))


    
    def retrieve_vote_b1(self, user):

        '''Every user retrieve the list of validation of B1 that contain the votes of P%, and if B1 is valid or not'''
        
        self.loop = asyncio.get_event_loop()
        self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

        self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
        # Make the client know there is a channel in the network
        self.cli.new_channel('secondchannel')

        self.args = ['B1_votes']
                # The response should be true if succeed
        self.response = self.loop.run_until_complete(self.cli.chaincode_query(
                requestor=self.org1_admin,
                fcn='GetVotes',
                channel_name='secondchannel',
                peers=['peer0.org1.dz'],
                args=self.args,
                cc_name='test_cc2'
                ))

        self.response = ast.literal_eval(self.response)  # convert dictionary string to dictionary
        return self.response["List Votes"]  # return List


    def maj_reputations(self, List, List_vote, leader):
        '''mise a jour de la liste des reputations'''
        self.validation_bloc = List_vote[-1]
        self.List_copy = List[:]
        if self.validation_bloc == 'valide':
            self.List_copy [leader] = self.List_copy [leader] + 10
            for self.i in range(0, len(List_vote)):
                if List_vote[self.i] == 'accepter':
                    self.List_copy[self.i] = self.List_copy[self.i] + 10
                elif List_vote[self.i] == 'rejeter':
                    self.List_copy[self.i] = self.List_copy[self.i] - 10

        if self.validation_bloc == 'notvalide':
            self.List_copy [leader] = self.List_copy [leader] - 10
            for self.i in range(0, len(List_vote)):
                if List_vote[self.i] == 'accepter':
                    self.List_copy[self.i] = self.List_copy[self.i] - 10
                elif List_vote[self.i] == 'rejeter':
                    self.List_copy[self.i] = self.List_copy[self.i] + 10

        for self.i in range(0, len(List)):
            if self.List_copy[self.i] > 100:
                self.List_copy[self.i] = 100
            elif self.List_copy[self.i] < 0:
                self.List_copy[self.i] = 0


        return self.List_copy



    def select_new_leader(self, p_leader, validation_b1, liste_vote_b1):
        '''change leader only if the validation of bloc B1 (validation_b1) is = notvalid '''
        self.new_leader = p_leader[0]
        self.p_leader_new = p_leader[:]
        self.boo = 1
        
        if validation_b1 == 'notvalid':
            while self.boo:
                self.ancien_leader = self.p_leader_new.pop(0)
                self.p_leader_new.append(self.ancien_leader)
                self.new_leader = self.p_leader_new[0]
                if list_vote_b1[self.new_leader] == 'rejeter':
                    self.boo = 0

        return (self.p_leader_new, self.new_leader)



    def calculate_merkle_reputations(self, p_leader_new, list_rep_updated):
        '''Calculer le merkle root de la liste des reputations par chaque noeud des P%'''
        self.liste_maj_rep = list_rep_updated[:]
        self.mt = MerkleTools(hash_type="sha256")
        for self.i in range(0, len(self.liste_maj_rep)):
            self.liste_maj_rep[self.i] = str(self.liste_maj_rep[self.i])
        self.mt.add_leaf(self.liste_maj_rep, True)
        self.mt.make_tree()
        self.is_ready = self.mt.is_ready
       	self.root_value = self.mt.get_merkle_root()
        return self.root_value



    def send_maj_reputations(self, user, p_leader, p_leader_new, liste_maj_rep_hash):
        # mypeer is the peer of the user(node) from the updated list p_leader "p_leader_new".
        '''send the new reputations list to the actual peer of the leader in order to make a merkle root for it'''
        if self.me == p_leader_new[0]:
            self.loop = asyncio.get_event_loop()

            self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

            self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
            # Make the client know there is a channel in the network
            self.cli.new_channel('secondchannel')

            self.mypeer = p_leader.index(p_leader_new[0])
            self.args = ["hash_reputations", liste_maj_rep_hash]

            # The response should be true if succeed
            self.response = self.loop.run_until_complete(self.cli.chaincode_invoke(
                requestor=self.org1_admin,
                fcn='NewRep',
                channel_name='secondchannel',
                peers=['peer'+str(self.mypeer)+'.org1.dz'], # the peer of the leader
                args=self.args,
                cc_name='test_cc2',
                transient_map=None,
                wait_for_event=True,
                ))
        

    def retrieve_merkle_reputations(self, user, p_leader, p_leader_new, local_hash_rep): 
        # l'id du peer qui est relier avec le leader
        '''recuperer le merkle root de la liste de reputations a partir du peer du leader'''
        self.result_comparaison2 = ""
        self.loop = asyncio.get_event_loop()

        self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

        self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
        # Make the client know there is a channel in the network
        self.cli.new_channel('secondchannel')
        self.list_pp = p_leader_new[:]
        del self.list_pp[0]
        if self.me in self.list_pp:
            self.list_data_retrived = []
            self.args = ["hash_reputations"]

            self.peer_leader = p_leader.index(p_leader_new[0])
            # The response should be true if succeed
            self.response = self.loop.run_until_complete(self.cli.chaincode_query(
                requestor=self.org1_admin,
                fcn='GetRep',
                channel_name='secondchannel',
                peers=['peer' + str(self.peer_leader) + '.org1.dz'],
                args=self.args,
                cc_name='test_cc2'
                ))

            #self.lead_me = str(self.list_pp.index(self.me) + 1)  # mon id in str to use it in cli.chaincode_query "peers"


            self.response = json.loads(self.response)
            #print(type(self.response))
            #self.list_data_retrived.append(self.response)
#
#            print(self.list_data_retrived)
            if self.response['MerklerootReputations'] == local_hash_rep:
            	self.result_comparaison2 = "true"
            else:
            	self.result_comparaison2 = "false"
        
        return self.result_comparaison2



    def send_vote_b2(self, user, list_p, result_comparaison):
        
        ''' every user from P% send votes about the validation of B2 (merkle root local comparer avec merkle root du leader)'''

        self.list_pp = list_p[:]
        del self.list_pp[0]
        
        if self.me in self.list_pp:

            if result_comparaison == "true":
                self.vote = "accepter"
            elif result_comparaison == "false":
                self.vote = "rejeter"


            self.loop = asyncio.get_event_loop()

            self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

            self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
            # Make the client know there is a channel in the network
            self.cli.new_channel('secondchannel')

        
            self.args = ["B2_votes", str(self.me), self.vote]
    
            # The response should be true if succeed
            self.response = self.loop.run_until_complete(self.cli.chaincode_invoke(
                requestor=self.org1_admin,
                fcn='Votes',
                channel_name='secondchannel',
                peers=['peer0.org1.dz'], # the peer of the leader "not necessarly"
                args=self.args,
                cc_name='test_cc2',
                transient_map=None, 
                wait_for_event=True,
                ))


    def retrieve_vote_b2(self, user):

        '''Every user retrieve the list of validation of B2 that contain the votes of P%, and if B1 is valid or not'''
        
        self.loop = asyncio.get_event_loop()
        self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")

        self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
        # Make the client know there is a channel in the network
        self.cli.new_channel('secondchannel')

        self.args = ["B2_votes"]
                # The response should be true if succeed
        self.response = self.loop.run_until_complete(self.cli.chaincode_query(
                requestor=self.org1_admin,
                fcn='GetVotes',
                channel_name='secondchannel',
                peers=['peer0.org1.dz'],
                args=self.args,
                cc_name='test_cc2',
                ))

        self.response = ast.literal_eval(self.response)  # convert dictionary string to dictionary
        return self.response["List Votes"]  # return List




    def validation_b2(self,user, state_b2, state_b1, p_leader_new, time, data, mr_data, list_reputations, mr_reputations):
        ''' '''
        self.value = ""
        self.k = 0
        if state_b2 == 'notvalide':
            self.value = 'notvalide'
        elif state_b2 == 'valide' and state_b1 == 'valide':
            self.value = 'valide'
            self.k = 1
        elif state_b2 == 'valide' and state_b1 == 'notvalide':
            self.value = 'valide'
            self.k = 1
            for self.i in range(0, len(data)):
                data[self.i] = "0" 
            self.mt = MerkleTools(hash_type="sha256")
            self.mt.add_leaf(data, True)
            self.mt.make_tree()
            mr_data = self.mt.get_merkle_root()
        
        #print(self.value)
        #print(p_leader_new[0])
        if self.k == 1 and self.me == p_leader_new[0]:
            #print(self.value)
            #print(p_leader_new[0])
            self.loop = asyncio.get_event_loop()
            self.cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")
            self.org1_admin = self.cli.get_user('org1.dz', user)  # user = User1 or User2 ...
            # Make the client know there is a channel in the network
            self.cli.new_channel('firstchannel')
            self.args = [str(time), str(data), str(mr_data), str(list_reputations), str(mr_reputations)]
    
           # The response should be true if succeed
            self.response = self.loop.run_until_complete(self.cli.chaincode_invoke(
               	requestor=self.org1_admin,
               	fcn='NewData',
               	channel_name='firstchannel',
               	peers=['peer0.org1.dz'], 
               	args=self.args,
               	cc_name='first_chaincode',
               	transient_map=None, 
               	wait_for_event=True,
	                ))
            #print(self.response)
            #exit()
            
            return self.value


