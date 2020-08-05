# import modules
import asyncio
import ast
from hfc.fabric import Client 
import random
import json
from class_sm import Smartmeter
from merkletools import MerkleTools
import time
#import subprocess
import os
users = 12

#values we need to store for each node (sm)
list_from_bloc={}
list_leader_p={}

list_data={}
mr_data={}
timestamp={}
result_mr_data={}

list_vote_b1={}
list_rep_updated={}
list_leader_p_new={}
leader_new={}
mr_rep={}

result_mr_rep={}

list_vote_b2={}
b2={}


sm={}
for i in range(1, users+1):
	idd = i - 1
	sm[i] = Smartmeter(idd)

#start = time.time()
boo = 1
while boo == 1:
#    start = time.time()
    user = {}
    for i in range(1, users+1):
        user[i] = 'User'+str(i)
	#get the list of reputations from the last bloc in the blockchain
        list_from_bloc[i] = sm[i].get_list_from_bloc()
	#get the leader and the P% from the liste that we already get from the blockchain (list_from _bloc)
        list_leader_p[i] = sm[i].get_leader_and_p(list_from_bloc[i])


    start = time.time()
    for i in range(1, users+1):
        #each node send the mesure (data) to all P % noeuds (peers)
        sm[i].send_mesure_to_p(user[i], list_leader_p[i])
    
        
    for i in range(1, users+1):
        #get the consommations list (data), and its merkle root (MR-D), and the result of compariang the merkle data of the leader with the merkle data of the peer (1 of the P%)
        list_data[i], mr_data[i], timestamp[i], result_mr_data[i] = sm[i].retrieve_merkle_data(user[i], list_leader_p[i])
	#send vote by the P% node based on the comparaison of merkle root data (result_mr_data)
        sm[i].send_vote_b1(user[i], list_leader_p[i], result_mr_data[i])
    
    
    for i in range(1, users+1):
        #every node retrieve the vote list of B1 (list contain all votes of P% and the validation/nonvalidation of the the bloc B1 in the last field)
        list_vote_b1[i] = sm[i].retrieve_vote_b1(user[i])
#        print(list_vote_b1[i][-1])
	#update the reputation list based on the validation of B1 (based on list_vote_b1)
        list_rep_updated[i] = sm[i].maj_reputations(list_from_bloc[i], list_vote_b1[i], list_leader_p[i][0])
	#select a new leader in order to accomplish the second phase securly only if B1 was not valid
        #print(list_rep_updated)
        #exit()
        list_leader_p_new[i], leader_new[i] = sm[i].select_new_leader(list_leader_p[i], list_vote_b1[i][-1], list_vote_b1[i])
	#begin the second phase (B2) by calculating and sending the merkle root of the new reputaions list
        mr_rep[i] = sm[i].calculate_merkle_reputations(list_leader_p_new[i], list_rep_updated[i])
	#only the leader will sent the mr_rep in order to be collected by the P% peers and make the comparaison
        sm[i].send_maj_reputations(user[i], list_leader_p[i], list_leader_p_new[i], mr_rep[i])
    
    #exit()
    wet = time.time()
    for i in range(1, users+1):
	#retrieve the mr_rep calculated by the leader by all the peers (including the leader) and compare it to the mr_rep calculated by the peer (not the leader)
        result_mr_rep[i] = sm[i].retrieve_merkle_reputations(user[i], list_leader_p[i], list_leader_p_new[i], mr_rep[i])
	#send vote by the P% node based on the comparaison of merkle root rep (result_mr_rep)
        sm[i].send_vote_b2(user[i], list_leader_p_new[i], result_mr_rep[i])
    
#    wet = time.time()   
    for i in range(1, users+1):
        #every node retrieve the vote list of B2 (list contain all votes of P% and the validation/nonvalidation of the the bloc B2 in the last field)
        list_vote_b2[i] = sm[i].retrieve_vote_b2(user[i])
	#check the validation of B1 and B2 in the same time and take decision based on it, the value returned is B2 is validated/notvalidated (validated go to next round, notvalidated redo the second phase)
       # print(list_vote_b2[i][-1])
       # print(list_vote_b1[i][-1])
        #time.sleep(10)
        b2[i] = sm[i].validation_b2(user[i], list_vote_b2[i][-1], list_vote_b1[i][-1], list_leader_p_new[i], timestamp[i], list_data[i], mr_data[i], list_rep_updated[i], mr_rep[i])
        #time.sleep(10)
    wet2 = time.time()    
#test if b2 is not valid
    while b2[i] == 'notvalide':
        for i in range(1, users+1):
            list_leader_p_new[i], leader_new[i] = sm1[i].select_new_leader(list_leader_p_new[i], list_vote_b1[i][-1], list_vote_b1[i][i])
	    #begin the second phase (B2) by calculating and sending the merkle root of the new reputaions list
            mr_rep[i] = sm1[i].calculate_merkle_reputations(list_leader_p_new[i], list_rep_updated[i])
	    #only the leader will sent the mr_rep in order to be collected by the P% peers and make the comparaison
            sm1[i].send_maj_reputations(user[i], list_leader_p[i], list_leader_p_new[i], mr_rep[i])
        for i in range(1, users+1):
	    #retrieve the mr_rep calculated by the leader by all the peers (including the leader) and compare it to the mr_rep calculated by the peer (not the leader)
            result_mr_rep[i] = sm1[i].retrieve_merkle_reputations(user[i], list_leader_p[i], list_leader_p_new[i], mr_rep[i])
	    #send vote by the P% node based on the comparaison of merkle root rep (result_mr_rep)
            sm1.send_vote_b2(user[i], list_leader_p_new[i], result_mr_rep[i])

#        wet = time.time()
        #print(we9t)
        for i in range(1, users+1):
	    #every node retrieve the vote list of B2 (list contain all votes of P% and the validation/nonvalidation of the the bloc B2 in the last field)
            list_vote_b2[i] = sm1[i].retrieve_vote_b2(user[i])
	    #check the validation of B1 and B2 in the same time and take decision based on it, the value returned is B2 is validated/notvalidated (validated go to next round, notvalidated redo the second phase)
               
            b2[i] = sm1[i].validation_b2(user[i], list_vote_b2[i][-1], list_vote_b1[i][-1], list_leader_p_new[i], timestamp[i], list_data[i], mr_data[i], list_rep_updated[i], mr_rep[i])
        


    print("Finish")
    end = time.time()
    os.system('python delete_data.py')
    print("Next")
    print("b2 time: " + str(wet2 - wet))
    print(end - start)
#    print(list_vote_b1[1])
    time.sleep(30) #wait 15 min
