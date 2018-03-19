#!/usr/bin/python
#This is just proof-of-concept level code, nowhere near production stable. 
#This script should be rewritten to make proper use of one of the Python 2.x steem libraries.
#This could either be "beem", or maybe in the distant future asyncsteem is the mfmf library can 
#be made into a Twisted based asynchonous library as well. 
#Fow now mfmf asn't a Twisted enabled lib, so beem should be a good choice once we get the 
#'transfer' stuff sorted.
import json
import os
import math
import time
import beem 
try:
    #If you build your own module framework, it is sugested you name it fmfw as working title
    #so all mfmf modules work out of the box potentially. 
    from fmfw import run
except:
    from mfmf import run

def do_transaction(account,keys,target,coin,amount,memo):
    #A bit silly as beem should support this. We use an external peogram for the transaction.
    os.environ["STEEM_ACCOUNT"] = account
    os.environ["STEEM_POSTING_KEY"] = keys[0]
    os.environ["STEEM_ACTIVE_KEY"] = keys[1]
    os.environ["STEEM_COIN"] = coin
    os.environ["STEEM_AMOUNT"] = amount
    os.environ["STEEM_TARGET"] = target
    os.environ["STEEM_MEMO"] = memo

    script = os.path.realpath(os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)),"mfmf_steem_transaction.py"))
    os.system("/usr/bin/python3 " + script)

def find_transaction_block(account,target,coin,amount,memo,start):
    s = beem.steem.Steem()
    bc = beem.blockchain.Blockchain(steem_instance=s)
    starttime = time.time()
    for op in bc.stream("transfer",start=start):
        if time.time() - starttime > 600:
            raise Exception("Taking way to long (> 10 minutes) to find transaction in the blockchain.")
        if op["from"] == account and op["to"] == target and op["memo"] == memo:
            return op["block_num"]

def process_merkletree_root_hash(hsh, config):
    keys = config["keys"]
    account = config["account"]
    case = config["case"]
    debug = False
    if "debug" in config:
        debug = config["debug"]
    target = "null"
    if debug:
        target = account
    coin = "STEEM"
    if "coin" in config and config["coin"] == "SBD":
        coin = "SBD"
    amount = "0.001"
    if "amount" in config:
        try:
            amm = float(config["amount"])
            if amm > 1.0:
                amount = "1.000"
            else:
                if amm > 0.001:
                    amount = str(math.floor(float(amm)*1000)/1000)
        except:
            pass
    memo = "mattockfs " + "case=" + case + " mt-root=" + hsh
    s = beem.steem.Steem()
    start_blockno = s.info()["head_block_number"]
    do_transaction(account,keys,target,coin,amount,memo)
    return find_transaction_block(account,target,coin,amount,memo,start_blockno)

class RootNode:
    def __init__(self,carvpathfile, conf):
        self.conf = conf
        self.imgpath = carvpathfile.as_file_path()
        mtree = {}
        self.merkleroot = None
        with open(self.imgpath,"r") as f:
            try:
                mtree = json.loads(f.read())
            except:
                print "Oops: invalid json."
                pass
        if "mh" in mtree:
            self.merkleroot = mtree["mh"]
        else:
            print "Oops: no 'mh' in merkletree JSON."
    def children(self):
        return []
    def get_meta(self):
        meta = {}
        if self.merkleroot != None:
            meta["mime-type"] = "x-blockchain/merkleroot"
            meta["merkletree-root"] = self.merkleroot
            meta["merkletree-carvpath"] = self.imgpath
            meta["block_number"] =  process_merkletree_root_hash(self.merkleroot, conf)
        return meta

class BlockChainIntegrityModule:
    def __init__(self,conf):
        self.conf = conf
    def root(self,carvpathfile,arg):
        return RootNode(carvpathfile, conf)
    def name(self):
        return "blockchainintegrity"

conf = {}
try:
    with open("/etc/mfmf/steem.json") as f:
        conf = json.loads(f.read())
except:
    print "Problem opening or parsing /etc/mfmf/steem.json"

if "keys" in conf and "account" in conf and "case" in conf:
    if conf["keys"][0] == "" or conf["keys"][1] == "" :
        print "Please set up /etc/mfmf/steem.json with your own keys and account for STEEM!"
    else:
        run(BlockChainIntegrityModule(conf))
else:
    print "Non-existing or incomplete config for this module"

