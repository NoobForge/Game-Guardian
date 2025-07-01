#imports
import functools
import threading
import multiprocessing
import subprocess
import plyer
import config


#global variables
valorant_process_name = 'VALORANT-Win64-Shipping.exe'


class gui:
    def __init__(self):
        pass

    def open_config_gui():
        pass

    def open_prevention_gui():
        pass


def threaded(func):
    """Decorator to automatically launch a function in a thread"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def multiprocessed(func):
    """Decorator to automatically launch a function in a process"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process
    return wrapper

def notify(message):
    plyer.notification.notify(title = 'Game Guardian', message = message)


def game_quota_achieved(game):
    #return true if the set quota has been achieved, otherwise false
    pass

def valorant_quota_achieved():
    #return true if the set quota has been achieved, otherwise false
    pass

def process_running(game):
    valorant_processes = [
        "VALORANT.exe",
    ]
    try:
        output = subprocess.check_output("tasklist", shell=True).decode()
        return any(proc in output for proc in valorant_processes)
    except subprocess.CalledProcessError:
        return False

def kill_process(process_name):
    try:
        subprocess.check_output(f'taskkill /f /im {process_name}')
        notify(f'killed {process_name}')
    except: pass

def process_maximised():
    #return false if process is minimised, otherwise true
    pass

def minimize_process():
    #minimize process
    pass


#testcode
kill_process(valorant_process_name)


root = gui()

    
#mainloop
while True:
    pass
