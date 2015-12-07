# -*- coding: cp936 -*-

__author__ = 'Encore Hu, <huyoo353@126.com>'

import os,sys
#sys.path.insert(0,r'F:\Projects\MyProjects\abcms')
from models import db
from models import A,B,C

def process(filepath, verbose=False):
    if not os.path.exists(filepath):
        raise Exception('filepath(%s) does not exists!' % filepath)

    with open(filepath,'r') as ff:
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
                        # 当作全书的书名录入, 请注意只录一行, 不要弄多行, 且必须弄一行标题, 不然后面的都挂了
                        a = A(title=last_chapter_title)
                        a.save()
                    else:
                        b=B(parent= a, title=last_chapter_title)
                        b.save()
                        #b=B.select().where(B.title==last_chapter_title, B.parent==a).get()
                        data_source=[]
                        for article_title in articles:
                            data={
                                'title':article_title,
                                'parent':b,
                                'content':'',
                            }
                            data_source.append(data)
                        with db.atomic():
                            C.insert_many(data_source).execute()
                        if verbose:
                            print 'chapter_title', last_chapter_title
                            print 'articles','\n    '.join(articles)
                articles=[]
                last_chapter_title=chapter_title
            else:
                chapter_flag=False
                articles.append(line.strip()) #cut tab key
        if last_chapter_title:
            b=B(parent= a, title=last_chapter_title)
            b.save()
            #b=B.select().where(B.title==last_chapter_title, B.parent==a).get()
            data_source=[]
            for article_title in articles:
                data={
                    'title':article_title,
                    'parent':b,
                    'content':'',
                }
                data_source.append(data)
            with db.atomic():
                C.insert_many(data_source).execute()
            if verbose:
                print 'chapter_title', last_chapter_title
                print 'articles','\n    '.join(articles)


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
