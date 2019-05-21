import trafaret as t
c = t.Dict({t.String: (t.String)})
z = {'a': 'k'}
#k = c.check({'a': ['f']})
k = c.check(z)
print(k)