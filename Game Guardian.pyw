#imports
import functools
import threading
import multiprocessing
import subprocess

#global variables



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

def notify():
    #send a desktop notification
    pass


def game_quota_achieved(game):
    #return true if the set quota has been achieved, otherwise false
    pass

def valorant_quota_achieved():
    #return true if the set quota has been achieved, otherwise false
    pass

def process_running(game):
    valorant_processes = [
        "VALORANT.exe",
        "RiotClientServices.exe",
        "vgc.exe",
        "VanguardTray.exe",
    ]
    try:
        output = subprocess.check_output("tasklist", shell=True).decode()
        return any(proc in output for proc in valorant_processes)
    except subprocess.CalledProcessError:
        return False


if process_running():
    print(True)
else:
    print(False)

    pass

def kill_process(game):
    #kill process
    pass

def process_maximised():
    #return false if process is minimised, otherwise true
    pass

def minimize_process():
    #minimize process
    pass




root = gui()

#mainloop
while True:
    pass