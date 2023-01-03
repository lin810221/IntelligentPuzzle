import PySimpleGUI as sg

def pre():

    layout = [
        [sg.Text('工單號碼：'), sg.Input(key = '_WONumber_', size=(20, 2))],
        [sg.Text('治具編號：'), sg.Input(key = '_JigNumber_', size=(20, 2))],
        [sg.Ok('Enter')]]
    
    return sg.Window(title = '輸入視窗', layout = layout, element_justification='c',
                       font = 'Courier 12', auto_size_text=True, auto_size_buttons=True,
                       element_padding=10)

def Input_WO_Jig():
    window = pre()
    while True:
        event, values = window.read()
        if event == 'Enter':
            if values['_WONumber_'] == '' or values['_JigNumber_'] == '':
                sg.popup('請輸入 工單號碼 / 治具編號！')
            else:
                window.Close()
                return (values['_WONumber_'], values['_JigNumber_'])
        
        elif event == sg.WINDOW_CLOSED:
            break
    window.close()