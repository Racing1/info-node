import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# This is the currency which you received API key for
CURRENCY_TICKER = ""
# Run $infonode to retrieve the API key, you must be admin of the project
FAT_PANDA_CLUB_API_KEY = ""
# IP of target node, 127.0.0.1 for localhost
INFO_NODE_HOST = ""
# Port of info node
INFO_NODE_PORT = ""
# Provide RPC credentials
INFO_NODE_RPC_USERNAME = ""
INFO_NODE_RPC_PASSWORD = ""

# Payload json
stats = {
    'peers': []
}

# On failure check VPS is able to access target node and RPC credentials are correct
connection = AuthServiceProxy("http://%s:%s@%s:%s" % \
    ( INFO_NODE_RPC_USERNAME, INFO_NODE_RPC_PASSWORD, INFO_NODE_HOST, INFO_NODE_PORT) )

# Customize to specific chain
# Accepted metrics are [ 'version', 'protocolversion', 'walletversion', 'blocks' ]
# Get in touch with us to expand the metrics list
getinfo = connection.getinfo()
#getinfo = connection.getblockchaininfo()
#getinfo = connection.getwalletinfo()
stats['version'] = getinfo['version']
stats['protocolversion'] = getinfo['protocolversion']
stats['walletversion'] = getinfo['walletversion']
stats['blocks'] = getinfo['blocks']

# Peers data
peers = connection.getpeerinfo()
for p in peers:
    stats['peers'].append(p['addr'])

# Submit metrics to panda-bot
url = "https://api.fatpanda.club/stat/%s" % CURRENCY_TICKER.lower()

headers = {
    'x-api-key': FAT_PANDA_CLUB_API_KEY,
    'content-type': "application/json",
    'user-agent': "panda-minion"
    }

response = requests.request("POST", url, headers=headers, json=stats)

assert response.status_code == 200
assert response.json()['success']
