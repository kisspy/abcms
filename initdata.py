# -*- coding: cp936 -*-

from models import A,B,C

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
                    # 当作全书的书名录入, 请注意只录一行, 不要弄多行, 且必须弄一行标题, 不然后面的都挂了
                    a = A(title=last_chapter_title)
                    a.save()
                else:
                    b=B(parent= a, title=last_chapter_title)
                    b.save()
                    #b=B.select().where(B.title==last_chapter_title, B.parent==a).get()
                    for article_title in articles:
                        c=C(title=article_title, parent=b, content='')
                        c.save()
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
        for article_title in articles:
            c=C(title=article_title, parent=b, content='')
            c.save()
        print 'chapter_title', last_chapter_title
        print 'articles','\n    '.join(articles)

