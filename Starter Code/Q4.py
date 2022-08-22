from bitcoin.core.script import *

######################################################################
# These functions will be used by Alice and Bob to send their respective
# coins to a utxo that is redeemable either of two cases:
# 1) Recipient provides x such that hash(x) = hash of secret
#    and recipient signs the transaction.
# 2) Sender and recipient both sign transaction
#
# TODO: Fill these in to create scripts that are redeemable by both
#       of the above conditions.
# See this page for opcode documentation: https://en.bitcoin.it/wiki/Script

# This is the ScriptPubKey for the swap transaction
def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        # fill this in!
        OP_IF, 
        OP_2, public_key_sender, public_key_recipient, OP_2, OP_CHECKMULTISIG,
        OP_ELSE, 
        public_key_recipient, OP_CHECKSIGVERIFY, OP_HASH160, hash_of_secret, OP_EQUAL,
        OP_ENDIF
    ]

# This is the ScriptSig that the receiver will use to redeem coins
def coinExchangeScriptSig1(sig_recipient, secret):
    return [
        # fill this in!
        secret, sig_recipient, OP_0
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed
def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [
        # fill this in!
        OP_0, sig_sender, sig_recipient, OP_1
    ]
######################################################################

######################################################################
#
# Configured for your addresses
#
# TODO: Fill in all of these fields
#
    # Note: Alice, BTC testnet; Bob BCY testnet3
    #
alice_txid_to_spend     = "1c5a4abe4326af9f2b0cec4422de2397cc8e1f203140c4205d03b0dc81990a97"
alice_utxo_index        = 0
alice_amount_to_send    = 0.00001111

bob_txid_to_spend       = "1210c2c0f8d2d217c88378ff3efa56e519a5e64a0c4461cdbfc1ca74fec9b014"
bob_utxo_index          = 0
bob_amount_to_send      = 0.00001111

# Get current block height (for locktime) in 'height' parameter for each blockchain (will be used in swap.py):
#  curl https://api.blockcypher.com/v1/btc/test3
btc_test3_chain_height  = 2254619

#  curl https://api.blockcypher.com/v1/bcy/test
bcy_test_chain_height   = 320503

# Parameter for how long Alice/Bob should have to wait before they can take back their coins
# alice_locktime MUST be > bob_locktime
alice_locktime = 5
bob_locktime = 3

tx_fee = 0.0001

# While testing your code, you can edit these variables to see if your
# transaction can be broadcasted succesfully.
broadcast_transactions = False
alice_redeems = False

######################################################################
