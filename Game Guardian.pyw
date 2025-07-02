#imports
import functools
import threading
import multiprocessing
import subprocess
import plyer
import config
import autostart
import win32gui
import win32con
import time


#global variables
valorant_process_name = 'VALORANT-Win64-Shipping.exe'


#snowwhiteohno
class gui:
    def __init__(self):
        pass

    def open_config_gui():
        pass

    def open_prevention_gui():
        pass


#baler1on
def threaded(func):
    """Decorator to automatically launch a function in a thread"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

#baler1on
def multiprocessed(func):
    """Decorator to automatically launch a function in a process"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process
    return wrapper

#baler1on
def notify(message):
    plyer.notification.notify(title = 'Game Guardian', message = message)

#baler1on
def process_pid(process_name):
    return subprocess.check_output(f'(Get-Process -Name "{process_name}").Id').decode()


def game_quota_achieved(game):
    #return true if the set quota has been achieved, otherwise false
    pass

def valorant_quota_achieved():
    #return true if the set quota has been achieved, otherwise false
    pass

#baler1on
def process_running(process_name):
    try:
        return 'Get-Process' not in subprocess.check_output(f'powershell.exe Get-Process -Name {process_name}').decode()
    except: return False

#baler1on
def kill_process(process_name):
    try:
        subprocess.check_output(f'taskkill /f /im {process_name}')
        notify(f'closed {process_name}')
    except: pass

#blitzdevdaddy
def process_maximised(window_title="VALORANT"):
    try:
        def enum_handler(hwnd, result):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if window_title.lower() in title.lower():
                    result.append(hwnd)

        result = []
        win32gui.EnumWindows(enum_handler, result)

        if result:
            hwnd = result[0]
            placement = win32gui.GetWindowPlacement(hwnd)
            show_cmd = placement[1]
            is_maximised = show_cmd != win32con.SW_SHOWMINIMIZED
            print(is_maximised)
            return is_maximised
        else:
            print(False)
            return False
    except Exception as e:
        print(f"check nhi hori maximise ke liye: {e}")
        return False

#blitzdevdaddy
def minimize_process(process_name):
    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if process_name.lower() in title.lower():
                print(f"Minimizing: {title}")
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    win32gui.EnumWindows(enum_handler, None)



#testcode
#time.sleep(5)
#kill_process(valorant_process_name)
#minimize_process("Discord")
#print(process_running('Valorant'))
process_maximised(window_title="VALORANT") 

root = gui()

    
#mainloop
while True:
    pass
