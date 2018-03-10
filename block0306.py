# coding= utf-8
import json
import sys
import os
from datetime import datetime,timedelta
import json
import os.path
import time
import MySQLdb
import Cookie
import random
import sqlite3
import base64

import pdb
#pdb.set_trace()
def getCount():
    command = '''curl  -s  --user dylan:123456 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockcount", "params": [] }' -H 'content-type: application/json;' http://1.119.143.222:18332  '''
    try:
        print command
        output = os.popen(command)
        ret =  output.read()
        ret_json =  json.loads(ret)
        count =ret_json['result']
        return 0, count
        
    except:
        return 1,0

def  getHash(blockcount):
    command = '''curl -s --user dylan:123456 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [%s] }' -H 'content-type: application/json;' http://1.119.143.222:18332 '''%blockcount
    print command
    try:
        output = os.popen(command)
        ret =  output.read()
        ret_json =  json.loads(ret)
        hash =ret_json['result']
        return 0, hash
        
    except:
        return 1,''

def getBlock(hash):
    command = '''curl -s --user dylan:123456 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["%s", 2] }' -H 'content-type: application/json;' http://1.119.143.222:18332 '''%(hash)
    print command
    try:
        output = os.popen(command)
        ret =  output.read()
        ret_json =  json.loads(ret)
        block =ret_json['result']
        return 0, block

    except:
        return 1,''


def putDB(block):
    conn = MySQLdb.Connect(host='localhost',user='root',passwd='',db='bitcoin',port=3306,charset = 'utf8')
    cur = conn.cursor()
    #time = cur.execute("select now()")
    #print time
    with open("./block.json","w") as f:
        json.dump(block,f)
    #s = json.loada(jsondata)
    #test=s

    test=block
    python_to_json = json.dumps(test, ensure_ascii=False)
    json_to_python = json.loads(python_to_json)
    no=0
    height = json_to_python['height']
    #pdb.set_trace()
    total = len(json_to_python['tx']) #remove result
    for no in range(0, total):
        #print "begin processing transaction %d of  %d------------"%(no,total) 
        #print json_to_python['result']['tx'][no]
        atr = json_to_python['tx'][no] #remove result
       # print "txid = %s"%atr['txid']
        txid = atr['txid']
       # print atr['vout'][0]['value']
        value = atr['vout'][0]['value']

        address=''
        addresscount=0
        try:
            #print atr['vout'][0]['scriptPubKey']['addresses']      
            addresscount=len(atr['vout'][0]['scriptPubKey']['addresses'])
            #print "address count %d"%addresscount
            address = atr['vout'][0]['scriptPubKey']['addresses']
        except:
            #print "line %d  txid = %s"%(no,atr['txid'])
            pass
        print "address count %d"%addresscount
        for addressno in range(0, addresscount):
            #sql = '''insert into tx(tx_out_value, txid, tx_address)  values ("%s",  "%s", "%s");'''%(value,txid,address[addressno])
            sql = '''insert into tx_out(tx_out_value, txid, tx_out_address,tx_height)  values ("%s",  "%s", "%s", "%s");'''%(value,txid,address[addressno],height)
            print sql
            ok = cur.execute(sql)
    conn.commit()

def test_Current():
    error ,count = getCount()
    if error:
        print "error"
    print count;
    #pdb.set_trace()
    error ,hash = getHash(count)
    if error:
        print "error"
    print hash

    error,block = getBlock(hash)
    if error:
        print "error"

    #print block

    putDB(block)

def getBlockNo():
    command = '''tail -n 1 ./block.log  '''
    try:
        print command
        output = os.popen(command)
        ret =  output.read()
        return 0, ret
    except:
        return 1,0

def putBlockNo(blocknumber):
    command = '''echo "%d" >> ./block.log  '''%blocknumber
    try:
        print command
        output = os.popen(command)
        return 0
    except:
        return 1

if __name__ == '__main__':
    os.system(''' date >> /tmp/new.log ''')


    import socket
    import time

    ip_port = ('127.0.0.1',9999)
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    sk.bind(ip_port)

    #time.sleep(30000)
    #run()
    #putBlockNo(112);
    #pdb.set_trace()
    err, complete = getBlockNo()
    print err,complete
    err, new = getCount()
    print err, new

    ibegin = int(complete)+1
    iend =int(new)-5
    for i in range(ibegin, iend):
    #for i in range(int(complete), int(new)-6):
#        getHash(i)
        error ,hash = getHash(i)
        if error:
            print "error getHash"
        print hash

        error,block = getBlock(hash)
        if error:
            print "error getBlock"

        #print block

        putDB(block)
        numberLast = int(i)
        putBlockNo(numberLast)

