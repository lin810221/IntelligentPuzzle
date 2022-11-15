import PySimpleGUI as sg

sg.theme('DarkAmber') # 主題設置

def login():
    layout = [
        [sg.Text('USERNAME')],
        [sg.Input(key = '_USER_')],
        [sg.Text('PASSWORD')],
        [sg.Input(key = '_PWD_', password_char = '*')],
        [sg.Ok('Enter', size = (40, 1))]]

    return sg.Window(title = "Login", layout = layout, 
                     finalize=True,  element_justification='c', 
                     return_keyboard_events=True)

def loading():
    layout = [[sg.Text('Loading')],
              [sg.ProgressBar(3000, orientation='h', size=(20, 20), key='_progressBar_')],]

    window = sg.Window(title = 'Loading', layout = layout)

    while True:
        event, values = window.read(timeout = 0)
        progress_bar = window['_progressBar_']
        for i in range(3000):
            progress_bar.UpdateBar(i + 1)
        break

        if event == sg.WINDOW_CLOSED:
            break

    window.close()


def make_win1():
    layout = [[sg.Text('void'), sg.Text('      ', k='-OUTPUT-')]]
    
    return sg.Window('Window Title', layout, finalize=True)


def main():
    window1, window2 = login(), None
    
    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WINDOW_CLOSED:
                break
            
        if window == window1:
            if event == 'Enter' or event == 'Enter:13':
                if values['_USER_'] == 'a' and values['_PWD_'] == 'a':
                    sg.popup('Success!')
                    window1.Close()
                    loading()
                    window2 = make_win1()
                    
                else:
                    sg.popup('Failed!', text_color = 'red')
    
    window.close()

if __name__ == '__main__':
    main()
