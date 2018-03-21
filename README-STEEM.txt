If you want to try out the blockchainintegrity module for posting merkle tree roots on the STEEM blockchain, there are a few steps needed that didn't quite fit into the setup script.

First, you need to have both Python 2 and Python 3 installed.

For Python 2, you need to install the beem python module

* https://github.com/holgern/beem

For Python 3, install steem-python

* https://github.com/steemit/steem-python

Note that the need for the later should be temporary and is a bit of a hack needed due
to the fact that beem is a realtively young library and doing transactions currently
doesn't seem to work as expected in Python 2.

After these two are installed, use quick_setup for the rest of the setup.

Before you can run the module, edit /etc/mfmf/steem.json and supply it with your STEEM
account settings. During testing, leave 'debug' on true, but please be sure to set it to
false if you want to do some kind of production level volumes with it. In debug mode all transactions will be toward your own account rather than the @null account.

Start the module blockchainintegrity.py as mfmf_009. This account owns your config file
and thus can be used to read your config while keeping your credentials safe from regular system users.
