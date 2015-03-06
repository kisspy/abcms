# -*- coding: cp936 -*-
#http://stackoverflow.com/questions/9816603/range-is-too-large-python/9833011
import itertools
#xrange = lambda stop: iter(itertools.count().next, stop)


def custom_range(start=0,stop=None,step=1):
    '''xrange in python 2.7 fails on numbers larger than C longs.
    we write a custom version'''
    if stop is None:
        #handle single argument case. ugly...
        stop = start
        start = 0
    i = start
    while i < stop:
        yield i
        i += step

xrange=custom_range


from time import clock as now

def exectime(func):
    def newFunc(*args, **kwrds):
        start = now()
        back = func(*args, **kwrds)
        finish = now()
        print "{%.3fs} cost by @%s" % (finish - start,func.__name__)
        return back
    return newFunc
from time import clock as now


DEBUG=False


def prettify(func):
    def innerfunc(*args, **kwrds):
        haoma=args[0]
        back = func(*args, **kwrds)
        if DEBUG:
            print haoma, func.__name__, ':',back
        #if back:
        #    print args.replace(pattern,'[%s]'%pattern)
        #else:
        #    print
        return back
    return innerfunc


def save_haomas(haomas):
    with open('haoma.txt','a') as ff:
        ff.write('\n'.join(haomas))
        ff.write('\n')

#本文档仅仅生成5位数到10位数之间的靓号
#11位数在中国是手机号码段, 很多有保留
#
lianghao={}

haoma_repeat  ='ABCDEFGHIJ'
haoma_continue='0123456789'

#单个数字重复
A=[x for x in haoma_continue]
AA=[x*2 for x in haoma_continue] #价值不高, 太多了
AAA=[x*3 for x in haoma_continue]
AAAA=[x*4 for x in haoma_continue]
AAAAA=[x*5 for x in haoma_continue]
AAAAAA=[x*6 for x in haoma_continue]
AAAAAAA=[x*7 for x in haoma_continue]
AAAAAAAA=[x*8 for x in haoma_continue]
AAAAAAAAA=[x*9 for x in haoma_continue]
AAAAAAAAAA=[x*10 for x in haoma_continue]

lianghao['A']=A
lianghao['AA']=AA
lianghao['AAA']=AAA
lianghao['AAAA']=AAAA
lianghao['AAAAA']=AAAAA
lianghao['AAAAAA']=AAAAAA
lianghao['AAAAAAA']=AAAAAAA
lianghao['AAAAAAAA']=AAAAAAAA
lianghao['AAAAAAAAA']=AAAAAAAAA
lianghao['AAAAAAAAAA']=AAAAAAAAAA

#两个数字重复
AB=[x+y for x in A for y in A if x!=y]
ABAB=[x*2 for x in AB]
ABABAB=[x*3 for x in AB]
ABABABAB=[x*4 for x in AB]
ABABABABAB=[x*5 for x in AB]

save_haomas(AB)
save_haomas(ABAB)
save_haomas(ABABAB)
save_haomas(ABABABAB)
save_haomas(ABABABABAB)



AABB=[x+y for x in AA for y in AA if x!=y]
AABBAABB=[x*2 for x in AABB]


ABBA= [x+y for x in AB for y in AB if x==y[::-1]]
ABBAABBA=[x*2 for x in ABBA]


AAAAB=[x+y for x in AAAA for y in A if x[-1]!=y]
print AAAAB

AAABB=[x+y*2 for x in AAA for y in A if x[-1]!=y]
print AAABB

AAAABB=[x+y*2 for x in AAAA for y in A if x[-1]!=y]
print AAAABB

#三个数字
ABC= [x+y+z for x in A for y in A for z in A if x!=y and y!=z and x!=z]
ABCABC=[x*2 for x in ABC]
ABCABCABC=[x*3 for x in ABC]

ABAC=[x+y for x in AB for y in AB if x[0]==y[0] and x[1]!=y[1]]
ABACABAC=[x*2 for x in ABAC]

AABBCC=[x+y+z for x in AA for y in AA for z in AA if x!=y and y!=z and x!=z]
ABCCBA=[x+y for x in ABC for y in ABC if x==y[::-1]]



#四个数字
ABCD = [x+y+z+o for x in A for y in A for z in A for o in A if x!=y and y!=z and x!=z and x!=o and y!=o and z!=o]
ABCDABCD=[x*2 for x in ABCD]
ABCDDCBA=[x+y for x in ABCD for y in ABCD if x==y[::-1]]
#print ABCDDCBA

ABCABD=[x+y for x in ABC for y in ABC if x[0:2]==y[0:2] and x[-1]!=y[-1]]


