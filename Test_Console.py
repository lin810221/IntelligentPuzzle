import PySimpleGUI as sg
import serial, datetime, time

ok = '$OK\r\n'
scroll = '=' * 30

s = serial.Serial(port = 'COM11', 
                  baudrate = 57600, 
                  bytesize = 8, 
                  parity = 'N', 
                  stopbits = 1) # open Terminal

text_elem = sg.Text()
sg.theme('DarkAmber') # 主題設置


menu_def = [['File', ['Open', 'Save', 'Exit' ]],
            ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],]]



TestItem = ['Dog', 'Cat', 'Bird', 'Rat', 'Rabbit',]


#TestItem = [f'Test {i}' for i in range(1, 11)]
#[sg.Listbox(TestItem, size=(10,24), font='Courier 12')]

def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)



left = [[sg.Text('TestItem')],
        [sg.Text('Dog'), LEDIndicator('_dog_')],
        [sg.Text('Cat'), LEDIndicator('_cat_')],
        [sg.Text('Bird'), LEDIndicator('_bird_')],
        [sg.Text('Rat'), LEDIndicator('_rat_')],
        [sg.Text('Rabbit'), LEDIndicator('_rabbit_')],]

right = [[sg.Text('Console')],
         [sg.Output(size=(90,26), font='Courier 12', key='@output'), ], ]




left2 = [[sg.Frame('Test Item', [[sg.Text('Dog\t'), LEDIndicator('_dog_')],
                                 [sg.Text('Cat\t'), LEDIndicator('_cat_')],
                                 [sg.Text('Bird\t'), LEDIndicator('_bird_')],
                                 [sg.Text('Rat\t'), LEDIndicator('_rat_')],
                                 [sg.Text('Rabbit\t'), LEDIndicator('_rabbit_')],
                                 [sg.Text('Bat\t'), LEDIndicator('_bat_')],
                                 [sg.Text('Lion\t'), LEDIndicator('_lion_')],
                                 ], size = (100, 390))]]


right2 = [[sg.Frame('Output', [[sg.Output(size=(75,20), font='Courier 12', key='@output', text_color='white'), ], ])]]

Actions = sg.Column([[sg.Frame('Actions:', [[sg.Column([[sg.Button('Test 1'), 
                                                         sg.Button('Test 2'),
                                                         sg.Button('Test 3'),
                                                         sg.Button('Clean'),
                                                         sg.Cancel()]],
                                                       size=(900,45), pad=(0,0))]])]], pad=(0,0))


# [sg.Button('Test 1'), sg.Button('Test 2'), sg.Button('Clean'), sg.Cancel(), ],
layout = [[sg.Menu(menu_def, key = '@menu')], # Menu Bar
          [sg.Text('Time: ', font=("Helvetica", 16)), sg.Text('', key='_time_', font=("Helvetica", 16), text_color='white')],
          [sg.Text('DEMO', size=(75, 1), justification='center', font=("Helvetica", 16), 
                   relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
          [sg.Push(), sg.Text('Command'), sg.Input('AT$', key = '@command'), sg.OK('Enter')],
          [sg.Column(left2), sg.Column(right2)],
          [Actions],
          [text_elem], ]


'輸入指令'
def TestItem(case):
    if case == 1:
        TestCase('WIFI', )
    
    elif case == 2:
        TestCase('FORM', )
        TestCase('IPFC', )
        TestCase('MDSC', )
        TestCase('FWDL', )
        TestCase('IOCG', )
        

    elif case == 3:
        TestCase('ROAM', )
        TestCase('ROAM', '0,5,0,0,"25110","46692"')


'指令重組'
def TestCase(a, b = None):
    res = 'AT$' + a + '=' + (b if b else '?') + '\n'
    s.write(res.encode ('utf-8'))
    verifyResponse()


'回應分析'
def verifyResponse():
    while(1):
        cage = s.readline().decode('utf-8').split()[0]
        if cage[0] == '$':
            now = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            
            print(now + ' : ' + cage)
            #sg.Print(now + ' : ' + cage)
            
            

            break
        else:
            pass
            #print(cage)


window = sg.Window(title = 'Test Console', layout = layout, 
                   return_keyboard_events=True, use_default_focus=False,
                   )

def getTime():
    return datetime.datetime.now().strftime('%H:%M:%S')

while True:
    event, values = window.read(timeout=10)
    
    
    if event == 'Enter': # Enter 鍵觸發
        command = values['@command'] + '\n'     # 輸入指令
        s.write(command.encode ('utf-8'))       # 寫入至 console 環境
        verifyResponse()
        #print(s.readline().decode('utf-8').split()[0])  # 顯示讀取的資訊

    if event == 'Test 1':
        print(scroll + ' Test 1 ' + scroll)
        ans = 0
        TestItem(1)
        SetLED(window, '_dog_', 'green1' if ans == 0 else 'red')
                
    if event == 'Test 2':
        print(scroll + ' Test 2 ' + scroll)
        TestItem(2)
        ans = 0
        SetLED(window, '_cat_', 'green1' if ans == 0 else 'red')
        SetLED(window, '_bird_', 'green1' if ans == 0 else 'red')
        SetLED(window, '_rat_', 'green1' if ans == 0 else 'red')
        SetLED(window, '_rabbit_', 'green1' if ans == 0 else 'red')


    if event == 'Test 3':
        print(scroll + ' Test 3 ' + scroll)

        ans = 1
        TestItem(3)
        SetLED(window, '_bat_', 'green1' if ans == 0 else 'red')
        SetLED(window, '_lion_', 'green1' if ans == 0 else 'red')
        

    '刷新輸出資訊'
    if event == 'Clean' or event == 'F5:116':
        window['@output'].update(value='')
        
    '終止程式執行'
    if event == sg.WINDOW_CLOSED or \
        event == 'Cancel' or \
            event == 'Escape:27':
                s.close() # close Terminal
                break
    text_elem.update(event)
    window['_time_'].Update(getTime())
    

window.close() # 關閉 GUI 介面
