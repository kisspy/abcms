# -*- coding: cp936 -*-
#from models import *
from models import A,B,C
print '\n'.join(dir())
titles=[
u'���޴�½',
u'�����',
u'���޴�½����',
u'���޴�½����',
u'���޴�½2��������'
]

#for title in titles:
#    a=A(title=title)
#    a.save()

chapters=[
u'��һ�� ��������',
u'�ڶ��� ��һ�껷',
u'������ ����ѧԺ',
u'���ļ� ʷ�����߹�',
u'���弯 �Ƕ�ɭ��',
u'������ �⸽���',
u'���߼� �����ս',
u'�ڰ˼� �ʶ�ս��',
u'�ھż� �ƽ�������',
u'��ʮ�� ����������',
u'��ʮһ�� ������',
u'��ʮ���� XXX',
u'��ʮ���� ���Ļ껷',
u'��ʮ�ļ� �����',
u'��ʮ�弯 �ƻ�ħͫ',
u'��ʮ���� �����ں�',
u'��ʮ�߼� �з�����',
u'��ʮ�˼� ������',
u'��ʮ�ż� �ϼ����',
u'�ڶ�ʮ�� ɱ¾֮��',
u'�ڶ�ʮһ�� �����ĵ������',
u'�ڶ�ʮ���� �����',
u'�ڶ�ʮ���� �Ի��ж�',
u'�ڶ�ʮ�ļ� �������',
u'�ڶ�ʮ�弯 ��������',
u'�ڶ�ʮ���� С�踴��',
u'�ڶ�ʮ�߼� ������',
u'�ڶ�ʮ�˼� �춷����',
u'�ڶ�ʮ�ż� ����',
u'����ʮ�� 嫺���',
u'����ʮһ�� ��½����',
u'����ʮ���� ����Ŀ���',
u'����ʮ���� �߹�����',
u'����ʮ�ļ� �����˻�',
u'����ʮ�弯 ��ս����Ŷ���',
u'����ʮ���� ������',
u'����ʮ�߼� ���������',
u'����ʮ�˼� ����ɣ��ҵİ���',
u'����ʮ�ż� �ط����',
u'����ʮ�� ��ս��ʼ',
u'����ʮһ�� Ѫս�����',
u'����ʮ���� ��ʹ֮��',
u'����ʮ���� ����ս��ʹ',
u'����ʮ�ļ� ������껷',
u'����ʮ�弯 ���񴫳�',
u'����ʮ���� ��������',
u'����ʮ�߼� ��ʹ��ɲ',
u'����ʮ�˼� �����ںϣ����֣�'

]
#a=A.select().where(A.id==1).get()
#for title in chapters:
#    b=B(parent= a, title=title)
#    b.save()

with open('chapters.txt','r') as ff:
    chapter_flag=False
    articles=[]
    chapter_title=''
    last_chapter_title=''
    for line in ff.readlines():
        line = line.strip('\n')
        line = line.decode('gbk')
        if line=='':
            continue
        if line[0] != '\t':
            chapter_flag=True
            chapter_title=line

            if last_chapter_title:
                if not articles:
                    # ����ȫ�������¼��, ��ע��ֻ¼һ��, ��ҪŪ����, �ұ���Ūһ�б���, ��Ȼ����Ķ�����
                    a = A(title=last_chapter_title)
                    a.save()
                #b=B.select().where(B.title==last_chapter_title, B.parent==a).get()
                #for article_title in articles:
                #    c=C(title=article_title, parent=b, content='')
                #    c.save()
                print 'chapter_title', last_chapter_title
                print 'articles','\n    '.join(articles)
            articles=[]
            last_chapter_title=chapter_title
        else:
            chapter_flag=False
            articles.append(line.strip()) #cut tab key
    if last_chapter_title:
        #b=B.select().where(B.title==last_chapter_title, B.parent==a).get()
        #for article_title in articles:
        #    c=C(title=article_title, parent=b, content='')
        #    c.save()
        print 'chapter_title', last_chapter_title
        print 'articles','\n    '.join(articles)

