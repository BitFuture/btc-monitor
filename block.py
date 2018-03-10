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


import logging
def log(msg):
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('./block.run.log')
    fh.setLevel(logging.DEBUG)
    
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # 定义handler的输出格式
    formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    # 记录一条日志
    logger.info(msg)


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


def putDB(filename_height, block):
    conn = MySQLdb.Connect(host='localhost',user='root',passwd='',db='bitcoin',port=3306,charset = 'utf8')
    cur = conn.cursor()
    #time = cur.execute("select now()")
    #print time
    blockfilename="./block%d.json"%filename_height
    #with open("./block.json","w") as f:
    with open(blockfilename,"w") as f:
        json.dump(block,f)
    #s = json.loada(jsondata)
    #test=s

    test=block
    python_to_json = json.dumps(test, ensure_ascii=False)
    json_to_python = json.loads(python_to_json)
    no=0
    #print "########################################"
    #print json_to_python
    #pdb.set_trace()
    try:
        height = json_to_python['height']
    except:
                #print "line %d  txid = %s"%(no,atr['txid'])
        print "exception...."
        #pdb.set_trace()
        sys.exit(1)
        pass
   

    #pdb.set_trace()
    total = len(json_to_python['tx']) #remove result
    for no in range(0, total):
        #print "begin processing transaction %d of  %d------------"%(no,total) 
        #print json_to_python['result']['tx'][no]
        atr = json_to_python['tx'][no] #remove result
       # print "txid = %s"%atr['txid']
        txid = atr['txid']
       # print atr['vout'][0]['value']
        value = 0 #atr['vout'][0]['value']

        outlen = len(atr['vout'])
        for outloop in range(0, outlen):

            address=''
            addresscount=0
            try:
                print atr['vout'][outloop]['scriptPubKey']['addresses']
                addresscount=len(atr['vout'][outloop]['scriptPubKey']['addresses'])
                print "@@@@address count %d"%addresscount
                address = atr['vout'][outloop]['scriptPubKey']['addresses']
                value = atr['vout'][outloop]['value']
            except:
                #print "line %d  txid = %s"%(no,atr['txid'])
                pass
            print "address count %d"%addresscount
            for addressno in range(0, addresscount):
                #sql = '''insert into tx(tx_out_value, txid, tx_address)  values ("%s",  "%s", "%s");'''%(value,txid,address[addressno])
                #sql = '''insert into tx_out(tx_out_value, txid, tx_out_address,tx_height)  values ("%s",  "%s", "%s", "%s");'''%(value,txid,address[addressno],height)
                n = atr['vout'][outloop]['n']
                sql = '''insert into tx_out(tx_out_value, txid, tx_out_address,tx_height, tx_out_index)  values ("%s",  "%s", "%s", "%s", "%s");'''%(value,txid,address[addressno],height,n)
                print sql
                ok=0
                try:
                    ok = cur.execute(sql)
                except Exception as e:
                    print e
                    #print dir(e)
                    #log(e.message)
                print "++++++++++++++++++++++++++++++sql execute %d++++++++++++++++++++++++++++++"%ok
    conn.commit()

def test_Current():
    error ,count = getCount()
    if error:
        print "error"
        sys.exit(1)
    print count;
    #pdb.set_trace()
    error ,hash = getHash(count)
    if error:
        print "error"
        sys.exit(1)
    print hash

    error,block = getBlock(hash)
    if error:
        print "error"

    #print block

    putDB(block)

def getBlockNo():
    command = '''tail -n 1 /develop/btc2/block.log  '''
    try:
        print command
        output = os.popen(command)
        ret =  output.read()
        return 0, ret
    except:
        return 1,0

def putBlockNo(blocknumber):
    print  "+++++++++++++++++++writing  block  number %d+++++++++++++++++++++++++++"%blocknumber
    command = '''echo "%d" >> /develop/btc2/block.log  '''%blocknumber
    try:
        print command
        output = os.popen(command)
        return 0
    except:
        return 1

if __name__ == '__main__':
    os.system(''' date >> /develop/btc2/cron.run.log ''')


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
            sys.exit(1)

        print hash

        error,block = getBlock(hash)
        if error:
            print "error getBlock"
            sys.exit(1)

        #print block
        if block=="":
            print "getBlock empty string"
            sys.exit(1)

        putDB(i , block)
        numberLast = int(i)
        putBlockNo(numberLast)
        log("complete run")


