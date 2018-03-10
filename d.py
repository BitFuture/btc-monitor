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

if __name__ == '__main__':
    conn = MySQLdb.Connect(host='localhost',user='root',passwd='',db='bitcoin',port=3306,charset = 'utf8')
    cur = conn.cursor()
    #time = cur.execute("select now()")
    #print time
    
    jsondata = file("./c.out");
    s = json.load(jsondata)
    test=s   
    python_to_json = json.dumps(test,ensure_ascii=False)
    json_to_python = json.loads(python_to_json)
    no=0
    import pdb
    #pdb.set_trace()
    total = len(json_to_python['result']['tx'])
    for no in range(0, total):
        #print "begin processing transaction %d of  %d------------"%(no,total) 
        #print json_to_python['result']['tx'][no]
        atr = json_to_python['result']['tx'][no]
       # print "txid = %s"%atr['txid']
        txid = atr['txid']
        print txid
       # print atr['vout'][0]['value']
        value = atr['vout'][0]['value']
        #print atr['vout'][0]['scriptPubKey']['hex']
        #print atr['vout'][0]['scriptPubKey']['asm']
        #print atr['vout'][0]['scriptPubKey']['type']
        #if has_key( atr['vout'][0]['scriptPubKey'], 'addresses'):
        #    print atr['vout'][0]['scriptPubKey']['addresses']
        address=''
        addresscount=0
        try: 
            lout = len(atr['vout'])
            print "---------------------------%d---"%lout
            print 
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
            sql = '''insert into tx_out(tx_out_value, txid, tx_out_address)  values ("%s",  "%s", "%s");'''%(value,txid,address[addressno])
            print sql
#            if txid=="7b59aa3c7e71a20ab0498c852017b077cb2d3291123b9008e339025b8fa2a79f":
#                print "found"
            #ok = cur.execute(sql)
    conn.commit()    
  #  print "----------------------------------------"
  #  print len(json_to_python['result']['tx'][1]['vout'])
