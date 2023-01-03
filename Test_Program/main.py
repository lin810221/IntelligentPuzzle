import PySimpleGUI as sg
import InputInfo, InputSN



# 輸入內控碼
'''
def InputSN():
    layout = [[sg.Text('內控碼'), sg.Input(key = '_SN_', size = (20, 2))],
              [sg.Ok('Enter')]]
    return sg.Window(title = '輸入視窗', layout = layout, element_justification='c',
                       font = 'Courier 12', auto_size_text=True, auto_size_buttons=True,
                       element_padding=10, keep_on_top=True)
'''

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
    
    TestItem_key = ['_Startup_', '_FlashTest_', '_LEDTest_',]
    
    TestItem_name = ['Startup', 'FlashTest', 'LEDTest',]
    LED = []
    
    for i in range(len(TestItem_key)):
        LED.append([LEDIndicator(TestItem_key[i]), sg.Text(TestItem_name[i])])
    
    
    
    # 馬錶
    layout_Timer = [[sg.Text('TIME', font='Young 30', key='_Timer_', visible=True)]]
    
    # 工單與治具
    layout_WOJ = [[sg.Text(f'工單：{WO_Jig[0]} / 治具：{WO_Jig[1]}',
                           font='Young 20' , key='_WOJ_', visible=True)]]
    
    # 判定結果
    layout_Criteria = [[sg.Text('TEST', font='Young 30', key = '_Criteria_', visible=True)]]
    
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
                                                        expand_y=True
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
    
    layout = [[sg.Column(layout_Timer, expand_x=True, expand_y=False, element_justification='l'),
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
              [layout_Action], ]
    
    return sg.Window(title = 'Product', 
                     layout = layout, 
                     resizable = True, 
                     finalize = True,
                     scaling=1.3
                     )

def main():
    # 輸入工單號碼與治具編號
    WO_Jig = InputInfo.Input_WO_Jig()
    if WO_Jig == None:
        return 0
    

    window =  make_window(WO_Jig)
    while True:
        event, values = window.read(timeout=1)
        SN = InputSN.Input_SN()
        if SN == None:
            break
        elif SN != None:
            window['_output_'].update('Hi\n', append=True)
            continue
        
        if event == sg.WINDOW_CLOSED or window == sg.WINDOW_CLOSED:
            break

    
    window.close()
if __name__ == '__main__':
    main()
