import json


Criteria = [['in0', [0.9, 1.0]],
            ['in1', [1.1, 1.3]],
            ['in2', [2.0, 2.5]],
            ['in3', [2.5, 2.8]],
            ['in4', [1.8, 2.0]],
            ['in5', [1.8, 2.0]],
            ['in6', [1.8, 2.0]],
            ['3VSB', [3.0, 3.5]],
            ['Vbat', [3.4, 3.6]]]


aaa = ['Vbat']


with open('sensors.json') as f:
	data = json.load(f)



data = data[list(data)[0]]


checkList = list(data)
checkList = checkList[1:10]
n = range(len(checkList))



for i in n:
    j = checkList[i]
    a = list(data.get(j))[0]
    value = data.get(j).get(a)
    a_min = list(data.get(j))[1]
    a_max = list(data.get(j))[2]
    #minimize = data.get(j).get(a_min)
    #maximize = data.get(j).get(a_max)
    #print(minimize, maximize)
    
    #print(a, value, sep = ': ')
      
    
    minimize = Criteria[i][1][0]
    maximize = Criteria[i][1][1]
    #print(minimize, maximize)
    if value > minimize and value < maximize:
        #print('Pass')
        pass
    else:
        print('Fail')
        break
    


'''
for i in checkList:     # i = ['in0', 'in1', ..., 'Vbat']
    a = list(data.get(i))[0]
    print(a, data.get(i).get(a), sep=': ')
'''

