from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


cust1_private_key = CBitcoinSecret(
    'cNueuxnikv79izoREdorckhCM4uiru8LE4zbb1JRCdAuKVgNYZuJ')
cust1_public_key = cust1_private_key.pub
cust2_private_key = CBitcoinSecret(
    'cQudXCCUjYoPZihecq5mUuYFr7kFZQPXbdSM3jRHyRg1319AB5Mn')
cust2_public_key = cust2_private_key.pub
cust3_private_key = CBitcoinSecret(
    'cUfH5fzpSQiK66CifHq3fDghcHZ7emqxXFHGeGfcA8aC8j1AxiVH')
cust3_public_key = cust3_private_key.pub


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 3

# You can assume the role of the bank for the purposes of this problem
# and use my_public_key and my_private_key in lieu of bank_public_key and
# bank_private_key.

Q3a_txout_scriptPubKey = [
    my_public_key, OP_CHECKSIGVERIFY, 
    OP_1, cust1_public_key, cust2_public_key, cust3_public_key, OP_3, OP_CHECKMULTISIG
]

# missing h(redeem script)

######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.000007 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        'a287c8645b7ebb8844d6b0e30bfc888a0069a6567e6b8ee10d08fc1a5e715386')
    utxo_index = 0 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, 
        utxo_index, Q3a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