#五个数字
ABCDE = [x+y+z+o+p for x in A for y in A for z in A for o in A for p in A if x!=y and y!=z and x!=z and x!=o and y!=o and z!=o and x!=p and y!=p and z!=p and o!=p]
#print ABCDE

#########################################################################################################
#连续自然数
haoma_list='0123456789a'

#单个数字重复
A=[x for x in haoma_list]
A1A2A3=[(x+y+z).replace('a','0') for x in A for y in A for z in A if int(x,16)+1==int(y,16) and int(y,16)+1==int(z,16)]
A1A2A3A1A2A3=[x*2 for x in A1A2A3]
#print A1A2A3
#连续四个自然数ABCD, 例如1234, 价值高
A1A2A3A4=[(x+y+z+o).replace('a','0') for x in A for y in A for z in A for o in A if int(x,16)+1==int(y,16) and int(y,16)+1==int(z,16) and int(z,16)+1==int(o,16)]
A1A2A3A4A1A2A3A4=[x*2 for x in A1A2A3A4]
print A1A2A3A4

#连续五个自然数
A1A2A3A4A5=[(x+y+z+o+p).replace('a','0') for x in A for y in A for z in A for o in A for p in A if int(x,16)+1==int(y,16) and int(y,16)+1==int(z,16) and int(z,16)+1==int(o,16) and int(o,16)+1==int(p,16)]
A1A2A3A4A5A1A2A3A4A5=[x*2 for x in A1A2A3A4A5]
print A1A2A3A4A5
print A1A2A3A4A5A1A2A3A4A5[:30]

'''
#连续六个自然数
A1A2A3A4A5A6=[(x+y+z+o+p+q).replace('a','0') for x in A for y in A for z in A for o in A for p in A for q in A if int(x,16)+1==int(y,16) and int(y,16)+1==int(z,16) and int(z,16)+1==int(o,16) and int(o,16)+1==int(p,16) and int(p,16)+1==int(q,16)]
print A1A2A3A4A5A6

#连续七个自然数
A1A2A3A4A5A6=[(x+y+z+o+p+q).replace('a','0') for x in A for y in A for z in A for o in A for p in A for q in A if int(x,16)+1==int(y,16) and int(y,16)+1==int(z,16) and int(z,16)+1==int(o,16) and int(o,16)+1==int(p,16) and int(p,16)+1==int(q,16)]
print A1A2A3A4A5A6

#连续六个自然数
A1A2A3A4A5A6=[(x+y+z+o+p+q).replace('a','0') for x in A for y in A for z in A for o in A for p in A for q in A if int(x,16)+1==int(y,16) and int(y,16)+1==int(z,16) and int(z,16)+1==int(o,16) and int(o,16)+1==int(p,16) and int(p,16)+1==int(q,16)]
print A1A2A3A4A5A6

#连续六个自然数
A1A2A3A4A5A6=[(x+y+z+o+p+q).replace('a','0') for x in A for y in A for z in A for o in A for p in A for q in A if int(x,16)+1==int(y,16) and int(y,16)+1==int(z,16) and int(z,16)+1==int(o,16) and int(o,16)+1==int(p,16) and int(p,16)+1==int(q,16)]
print A1A2A3A4A5A6
'''

##############################################################################################
# 生日靓号
#
PEOPLE_MAX_AGE=10 #人类最大寿命
PEOPLE_AVG_AGE=5  #人类平均寿命

import time, datetime
now=datetime.datetime.now()

min_year=now.year-PEOPLE_MAX_AGE
max_year=now.year+PEOPLE_AVG_AGE*2 - PEOPLE_MAX_AGE
print min_year,max_year

months=[1,2,3,4,5,6,7,8,9,10,11,12]
month_days={
    1:31,
    2:28,
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31
}
leapyear_month_days=month_days.copy()

leapyear_month_days[2]=29



def isLeapYear(year):
    if year % 2 !=0:
        return False

    if (year % 4 == 0 and (year%100 != 0 or year % 400 == 0) ) :
        return True
    else :
        return False

#for x in xrange(min_year,max_year):
#    print x, isLeapYear(x)


ALL_BIRTHDAY=[]

