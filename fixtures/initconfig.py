# -*- coding: cp936 -*-
import sys
import os
import hashlib

from models import Config
def process(filepath, verbose=False):
    if not os.path.exists(filepath):
        raise Exception('filepath(%s) does not exists!' % filepath)

    configs=dict(sitename='ABCcms', siteurl='http://localhost')
    with open(filepath,'r') as ff:
        for line in ff.readlines():
            line = line.strip('\n')
            line = line.decode('gbk')
            if line=='':
                continue
            if len(line.split('='))==2:
                key, value=line.split('=')
                configs[key]=value
            else:
                print 'Error Data',line
    print configs
    config=Config(**configs)
    config.save()

if __name__ == '__main__':
    print 'sys.argv:', sys.argv
    filepath=None
    if len(sys.argv)>=3:
        filepath=sys.argv[1]
        verbose=bool(sys.argv[1])
    elif len(sys.argv)==2:
        filepath=sys.argv[1]
        verbose=False
    #print filepath, verbose
    if filepath:
        process(filepath, verbose=verbose)
    #print filepath, verbose
