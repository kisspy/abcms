from client import FakeClient

c=FakeClient(base_url='http://localhost:9000',debug=0)

for x in xrange(1000):
    #print c.get('http://www.qb.vc/hm?code=unkwon&data=MA__')
    print c.get('http://localhost:9000/hm?code=unkwon&data=MA__')
