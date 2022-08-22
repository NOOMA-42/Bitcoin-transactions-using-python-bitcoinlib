from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2
Q2a_txout_scriptPubKey = [
        OP_2DUP, OP_ADD, OP_5, OP_EQUALVERIFY, OP_SUB, OP_3, OP_EQUAL
]

# Condition Script
# https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line/blob/master/12_1_Using_Script_Conditionals.md
# 
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.000004 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        'f38fa3f2956c4afd2562bf6f9331a1fcbbfc002d67c78c3a3d16f197850b77a5')
    utxo_index = 0 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q2a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
