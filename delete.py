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


def getBlockNo():
    command = '''tail -n 1 ./block.log  '''
    try:
        print command
        output = os.popen(command)
        ret =  output.read()
        return 0, ret
    except:
        return 1,0


if __name__ == '__main__':
    os.system(''' date >> /develop/btc2/cron.run.delete.log ''')
    import socket
    import time

    ip_port = ('127.0.0.1',9997)
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    sk.bind(ip_port)

    err, complete = getBlockNo()
    if err:
        sys.exit(0)

    todelete = int(complete) - 6*24*100
    sql = '''delete from tx_out where tx_height < %d;'''%todelete
    print sql

    conn = MySQLdb.Connect(host='localhost',user='root',passwd='',db='bitcoin',port=3306,charset = 'utf8')
    cur = conn.cursor()
#    ret = cur.execute(sql)
    conn.commit()
    #print ret
    
