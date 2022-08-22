import hashlib

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, Hash160, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUAL, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

SelectParams('testnet')

def to_p2sh_scriptPubKey(self):
    """Create P2SH scriptPubKey from this redeemScript
    That is, create the P2SH scriptPubKey that requires this script as a
    redeemScript to spend.
    checksize - Check if the redeemScript is larger than the 520-byte max
    pushdata limit; raise ValueError if limit exceeded.
    Since a >520-byte PUSHDATA makes EvalScript() fail, it's not actually
    possible to redeem P2SH outputs with redeem scripts >520 bytes.
    """
    return CScript([OP_HASH160, Hash160(self), OP_EQUAL])
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
def create_txout(amount, scriptPubKey):
    return CMutableTxOut(amount*COIN, CScript(scriptPubKey))
def create_txin(txid, utxo_index):
    return CMutableTxIn(COutPoint(lx(txid), utxo_index))

faucet_address = CBitcoinAddress('mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB')

def P2PKH_scriptPubKey(address):
    ######################################################################
    # TODO: Complete the standard scriptPubKey implementation for a
    # PayToPublicKeyHash transaction
    return [
        OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG
    ]
    ######################################################################



# Create the (in)famous correct brainwallet secret key.
h = hashlib.sha256(b'correct horse battery staple').digest()
seckey = CBitcoinSecret.from_secret_bytes(h)

cust2_private_key = CBitcoinSecret(
    'cQudXCCUjYoPZihecq5mUuYFr7kFZQPXbdSM3jRHyRg1319AB5Mn')
cust2_public_key = cust2_private_key.pub
# Create a redeemScript. Similar to a scriptPubKey the redeemScript must be
# satisfied for the funds to be spent.
txin_redeemScript = CScript([cust2_public_key, OP_CHECKSIG])
print(b2x(txin_redeemScript))

# Create the magic P2SH scriptPubKey format from that redeemScript. You should
# look at the CScript.to_p2sh_scriptPubKey() function in bitcoin.core.script to
# understand what's happening, as well as read BIP16:
# https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki
txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()

# Convert the P2SH scriptPubKey to a base58 Bitcoin address and print it.
# You'll need to send some funds to it to create a txout to spend.
""" 
txin_p2sh_address = CBitcoinAddress.from_scriptPubKey(txin_scriptPubKey)
"""
print('Pay to:',P2PKHBitcoinAddress.from_pubkey(cust2_public_key))

# Same as the txid:vout the createrawtransaction RPC call requires
#
# lx() takes *little-endian* hex and converts it to bytes; in Bitcoin
# transaction hashes are shown little-endian rather than the usual big-endian.
# There's also a corresponding x() convenience function that takes big-endian
# hex and converts it to bytes.
txid = '697dd4cf5bb5c42cc5344bccf7f3c50399cfa4f5ad8c7a32d358ce207c24baf4'
vout = 1

# Create the txin structure, which includes the outpoint. The scriptSig
# defaults to being empty.
txin = create_txin(txid, vout)

# Create the txout. This time we create the scriptPubKey from a Bitcoin
# address.

txout = create_txout(0.0000005, P2PKH_scriptPubKey(faucet_address))




# Create the unsigned transaction.
tx = CMutableTransaction([txin], [txout])

# Calculate the signature hash for that transaction. Note how the script we use
# is the redeemScript, not the scriptPubKey. That's because when the CHECKSIG
# operation happens EvalScript() will be evaluating the redeemScript, so the
# corresponding SignatureHash() function will use that same script when it
# replaces the scriptSig in the transaction being hashed with the script being
# executed.
sighash = SignatureHash(txin_redeemScript, tx, 0, SIGHASH_ALL)

# Now sign it. We have to append the type of signature we want to the end, in
# this case the usual SIGHASH_ALL.
sig = cust2_private_key.sign(sighash) + bytes([SIGHASH_ALL])

# Set the scriptSig of our transaction input appropriately.
txin_scriptSig = [sig, txin_redeemScript]
txin.scriptSig = CScript(txin_scriptSig)

# Verify the signature worked. This calls EvalScript() and actually executes
# the opcodes in the scripts to see if everything worked out. If it doesn't an
# exception will be raised.
VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))
print("Pass Verification!\n")
# Done! Print the transaction to standard output with the bytes-to-hex
# function.

print(b2x(tx.serialize()))