import PySimpleGUI as sg
import serial, datetime, time


ok = '$OK\r\n'
s = serial.Serial(port = 'COM11', 
                  baudrate = 57600, 
                  bytesize = 8, 
                  parity = 'N', 
                  stopbits = 1) # open Terminal

text_elem = sg.Text()
sg.theme('DarkAmber')

menu_def = [['File', ['Open', 'Save', 'Exit' ]],
            ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],]]



#TestItem = ['Dog', 'Cat', 'Bird', 'Rat', 'Rabbit',]


TestItem = [f'Test {i}' for i in range(1, 11)]


left = [
    [sg.Text('TestItem')],
    [sg.Listbox(TestItem, size=(10,24), font='Courier 12'), ]
    ]

right = [
    [sg.Text('Console')],
    [sg.Output(size=(100,26), font='Courier 12', key='@output'), ],
    ]


layout = [[sg.Menu(menu_def, key = '@menu')], # Menu Bar
          [sg.Text('DEMO', size=(95, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
          [sg.Push(), sg.Text('Command'), sg.Input('AT$', key = '@command'), sg.OK('Enter')],
          [sg.Column(left), sg.Column(right)],
          [sg.Button('Test 1'), sg.Button('Test 2'), sg.Button('Clean'), sg.Cancel(), ],
          [text_elem]
          ]



def TestItem(case):
    if case == 1:
        TestCase('WIFI', )
    
    elif case == 2:
        TestCase('FORM', )
        TestCase('IPFC', )
        TestCase('MDSC', )
        TestCase('FWDL', )
        TestCase('IOCG', )
        TestCase('ROAM', )
        TestCase('ROAM', '0,5,0,0,"25110","46692"')


def TestCase(a, b = None):
    res = 'AT$' + a + '=' + (b if b else '?') + '\n'
    s.write(res.encode ('utf-8'))
    #verifyResponse()
    while(1):
        cage = s.readline().decode('utf-8').split()[0]
        if cage[0] == '$':
            now = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            print(now + ' : ' + cage)
            break
        else:
            pass

'''
def verifyResponse():
    while(1):
        cage = s.readline().decode('utf-8').split()[0]
        if cage[0] == '$':
            now = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            print(now + ' : ' + cage)
            break
        else:
            pass
            #print(cage)
'''

window = sg.Window(title = 'Test Console', layout = layout, return_keyboard_events=True, use_default_focus=False)


while True:
    event, values = window.read()
    
    if event == 'Enter': # Enter 鍵觸發
        command = values['@command'] + '\n'     # 輸入指令
        s.write(command.encode ('utf-8'))       # 寫入至 console 環境
        print(s.readline().decode('utf-8').split()[0])  # 顯示讀取的資訊

    if event == 'Test 1':
        TestItem(1)
                
    if event == 'Test 2':
        TestItem(2)
        window['@output'].update()
        

    '刷新輸出資訊'
    if event == 'Clean' or event == 'F5:116':
        window['@output'].update(value='')
        
    '終止程式執行'
    if event == sg.WINDOW_CLOSED or \
        event == 'Cancel' or \
            event == 'Escape:27':
        break
    text_elem.update(event)
    
s.close() # close Terminal
window.close() # 關閉 GUI 介面
