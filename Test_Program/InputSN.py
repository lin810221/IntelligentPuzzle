import PySimpleGUI as sg


def pre():
    layout = [[sg.Text('內控碼'), sg.Input(key = '_SN_', size = (20, 2))],
              [sg.Ok('Enter')]]
    return sg.Window(title = '輸入視窗', layout = layout, element_justification='c',
                       font = 'Courier 12', auto_size_text=True, auto_size_buttons=True,
                       element_padding=10, keep_on_top=True)

def Input_SN():
    window = pre()
    while True:
        event, values = window.read()
        if event == 'Enter':
            if values['_SN_'] == '':
                sg.popup('請輸入內控碼！', keep_on_top=True)
            else:
                window.close()
                return values['_SN_']
        elif event == sg.WINDOW_CLOSED:
            break
    window.close()