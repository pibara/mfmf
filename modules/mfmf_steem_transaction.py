#!/usr/bin/python3
#This should NOT be a seperate program but unfortunately non of the Python 2 steem libs
#seem able to perform transfer transactions.
import os 
import steem

account = os.environ["STEEM_ACCOUNT"]
keys = [os.environ["STEEM_POSTING_KEY"],os.environ["STEEM_ACTIVE_KEY"]]
coin = os.environ["STEEM_COIN"]
amount = os.environ["STEEM_AMOUNT"]
target = os.environ["STEEM_TARGET"]
memo = os.environ["STEEM_MEMO"]

stm = steem.steem.Steem(["https://rpc.buildteam.io","steemd.minnowsupportproject.org","steemd.pevo.science","rpc.steemviz.com","seed.bitcoiner.me","rpc.steemliberator.com","api.steemit.com","steemd.privex.io"], keys=keys)
steem.instance.set_shared_steemd_instance(stm)
stm.commit.transfer(target, amount, coin, memo=memo, account = account)

with open("/tmp/mfmf-dummy.log","w") as f:
    f.write(account)
    f.write("\n")
    f.write(amount)
    f.write(" ")
    f.write(coin)
    f.write("\n")
    f.write(target)
    f.write("\n")
    f.write(memo)

