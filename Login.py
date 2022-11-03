import PySimpleGUI as sg


sg.theme('Darkblue1')

# 處理登入問題
def login():
    ans = 0
    layout = [
        [sg.Text('USERNAME')],
        [sg.Input(key = '_USER_')],
        [sg.Text('PASSWORD')],
        [sg.Input(key = '_PWD_', password_char = '*')],
        [sg.Ok('Enter', button_color='#000000', size = (40, 1))]]
    
    window = sg.Window(title="Login", layout = layout, 
                       element_justification='c', return_keyboard_events=True)

    while True:
        event, values = window.read()
        
        if event == 'Enter' or event == 'Enter:13':
            if values['_USER_'] == 'admin' and values['_PWD_'] == '0000':
                ans += 1
                sg.popup('Success!')
                break
            else:
                sg.popup('Failed!', text_color = 'red')
        
        if event == sg.WINDOW_CLOSED:
            break
    
    window.close()
    return ans

# 登入條
def loading():
    layout = [
        [sg.Text('Loading')],
        [sg.ProgressBar(10000, orientation='h', size=(20, 20), key='_progressBar_')],]

    window = sg.Window(title = 'Loading', layout = layout)

    while True:
        event, values = window.read(timeout = 1000)
        progress_bar = window['_progressBar_']
        for i in range(10000):
            progress_bar.UpdateBar(i + 1)
        break

        
        if event == sg.WINDOW_CLOSED:
            break

    window.close()

# 主功能
def main():
    login_result = login()
    if login_result == 1:
        loading()


if __name__ == '__main__':
    main()