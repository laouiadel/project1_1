import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()

cli = Client(net_profile="/home/Adel/Desktop/PFE/Two_Chain_Network_Template/pfe-project/sdk/MyNetwork.json")
org1_admin = cli.get_user('org1.dz', 'Admin')



org1_admin = cli.get_user(org_name='org1.dz', name='Admin')
# Make the client know there is a channel in the network
cli.new_channel('firstchannel')



# Invoke the chaincode
args = ['10/07/2020 06:09:30', '[2kw, 4kw, 18kw, 21kw, 11kw, 10kw, 9kw, 13kw, 4kw, 15kw, 12kw, 8kw]', 'sd7f6s7f6s7f8as7fs7f8', '[66, 45, 78, 94, 77, 0, 0, 0, 0, 0, 44, 36]', 'asf7safs6f5s4df5sd4fas']

# The response should be true if succeed
response = loop.run_until_complete(
            cli.chaincode_invoke(
            requestor=org1_admin,
            channel_name='firstchannel',
            peers=['peer0.org1.dz', 'peer1.org1.dz', 'peer2.org1.dz', 'peer3.org1.dz'],
            args=args,
            fcn='NewData',
            cc_name='first_chaincode',
            transient_map=None,  # optional, for private data
            wait_for_event=True,  # for being sure chaincode invocation has been  commited in the ledger, default is on tx event
                                                                                    )
            )

print(response)
