import time, threading


def Timer(): 
    n = 5
    for i in range(n+1):
        print(f'{n-i} sec')
        time.sleep(1)
    print('Times Up', end='')

t = threading.Thread(target = Timer)
t.start()