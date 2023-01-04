import PySimpleGUI as sg
import time
import InputInfo, InputSN



sg.theme('random')

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




def make_window(WO_Jig):
    menu_def = [['&Tool', ['&Option']]]
    
    TestItem_key = ['_Startup_', '_FlashTest_', '_LEDTest_',]
    
    TestItem_name = ['Startup', 'FlashTest', 'LEDTest',]
    LED = []
    
    for i in range(len(TestItem_key)):
        LED.append([LEDIndicator(TestItem_key[i]), sg.Text(TestItem_name[i])])
    
    
    
    # 馬錶
    layout_Timer = [[sg.Text('TIME', font='Young 30 bold', key='_Timer_', visible=True)]]
    
    # 工單與治具
    layout_WOJ = [[sg.Text(f'工單：{WO_Jig[0]} / 治具：{WO_Jig[1]}',
                           font='Young 16' , key='_WOJ_', visible=True)]]
    
    # 判定結果
    layout_Criteria = [[sg.Text('TEST', font='Young 30 bold', key = '_Criteria_', visible=True)]]
    
    # 測項框
    layout_TestItem = [[sg.Frame('Test Item', 
                                 layout = [[sg.Column(LED,
                                                      scrollable = True,
                                                      vertical_scroll_only = True,
                                                      expand_x = True,
                                                      expand_y = True
                                                      )
                                            ]],
                                 size=(200, 480),
                                 expand_x=True,
                                 expand_y=True
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
                   [[sg.Column([[sg.Button('F1'), sg.Button('F2')]],
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
    while True:
        event, values = window.read(timeout=1000)
        if event in ['F1', 'F1:112']:
            SN = InputSN.Input_SN()
            if SN != None:
                window['_output_'].update('Hi\n', append=True)
                start_time = time.time()
                active = True
                window['_Criteria_'].update('TESTING', text_color = 'DodgerBlue')

            else:
                break
        
        if active == True:
            elapsed_time = round(time.time()-start_time)
            window['_Timer_'].update('{:02d}:{:02d}'.format((elapsed_time // 100)%60,
                                                            elapsed_time % 100),
                                     text_color = 'DodgerBlue')
            if elapsed_time >= 20:
                active = False
                window['_Criteria_'].update('FAIL', text_color = 'red')
                window['_Timer_'].update(text_color = 'red')
            
            #print(elapsed_time)
        
        
        if event == 'Option':
            left = [[sg.Checkbox('Flash Test', key=None)],
                     [sg.Checkbox('RS485 Test')],
                     [sg.Checkbox('GPS Test')],
                     [sg.Checkbox('G-Sensor self')],
                     [sg.Checkbox('A/D Conversion (AN1, AN2, AN3)')],
                     [sg.Checkbox('A/D Convert (VIN, VBA)')],
                     [sg.Checkbox('A/D Cal.')],
                     [sg.Checkbox('I/O Test')],]
            
            right = [[sg.Checkbox('Blue Tooth')],
                      [sg.Checkbox('WIFI Test')],
                      [sg.Checkbox('LTE Test')],
                      [sg.Checkbox('OBD Test')],
                      [sg.Checkbox('LED Test')],
                      [sg.Checkbox('Buzzer Test')],
                      [sg.Checkbox('Charger Test')],
                      [sg.Checkbox('Battery Test')],]
            
            layout = [[sg.Checkbox('All checked', enable_events=False),
                       sg.Checkbox('All unchecked', enable_events=False),],
                      [sg.HorizontalSeparator()],
                      [sg.Column(left), sg.Column(right)],
                      [sg.OK(), sg.Cancel('Cancel')]]
            event, values = sg.Window('Option', layout = layout, no_titlebar=True, keep_on_top=True).read(close=True)
            
            if event == 'OK':
                window.refresh()    # 可強制更新 GUI 而不被等待計時所干擾
        
        '''
        if event == 'F5:116':
            window['_output_'].update(value='')
        '''
            
        if event == sg.WINDOW_CLOSED:
            break

    
    window.close()
if __name__ == '__main__':
    main()
