import requests

REPORT = []
TestItem = []
TestResult = []
DataInfo = []

f = open('TIME.txt')
for i in f:
    DataInfo.append(i.split('\n')[0])
f.close



f = open('REPORT.txt', 'r')
for i in f:
    TestItem.append(i.split(':')[0] + ',')
    TestResult.append(i.split(':')[1].split('\n')[0]) 
f.close



def LoadData(TestItem, TestResult):
    Model = DataInfo[0] + ','
    #TestItem
    SN = DataInfo[1] + ':' + DataInfo[2] + ','
    IMEI = ' ,'
    StartTime = DataInfo[3] + ','
    TestTime = DataInfo[4] + ','
    #TestResult
    data = Model + TestItem + SN + IMEI + StartTime + TestTime + TestResult
    return data

def POST():
    #60.250.127.128
    #url = 'http://atrack.com.tw/factory/upload'
    #url = 'http://60.250.127.128:9527/factory/upload'
    #url = 'http://localhost:5000/factory/upload'
    url = 'http://192.168.81.54:5000/factory/upload'
    headers = {'Content-Type': 'text/plain; charset=utf-8'}
    
    for i in range(len(TestItem)):
        data = LoadData(TestItem[i], TestResult[i])
        print(data)
        payload = {
            'id':data, 
            'body':data}
    
        r = requests.post(url, headers = headers, data = data)
        print(r)
    
POST()
'''
TestForm = []
for i in range(len(TestItem)):
    data = LoadData(TestItem[i], TestResult[i])
    print(data)
    #[TestForm.append(LoadData(TestItem[i], TestResult[i]))]
    #print(TestForm[i])
'''




