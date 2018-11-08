import re

searcher = re.compile('<(\d+)>')

f =open('vars.txt')
lines = f.readlines()
f.close()
vars = map(lambda y: y[0], map(lambda x: x.strip().split(';'), lines))

pos = []
for v in vars:
    match = searcher.search(v)
    if match:
        pos.append(match.group(1))

types = []
names = []

for v in vars:
    fst, typename = v.split(':')
    types.append(typename)
    fsplit =  re.split('\s+', fst)
    print fsplit
    names.append(fsplit[1])
    
    
f.close()

f = open('varlist.txt','w')
for i in range (0, len(pos)):
    print '{0}, {1}, {2}'.format(names[i],pos[i],types[i])
    f.write('{0}, {1}, {2}\n'.format(names[i],pos[i],types[i]))


