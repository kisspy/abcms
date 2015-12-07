# -*- coding: cp936 -*-
import sys
import os
import hashlib

from models import User
def process(filepath, verbose=False):
    if not os.path.exists(filepath):
        raise Exception('filepath(%s) does not exists!' % filepath)

    with open(filepath,'r') as ff:
        for line in ff.readlines():
            line = line.strip('\n')
            line = line.decode('gbk')
            if line=='':
                continue
            if len(line.split('/'))==3:
                username, email, password=line.split('/')
                user=User(username=username, email=email, password=hashlib.sha1(password).hexdigest())
                user.save()
            else:
                print 'Error Data',line

if __name__ == '__main__':
    print 'sys.argv:', sys.argv
    if len(sys.argv)>=3:
        filepath=sys.argv[1]
        verbose=bool(sys.argv[1])
    elif len(sys.argv)==2:
        filepath=sys.argv[1]
        verbose=False
    #print filepath, verbose
    process(filepath, verbose=verbose)
    #print filepath, verbose