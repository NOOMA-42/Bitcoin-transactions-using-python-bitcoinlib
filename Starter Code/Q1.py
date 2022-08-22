from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)


def P2PKH_scriptPubKey(address):
    ######################################################################
    # TODO: Complete the standard scriptPubKey implementation for a
    # PayToPublicKeyHash transaction
    return [
        OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG
    ]
    ######################################################################


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key, public_key):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             private_key)
    ######################################################################
    # TODO: Complete this script to unlock the BTC that was sent to you
    # in the PayToPublicKeyHash transaction.
    return [
        signature, public_key
    ] 
    ######################################################################

def send_from_P2PKH_transaction(amount_to_send,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey,
                                sender_private_key,
                                network):

    sender_public_key = sender_private_key.pub
    sender_address = P2PKHBitcoinAddress.from_pubkey(sender_public_key)

    txout = create_txout(amount_to_send, txout_scriptPubKey) # UTXO of sendee

    txin_scriptPubKey = P2PKH_scriptPubKey(sender_address) # UTXO of your self. Containing scriptPK
    txin = create_txin(txid_to_spend, utxo_index) # txid+utxo index
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey,
        sender_private_key, sender_public_key)
    
    # Input | Output | Output
    # txin (txid_to_spend, utxo_index), signature, public_key | txout (= amount + UTXO of sendee) | txin_scriptPubKey (= P2PKH_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)
    # *not sure how does create signed work?

    
    return broadcast_transaction(new_tx, network)


if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.0001 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        '0d237766b1e4deffc26c925e7665063c353cb067f2a800b799a0eba2643b105f')
    utxo_index = 1 # index of the output you are spending, indices start at 0
    ######################################################################

    txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)
    response = send_from_P2PKH_transaction(
        amount_to_send,
        txid_to_spend,
        utxo_index,
        txout_scriptPubKey,
        my_private_key,
        network_type,
    )
    print(response.status_code, response.reason)
    print(response.text)
