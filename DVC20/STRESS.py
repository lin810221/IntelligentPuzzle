DataInfo = []
f = open('stress.txt', 'r')
for i in f.readlines():
    DataInfo.append(i)
f.close

print(DataInfo[1].split(' ')[-1].split('s')[0])
