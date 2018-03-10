import os
import logging
command = '''curl --user dylan:123456 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockcount", "params": [] }' -H 'content-type: application/json;' http://1.119.143.222:18332  >a.out'''
r =os.system(command)
print r
