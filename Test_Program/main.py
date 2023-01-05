import PySimpleGUI as sg
import time, datetime
import InputInfo, InputSN, Option




# 設定主題樣式
sg.theme('DarkTanBlue')

# 測試項目
def TestItem():
    TestItem_dict = {'_Startup_':'Startup',
                 '_Flash_':'Flash Test',
                 '_LED_':'LED Test',
                 '_Buzzer_':'Buzzer Test',
                 '_RS-485_':'RS-485',
                 '_G-Sensor_':'G-Sensor',
                 '_AD Conversion_':'A/D Conversion (AN1、AN2、AN3)',
                 '_AD Convert_':'A/D Conversion (VIN,VBAT)',
                 '_AD Cal_':'A/D Cal.',
                 '_IO_':'I/O Test',
                 '_OBD_':'OBD Test',
                 '_BlueTooth_':'Blue Tooth',
                 '_GPS_':'GPS Test',
                 '_Charger_':'Charger Test',
                 '_Battery_':'Battery Test',
                 '_WIFI_':'WIFI Test',
                 '_LTE_':'LTE Test'}
    return TestItem_dict


#獲取時間
def getTime():
    #return datetime.datetime.now().strftime('%H:%M:%S')
    return datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")


# LED 燈號位置設計
def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
                    graph_bottom_left=(-radius, -radius),
                    graph_top_right=(radius, radius),
                    pad=(0, 0), key=key)

# LED 燈號顏色設計
def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)

# 主程式介面設計
def make_window(WO_Jig, TestOption=None):
    menu_def = [['&Tool', ['&Option']]]
    TestItem_dict = TestItem()
    
    
    if TestOption == None:
        LED = []
        for i in TestItem_dict:
            LED.append([LEDIndicator(i), sg.Text(TestItem_dict.get(i))])
    else:
        LED = [[LEDIndicator('_Startup_'), sg.Text('Startup')]]
        for i in TestOption:
            if TestOption.get(i) == True:
                LED.append([LEDIndicator(i), sg.Text(TestItem_dict.get(i))])
            else:
                continue

    # 馬錶
    layout_Timer = [[sg.Text('TIME', font='Young 30 bold', key='_Timer_', visible=True)]]
    
    # 工單與治具
    layout_WOJ = [[sg.Text(f'工單：{WO_Jig[0]} / 治具：{WO_Jig[1]}',
                           font='Young 16 bold' , key='_WOJ_', text_color='yellow', visible=True)]]
    
    # 判定結果
    layout_Criteria = [[sg.Text('TEST', font='Young 30 bold', key = '_Criteria_', visible=True)]]
    
    # 測項框
    layout_TestItem = [[sg.Frame('Test Item', 
                                 layout = [[sg.Column(LED,
                                                      scrollable = True,
                                                      vertical_scroll_only = True,
                                                      expand_x = True,
                                                      expand_y = True,
                                                      )
                                            ]],
                                 size=(200, 480),
                                 expand_x=True,
                                 expand_y=True,
                                 ),
                        ]]
    
    # 輸出框
    layout_Console = [[sg.Frame('Output', 
                                layout = [[sg.Multiline(size = (75, 25),
                                                        font='Courier 12',
                                                        key = '_output_',
                                                        text_color = 'white',
                                                        background_color = 'black',
                                                        autoscroll = True,
                                                        expand_x=True,
                                                        expand_y=True,
                                                        disabled=True
                                                        ),
                                           ]],
                                expand_x=True,
                                expand_y=True
                                )
                       ]]

    # 動作
    layout_Action = sg.Column(
        [[sg.Frame('Action',
                   [[sg.Column([[sg.Button('F1', size=10), sg.Button('F2', size=10)]],
                               expand_x=True, expand_y=True
                               )]],
                   expand_x=True, expand_y=True)
          ]]
        )
    
    layout = [[sg.Menu(menu_def, key='_menu_')],
              [sg.Column(layout_Timer, expand_x=True, expand_y=False, element_justification='l'),
               sg.Column(layout_WOJ, expand_x=True, expand_y=False, element_justification='c'), 
               sg.Column(layout_Criteria, expand_x=True, expand_y=False, element_justification='r')],
              [sg.Pane([sg.Column(layout_TestItem, expand_x=True, expand_y=True), 
                        sg.Column(layout_Console, expand_x=True, expand_y=True)],
                       relief=sg.RELIEF_RAISED,
                       orientation='h',
                       border_width=0,
                       expand_x=True,
                       expand_y=True
                       )],
              [layout_Action], 
              ]
    
    return sg.Window(title = 'Product', 
                     layout = layout, 
                     resizable = True, 
                     finalize = True,
                     scaling = 1.3,
                     no_titlebar = bool(0),
                     return_keyboard_events=True
                     )

def main():
    # 輸入工單號碼與治具編號
    WO_Jig = InputInfo.Input_WO_Jig()
    if WO_Jig == None:
        return 0
    
    active = False
    window =  make_window(WO_Jig)
    TestItem_dict = TestItem()
    while True:
        event, values = window.read(timeout=1000)
        if event in ['F1', 'F1:112']:
            SN = InputSN.Input_SN()
            if SN != None:  # 開始測試
                window['_output_'].update('Start Testing\n', append=False)
                start_time = time.time()
                active = True
                window['_Criteria_'].update('TESTING', text_color = 'DodgerBlue')
                
                
                for i in TestItem_dict:
                    SetLED(window, i, 'gray')
                
            else:
                continue
            
        if event in ['F2', 'F2:113']:
            pass

        if active == True:
            elapsed_time = round(time.time()-start_time)
            window['_Timer_'].update('{:02d}:{:02d}'.format(elapsed_time // 60, elapsed_time % 60),
                                     text_color = 'DodgerBlue')
            if elapsed_time >= 5:
                window['_Criteria_'].update('PASS', text_color = 'green1')
                window['_Timer_'].update(text_color = 'green1')
                window['_output_'].update(getTime() + ' : ', append=True)
                window['_output_'].update('Pass\n', text_color_for_value='Green1', append=True)
                ans = 0
                for i in TestItem_dict:
                    SetLED(window, i, 'green1' if ans == 0 else 'red')
            
            if elapsed_time >= 20:
                active = False
                window['_Criteria_'].update('FAIL', text_color = 'red')
                window['_Timer_'].update(text_color = 'red')
                window['_output_'].update(getTime() + ' : ', append=True)
                window['_output_'].update('Fail\n', text_color_for_value='Red', append=True)
                ans = 1
                for i in TestItem_dict:
                    SetLED(window, i, 'green1' if ans == 0 else 'red')
            
            #print(elapsed_time)
        
        if event == 'Option':
            TestOption = Option.Option()
            if TestOption != None:  
                TestItem_dict = TestItem()
                for i in TestOption:
                    if TestOption.get(i) == False:
                        del TestItem_dict[i]
                    else:
                        continue
                    
                print(TestOption)
                window.close()
                window = make_window(WO_Jig, TestOption=TestOption)
            else:
                continue
            
            
            
        
        '''
        if event == 'F5:116':
            window['_output_'].update(value='')
        '''
            
        if event == sg.WINDOW_CLOSED:
            break

    
    window.close()
    del window
if __name__ == '__main__':
    main()