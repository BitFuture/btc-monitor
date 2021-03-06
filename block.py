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
import sqlite3
import traceback


def dump():
    isotimeformat='%Y%m%d-%H%M%S'
    timestring=time.strftime(isotimeformat,time.localtime(time.time()))
    dumpfile = "./%s.dump"%timestring
    #print dumpfile
    f=open(dumpfile,'a')
    traceback.print_exc(file=f)
    f.flush()    
    f.close()


def config():
    try:
        config_string=open("./config.json").read()
        config = json.loads(config_string)
        #print config
        
    except Exception as e:
        print "config.json Error!!!"
        print e
        dump()
        sys.exit(1)
    return config

AddressSet =set()
def InitAddressSet():
    '''
    #conn = MySQLdb.Connect(host='192.168.1.144',user='root',passwd='',db='bitcoin',port=3306,charset = 'utf8')
    '''
    conn = MySQLdb.Connect(host=config()['dbserverip'],user=config()['dbuser'],passwd=config()['dbpassword'] ,db=config()['dbservername'],port=3306,charset = 'utf8')
    cursor = conn.cursor()

    sql = u"SELECT user_address   from user_address;"
    result =0
    try:
        n = cursor.execute(sql)
        itemset = cursor.fetchall()
        for item in itemset:
            print item[0]
            AddressSet.add(item[0])
        result =1
    except Exception , e:
        print Exception,":" ,e
        result =  -1
    cursor.close()
    conn.close()
    return result

def IsPrivateAddress(a):
    #return True
    return a in AddressSet

def getCount():
    #command = '''curl  -s  --user dylan:123456 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockcount", "params": [] }' -H 'content-type: application/json;' http://192.168.1.128:8332  '''
    #print command
    command = '''curl  -s  --user %s:%s --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockcount", "params": [] }' -H 'content-type: application/json;' %s  '''%(config()['btcuser'], config()['btcpassword'],config()['btcserver'])
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
    #command = '''curl -s --user dylan:123456 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [%s] }' -H 'content-type: application/json;' http://192.168.1.128:8332 '''%blockcount
    command = '''curl -s --user %s:%s --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [%s] }' -H 'content-type: application/json;' %s '''%(config()['btcuser'], config()['btcpassword'],blockcount, config()['btcserver'])
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
    #command = '''curl -s --user dylan:123456 --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["%s", 2] }' -H 'content-type: application/json;' http://192.168.1.128:8332 '''%(hash)
    command = '''curl -s --user %s:%s --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["%s", 2] }' -H 'content-type: application/json;' %s '''%( config()['btcuser'], config()['btcpassword'],hash, config()['btcserver'])
    print command
    try:
        output = os.popen(command)
        ret =  output.read()
        ret_json =  json.loads(ret)
        block =ret_json['result']
        return 0, block

    except:
        return 1,''