for y in xrange(min_year,max_year):
    for m in months:
        if isLeapYear(y):
            days=leapyear_month_days[m]
        else:
            days=month_days[m]
        tmp=[]
        for d in xrange(1, days+1):
            if m<10:
                if d<10:
                    ALL_BIRTHDAY.append('%d%d%d' % (y,m,d))
                    ALL_BIRTHDAY.append('%d%d%02d' % (y,m,d))
                    ALL_BIRTHDAY.append('%d%02d%d' % (y,m,d))
                    ALL_BIRTHDAY.append('%d%02d%02d' % (y,m,d))
                else:
                    ALL_BIRTHDAY.append('%d%d%d' % (y,m,d))
                    ALL_BIRTHDAY.append('%d%02d%d' % (y,m,d))
            else:
                if d<10:
                    ALL_BIRTHDAY.append('%d%d%d' % (y,m,d))
                    ALL_BIRTHDAY.append('%d%d%02d' % (y,m,d))
                else:
                    ALL_BIRTHDAY.append('%d%d%d' % (y,m,d))

        #    tmp.append('%d%d%d' % (y,m,d))
        #    tmp.append('%d%d%2d' % (y,m,d))
        #    tmp.append('%d%2d%d' % (y,m,d))
        #    tmp.append('%d%2d%2d' % (y,m,d))
        #tmp=list(set(tmp))
        #BIRTHDAY.extend(tmp)

#print ALL_BIRTHDAY
#月和日中无零
# 2013年3月2日, 表示为201332, 不表示为2013032, 不表示为2013302, 不表示为20130302

BIRTHDAY_NO_ZERO=[]

for y in xrange(min_year,max_year):
    for m in months:
        if isLeapYear(y):
            days=leapyear_month_days[m]
        else:
            days=month_days[m]
        tmp=[]
        for d in xrange(1, days+1):
            BIRTHDAY_NO_ZERO.append('%d%d%d' % (y,m,d))
#print BIRTHDAY_NO_ZERO

##月日均带零, 8位 20130302法
BIRTHDAY08=[]

for y in xrange(min_year,max_year):
    for m in months:
        if isLeapYear(y):
            days=leapyear_month_days[m]
        else:
            days=month_days[m]
        tmp=[]
        for d in xrange(1, days+1):
            BIRTHDAY08.append('%d%02d%02d' % (y,m,d))


#print ABCDABCD
for length in xrange(5, 11):
    haoma=[]
    i=0
    while i < length:
        haoma.append(haoma_repeat[i])
        i=i+1
    print ''.join(haoma)

#lll=['aa','ab','ba','bb']
#
#for x in lll:
#    for y in lll:
#        if (x+y).count('a')==2:
#            print x+y
def isHead(haoma, pattern):
    if haoma.startswith(pattern):
        return True
    else:
        return False

def isTail(haoma, pattern):
    if haoma.startswith(pattern):
        return True
    else:
        return False

def isRule(haoma, rule_haoma_pattern_list):
    result=False
    pattern=''

    for p in rule_haoma_pattern_list:
        if p in haoma:
            result=True
            pattern=p
            break
        else:
            continue
    return result, pattern

#@prettify
def isAA(haoma):
    return isRule(haoma, AA)

def isAAA(haoma):
    return isRule(haoma, AAA)

def isAAAA(haoma):
    return isRule(haoma, AAAA)

def isAAAAA(haoma):
    return isRule(haoma, AAAAA)

def isAAAAAA(haoma):
    return isRule(haoma, AAAAAA)

#@prettify
def isAABB(haoma):
    return isRule(haoma, AABB)

def isABAB(haoma):
    return isRule(haoma, ABAB)

def isABBA(haoma):
    return isRule(haoma, ABBA)

def isABC(haoma):
    return isRule(haoma, ABC)

def isABABAB(haoma):
    return isRule(haoma, ABABAB)

def isABCABC(haoma):
    return isRule(haoma, ABCABC)

def isABCABD(haoma):
    return isRule(haoma, ABCABD)

def isABABABAB(haoma):
    return isRule(haoma, ABABABAB)

def isAABBCCDD(haoma):
    return isRule(haoma, AABBCCDD)



def isABCDABCD(haoma):
    return isRule(haoma, ABCDABCD)

d={
    'isAA':0,
    'isAAA':0,
    'isAAAA':0,
    'isAAAAA':0,
    'isAABB':0,
    'isAABBCC':0,
}

for x in xrange(10**5, 10**6):
    #if isAA(str(x)):
    #    d['isAA']=d.get('isAA',0)+1
    result,pattern=isAAA(str(x))
    if result:
        d['isAAA']=d.get('isAAA',0)+1

    result,pattern=isAAAA(str(x))
    if result:
        d['isAAAA']=d.get('isAAAA',0)+1

    result,pattern=isAAAAA(str(x))
    if result:
        d['isAAAAA']=d.get('isAAAAA',0)+1
        #print x
    result,pattern=isAABB(str(x))
    if result:
        d['isAABB']=d.get('isAABB',0)+1

    result,pattern=isABAB(str(x))
    if result:
        d['isABAB']=d.get('isABAB',0)+1

print d

