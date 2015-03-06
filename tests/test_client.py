# -*- coding: cp936 -*-
from client import FakeClient

c=FakeClient(base_url='http://localhost:9000',debug=0)
#print c.get_xsrf()
##c.login()
##c.get('http://localhost:8888/bbs/f/1')
#c.get('http://localhost:8888/bbs/f/1/newthread')
###for x in xrange(304,400):
###    c.new_thread(title=u'fadsf %03d' % x ,content=u'sssss %s' % x )
#c.new_thread(title=u'fadsf 98',content=u'sssss 98' )

root=r'D:\archives\wwwspider\spiders\2'
#root=r'D:\archives\django\csdn\新建文件夹'
root=r'D:\archives\django\cnblogs\22'

posted_root=r'F:\Projects\MyProjects\webbot\data\kisspy'

import os,shutil
import datetime, time,random
i=0
for x in os.listdir(root):
    i=i+1
    print i
    
    if not x.lower().endswith('.txt'):
        continue
    with open(os.path.join(root,x),'r') as ff:
        try:
            txt=ff.read().decode('utf-8')
        except UnicodeDecodeError:
            try:
                txt=ff.read().decode('gb18030')
            except UnicodeDecodeError:
                txt=''
                print 'UnicodeDecodeError',x

        if txt:
            lines=txt.split('\n')
            lll=[]
            for line in lines:
                line=line.rstrip()
                lll.append(line)

            lines=lll
            
            title=lines[0]
            
            #content='\n'.join(lines[1:])
            content='\n\n'.join(lines[2:])
            #print '**',title
            
            c.new_thread(title=title ,content=content,fid=2)
            print 'POSTED!',x
            posted=1
            
        else:
            posted=0
            print 'Failed!',x
    #shutil.move(os.path.join(root,x),os.path.join(posted_root,str(int(time.time()))+'-'+x))
    if posted:
        #os.remove(os.path.join(root,x))
        shutil.move(os.path.join(root,x),os.path.join(posted_root,x))
    #print 'Please Wait, It is still running'
    waiting=random.randint(10,21)
    #for x in xrange(waiting):
    #    print '.',
    #    time.sleep(1)
    time.sleep(waiting)
    print
print 'Done!'