def putDB( block):
#    conn = MySQLdb.Connect(host='localhost',user='root',passwd='',db='bitcoin',port=3306,charset = 'utf8')
    conn = MySQLdb.Connect(host=config()['dbserverip'],user=config()['dbuser'],passwd=config()['dbpassword'] ,db=config()['dbservername'],port=3306,charset = 'utf8')    
    cur = conn.cursor()

    #pdb.set_trace()
    python_to_json = json.dumps(block, ensure_ascii=False)
    json_to_python = json.loads(python_to_json)

    height =0
    try:
        height = json_to_python['height']
    except:
        print "height exception...."
        sys.exit(1)

    blockfilename="./block%d.json"%height
    with open(blockfilename,"w") as f:
        json.dump(block,f)

    txs = json_to_python['tx']
    txcount = len(txs)

    for nth in range(0, txcount):
        tx = txs[nth]
        txid = tx['txid']
        value = 0
        inlen = len(tx['vin'])
        refsequence=0
        refvout=''
        for inloop in range(0, inlen):
            if tx['vin'][inloop].has_key("sequence"):
                refsequence =tx['vin'][inloop]["sequence"]
            if tx['vin'][inloop].has_key('vout'):
                refvout = tx['vin'][inloop]['vout']
                #print type(refvout)
                #print "refvout = %s"%refvout
                #if refvout=='79':
                    #pdb.set_trace()
                #    print refvout
            else:
                continue
            if tx['vin'][inloop].has_key('txid'):
                reftxid = tx['vin'][inloop]['txid']
                #print type(reftxid)
                #print "reftxid=%s"%reftxid
                #if reftxid == '7b59aa3c7e71a20ab0498c852017b077cb2d3291123b9008e339025b8fa2a79f':
                #    pdb.set_trace()
            else:
                continue
            mark = 0
            try:
                #if reftxid =="a4e9e59a2ada3d6a3cfce0d0a8e0c2d9970d4b29d1e0e0def94ab62de68e30d5":
                #   pdb.set_trace()
                sqlCmd='''select tx_out_address from tx_out where txid like "%s" and tx_out_index like "%s"; '''%(reftxid,refvout)
                #print sqlCmd
                n = cur.execute(sqlCmd)
                #print n
                itemset = cur.fetchall()
                #print type(itemset)
                for item in itemset:
                    print item[0]
                    if  IsPrivateAddress(item[0]):
                        mark = 1    #should mark this is within inner addresses.
                        #if mark:
                        sql = '''insert into tx_in(txid,ref_txid, tx_in_address,tx_height,tx_vout)  values ("%s","%s", "%s", "%s",  "%s");'''%(txid,reftxid,item[0],height,refvout)
                        print sql
                        ok=0
                        try:
                            ok = cur.execute(sql)
                        except Exception as e:
                            print e
                            #print dir(e)
                            #return 1
                            #pdb.set_trace()
                            print "serious bug !!! insert  result =%d : %s "%(ok ,sql)
                            pass #sys.exit(1)
            except Exception as e:
                print e
                pass

    try:
        #pdb.set_trace()
        conn.commit()
    
    except Exception as e:
        print e
        #pdb.set_trace()
        print "serious bug ,commit error!!! height = %s"%height
        sys.exit(1)


    #print "sys exit"
    #sys.exit(0)


    #it is turn to preocess the vout of this block
    for nth in range(0, txcount):
        tx = txs[nth]
        txid = tx['txid']
        value = 0

        outlen = len(tx['vout'])
        for outloop in range(0, outlen):
            n = tx['vout'][outloop]['n']
            value = tx['vout'][outloop]['value']

            address=''
            addresscount=0
            innerloopcount=0

            try:
                if  tx['vout'][outloop]['scriptPubKey'].has_key('addresses'):
                    addresscount=len(tx['vout'][outloop]['scriptPubKey']['addresses'])
                #print "@@@@address count %d"%addresscount
                innerloopcount = min(addresscount,1 )
            except:
                print "outloop exception  txid = %s"%txid
                pass

            for addressno in range(0, innerloopcount):
                address = tx['vout'][outloop]['scriptPubKey']['addresses'][addressno]
                if not IsPrivateAddress(address) :
                    continue
                sql = '''insert into tx_out(tx_out_value, txid, tx_out_address,tx_height, tx_out_index)  values ("%s",  "%s", "%s", "%s", "%s");'''%(value,txid,address,height,n)
                #print sql
                ok=0
                try:
                    ok = cur.execute(sql)
                except Exception as e:
                    print e
                    #print dir(e)
                    pass
                    #return 1
                    #log(e.message)
                print " %d  %s ++++++++++++++++++++++++++++++"%(ok ,sql)
    conn.commit()
    return 0

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
    #pdb.set_trace()
    command = '''tail -n 1 /develop/btc2/block.log  '''
    try:
        print command
        output = os.popen(command)
        ret =  output.read()
        return 0, ret
    except:
        return 1,0

def putBlockNo(blocknumber):
    print  "+++++++++++++++++++finishing  block   %d+++++++++++++++++++++++++++"%blocknumber
    command = '''echo "%d" >> /develop/btc2/block.log  '''%blocknumber
    try:
        print command
        output = os.popen(command)
        return 0
    except:
        return 1

if __name__ == '__main__':
    os.system(''' date >> /develop/btc2/cron.run.log ''')
    #print config()['dbserverip']
    
    import socket
    import time

    ip_port = ('127.0.0.1',9999)
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    sk.bind(ip_port)

    InitAddressSet()
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

        error = putDB( block)
        if not error:
            numberLast = int(i)
            putBlockNo(numberLast)
        #log("complete run")
