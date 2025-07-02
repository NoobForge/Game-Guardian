#blitzdevdaddy,snowwhiteohno,baler1on
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
import os
import sys
import singleton
import valo_api
import datetime


#global variables
valo_api_key = 'HDEV-dec0a00b-3220-4745-81d7-f2908bf14a5d'
player_name = 'blitz'
player_tag = 'rizz'
player_region = 'ap'


#baler1on
config.backup = os.path.join(os.path.dirname(__file__), 'config.json')
config.path = os.path.join(os.getenv('APPDATA'), 'Game Guardian', 'config.json')

valo_api.set_api_key(valo_api_key)

def toggle_autostart():
    """Toggle autostart status in registry and config"""
    if autostart.exists('Game Guardian')== True:
        autostart.remove('Game Guardian')
        config.write('autostart',False)
    else:
        autostart.add('Game Guardian',os.path.abspath(sys.argv[0]))
        config.write('autostart',True)
if autostart.exists('Game Guardian')!= config.read('autostart'):
    toggle_autostart()


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
    """Send a notification with the given message"""
    plyer.notification.notify(title = 'Game Guardian', message = message)

#baler1on
def process_pid(process_name):
    """Get the process ID of a running process by its name"""
    return subprocess.check_output(f'(Get-Process -Name "{process_name}").Id').decode()

#baler1on
def quit():
    """Force quit the application"""
    subprocess.check_output(f'taskkill /f /pid {os.getpid()}')
try:
    me = singleton.SingleInstance()
except: quit()

#baler1on
def utc_to_local(utc_str):
    if utc_str.endswith('Z'):
        utc_str = utc_str[:-1]
    try:
        dt = datetime.datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S.%f")
    except:
        dt = datetime.datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S")
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    local_dt = dt.astimezone()
    return local_dt


def game_quota_achieved(game):
    #return true if the set quota has been achieved, otherwise false
    pass

#baler1on
def valorant_quota_achieved():
    def gamemode_played_today(gamemode):
        matches_today = 0
        if gamemode == "All":
            for match in valo_api.endpoints.get_lifetime_matches_by_name(version='v1', region='ap', name='blitz', tag='rizz'):
                if utc_to_local(match.meta.started_at).date() == datetime.datetime.now().date():
                    matches_today += 1
        else:
            for match in valo_api.endpoints.get_lifetime_matches_by_name(version='v1', region='ap', name='blitz', tag='rizz', mode=gamemode):
                if utc_to_local(match.meta.started_at).date() == datetime.datetime.now().date():
                    matches_today += 1
        return matches_today
    
    if config.read("valorant_quota_achieved"):
        return True
    else:
        pass

#baler1on
def process_running(process_name):
    """Check if a process is running by its name"""
    try:
        return 'Get-Process' not in subprocess.check_output(f'powershell.exe Get-Process -Name {process_name}').decode()
    except: return False

#baler1on
def kill_process(process_name):
    """Kill a process by its name"""
    try:
        subprocess.check_output(f'taskkill /f /im {process_name}')
        notify(f'closed {process_name}')
    except: pass

#blitzdevdaddy
def process_maximised(process_name):
    """Check if a process is maximised by its window title"""
    try:
        def enum_handler(hwnd, result):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if process_name.lower() in title.lower():
                    result.append(hwnd)

        result = []
        win32gui.EnumWindows(enum_handler, result)

        if result:
            hwnd = result[0]
            placement = win32gui.GetWindowPlacement(hwnd)
            show_cmd = placement[1]
            is_maximised = show_cmd != win32con.SW_SHOWMINIMIZED
            return is_maximised
        else:
            return False
    except Exception as e:
        print(f"check nhi hori maximise ke liye: {e}")
        return False

#blitzdevdaddy
def minimize_process(process_name):
    """Minimize a process by its window title"""
    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if process_name.lower() in title.lower():
                print(f"Minimizing: {title}")
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    win32gui.EnumWindows(enum_handler, None)



#testcode
#time.sleep(5)
#kill_process('Valorant')
#minimize_process("Discord")
#print(process_running('Valorant'))
#print(process_maximised('Valorant'))

root = gui()

    
#mainloop
while True:
    pass
