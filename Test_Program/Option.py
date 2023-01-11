import PySimpleGUI as sg
import main


'''
TestItem_key = ['_Startup_', '_Flash_', '_LED_',
                '_Buzzer_', '_RS-485_', '_G-Sensor_',
                '_AD Conversion_', '_AD Convert_', '_AD Cal_',
                '_IO_', '_OBD_', '_BlueTooth_',
                '_GPS_', '_LTE_', '_WIFI_',
                '_Charger_', '_Battery_']
'''

# 載入產測資訊
TestItem_dict = main.TestItem()




def pre():
    count = 0
    left, right = [], []
    for i in TestItem_dict:
        if i == '_Startup_':
            continue
        else:
            if count % 2 == 0:
                left.append([sg.Checkbox(TestItem_dict.get(i), key=i, enable_events=True)])
                
            else:
                right.append([sg.Checkbox(TestItem_dict.get(i), key=i, enable_events=True)])
        count += 1
    
    layout = [[sg.Checkbox('All checked', key='_AllChecked_', enable_events=True),
               sg.Checkbox('All unchecked', key='_AllUnchecked_', enable_events=True),],
              [sg.HorizontalSeparator()],
              [sg.Column(left), sg.Column(right)],
              [sg.OK(), sg.Cancel('Cancel')]]

    return sg.Window('Option', layout = layout, no_titlebar=True, keep_on_top=True, finalize=True)
    
def Option():
    window = pre()
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, 'Cancel']:
            break
    
        elif event == '_AllChecked_':
            for i in TestItem_dict:
                if i == '_Startup_':
                    continue
                else:
                    window[i].update(True)
            window['_AllUnchecked_'].update(False)
            
        elif event == '_AllUnchecked_':
            for i in TestItem_dict:
                if i == '_Startup_':
                    continue
                else:
                    window[i].update(False)
            window['_AllChecked_'].update(False)
        
        elif event.startswith( tuple(list(TestItem_dict.keys())) ): # dict -> list -> tuple
            if not values[event]:
                window['_AllChecked_'].update(False)
            else:
                window['_AllUnchecked_'].update(False)
    
        elif event == 'OK':
            a = values
            del a['_AllChecked_']
            del a['_AllUnchecked_']
            window.close()
            return a
    window.close()
