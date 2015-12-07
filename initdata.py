# -*- coding: cp936 -*-
#from models import *
from models import A,B,C
print '\n'.join(dir())
titles=[
u'斗罗大陆',
u'天火大道',
u'斗罗大陆漫画',
u'斗罗大陆续集',
u'斗罗大陆2绝世唐门'
]

#for title in titles:
#    a=A(title=title)
#    a.save()

chapters=[
u'第一集 斗罗世界',
u'第二集 第一魂环',
u'第三集 怪物学院',
u'第四集 史莱克七怪',
u'第五集 星斗森林',
u'第六集 外附魂骨',
u'第七集 斗魂大战',
u'第八集 皇斗战队',
u'第九集 黄金铁三角',
u'第十集 冰火炼金身',
u'第十一集 大力神',
u'第十二集 XXX',
u'第十三集 第四魂环',
u'第十四集 象甲宗',
u'第十五集 破幻魔瞳',
u'第十六集 绝技融合',
u'第十七集 有凤来仪',
u'第十八集 三块魂骨',
u'第十九集 紫极神光',
u'第二十集 杀戮之都',
u'第二十一集 唐三的第三魂骨',
u'第二十二集 昊天宗',
u'第二十三集 猎魂行动',
u'第二十四集 异界唐门',
u'第二十五集 单属宗族',
u'第二十六集 小舞复活',
u'第二十七集 庚辛城',
u'第二十八集 天斗宫变',
u'第二十九集 海神岛',
u'第三十集 瀚海城',
u'第三十一集 登陆海神岛',
u'第三十二集 海神的考验',
u'第三十三集 七怪真身',
u'第三十四集 唐三八环',
u'第三十五集 挑战，封号斗罗',
u'第三十六集 海神斗罗',
u'第三十七集 海神三叉戟',
u'第三十八集 复活吧！我的爱人',
u'第三十九集 重返昊天',
u'第四十集 大战初始',
u'第四十一集 血战嘉陵关',
u'第四十二集 天使之神',
u'第四十三集 唐三战天使',
u'第四十四集 百万年魂环',
u'第四十五集 海神传承',
u'第四十六集 海神唐三',
u'第四十七集 天使罗刹',
u'第四十八集 完美融合（大结局）'

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
                    # 当作全书的书名录入, 请注意只录一行, 不要弄多行, 且必须弄一行标题, 不然后面的都挂了
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

