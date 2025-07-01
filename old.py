import plyer
import valo_api
import threading
import time
import os
import pystray 
import tkinter
from PIL import Image, ImageDraw
from tendo import singleton
import sys
import subprocess



config = open(os.path.join(sys.path[0], "config.txt"), "r")

valorant_process_name = str(config.readline())
valorant_process_name = valorant_process_name.replace(valorant_process_name[-1],'',1)

key = str(config.readline())
key = key.replace(key[-1],'',1)

name = str(config.readline())
name = name.replace(name[-1],'',1)

tag = str(config.readline())
tag = tag.replace(tag[-1],'',1)

unrated_match_limit = int(config.readline())
competitive_match_limit = int(config.readline())
swiftplay_match_limit = int(config.readline())
spikerush_match_limit = int(config.readline())
deathmatch_match_limit = int(config.readline())
escalation_match_limit = int(config.readline())
teamdeathmatch_match_limit = int(config.readline())
all_match_limit = int(config.readline())

config.close()


try:
    me = singleton.SingleInstance()
except:
    plyer.notification.notify(title = "anti valo", message = "process already active")
    time.sleep(10)
    pid = os.getpid()
    os.system(f'taskkill /f /pid {pid} >nul 2>&1')
    print('mm')


if key != 0:
    print('key_set')
    valo_api.set_api_key(key)


valorant_locked = False
valorant_played = False



def eos_screen():
    eos_window = tkinter.Tk()
    eos_window.geometry('300x100')
    eos_window.configure(bg='#ab23ff')
    eos_window.wm_attributes('-transparentcolor', '#ab23ff')
    eos_window.attributes('-topmost',True)
    eos_window.overrideredirect(True)

    timer = 30

    eos_label = tkinter.Label(text=f'EOS : {timer}', fg='red', font=("Arial", 48, "bold"),bg='#ab23ff')
    eos_label.place(x=0,y=0)

    for elapsed_time in range(timer+2):
        time.sleep(1)
        remaining_time = timer - elapsed_time
        print(remaining_time)
        eos_label.config(text=f'EOS : {remaining_time}')
        eos_label.update()

    eos_window.destroy()

def start_eos_timer():
    eos_thread = threading.Thread(target=eos_screen)
    eos_thread.start()



def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

def tray_quit(tray,query):
    tray.stop()
    pid = os.getpid()
    os.system(f'taskkill /f /pid {pid} >nul 2>&1')

def tray():
    image = create_image(64, 64, 'black', 'red')
    tray = pystray.Icon("antivalo", image, "antivalo tray", menu=pystray.Menu(pystray.MenuItem("exit", tray_quit)))
    tray.run()

tray_thread = threading.Thread(target=tray)
tray_thread.start()



def variable_reset_timer():
    global valorant_locked,valorant_played
    while True:
        valorant_locked = False
        valorant_played = False
        print('f')
        
        local_time = time.localtime()
        next_time_epoch = time.mktime((local_time.tm_year, local_time.tm_mon, local_time.tm_mday, 2, 0, 0,local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))+86400
        sleep_time = int(next_time_epoch)-int(time.mktime(local_time))
        time.sleep(sleep_time)
    
variable_reset_thread = threading.Thread(target=variable_reset_timer)
variable_reset_thread.start()
print('bruh')



def kill_valorant():
    os.system(f'taskkill /f /im {valorant_process_name} >nul 2>&1')
    print('killed valorant')
    plyer.notification.notify(title = "anti valo", message = "valorant closed, padhle jaake")



def valorant_active():
    print('he')
    output_data = os.popen(f'powershell.exe Get-Process Valorant').read()
    print(str(output_data))
    is_node_running = 'Get-Process' not in str(output_data)
    if is_node_running==True:
        print('umm')
    return is_node_running



def valorant_played_today():
    global unrated_match_limit, competitive_match_limit, swiftplay_match_limit, spikerush_match_limit, deathmatch_match_limit, escalation_match_limit, teamdeathmatch_match_limit, all_match_limit
    def gamemode_played_today(gamemode,data_size):
        if data_size == 0:
            return False
        else:
            try:
                print('ho')
                print(gamemode)
                if gamemode=='all':
                    last_match_data = str(valo_api.endpoints.get_lifetime_matches_by_name(version='v1',region='ap',name='Manasmay',tag='2812'))
                else:
                    last_match_data = str(valo_api.endpoints.get_lifetime_matches_by_name(version='v1',region='ap',name='Manasmay',tag='2812',mode=gamemode))

                num_matches_played=0
                last_match_time_prev_index = 0
                while True:
                    last_match_time_index = last_match_data.find("started_at='",last_match_time_prev_index+1)
                    if last_match_time_index== -1:
                        print('jo')
                        break
                    last_match_time_prev_index = last_match_time_index

                    last_match_time_gmt = time.strptime(last_match_data[last_match_time_index+12:last_match_time_index+31], '%Y-%m-%dT%H:%M:%S')
                    last_match_time_ist = time.localtime(time.mktime(last_match_time_gmt)+19800)
                    last_match_date_ist = last_match_time_ist.tm_mday

                    current_date_local = time.localtime().tm_mday
                
                    if last_match_date_ist == current_date_local:
                        num_matches_played+=1
                    else:
                        print('jo')
                        break
                print(num_matches_played)
                if num_matches_played==data_size:
                    print('played_true')
                    return True
                else:
                    return False

            except:
                plyer.notification.notify(title = "anti valo", message = "api error", timeout = 10)
                time.sleep(2)
                gamemode_played_today(gamemode,data_size)

    if gamemode_played_today('Unrated',unrated_match_limit)==True or gamemode_played_today('Competitive',competitive_match_limit)==True or gamemode_played_today('Swiftplay',swiftplay_match_limit)==True or gamemode_played_today('Spikerush',spikerush_match_limit)==True or gamemode_played_today('Deathmatch',deathmatch_match_limit)==True or gamemode_played_today('Escalation',escalation_match_limit)==True or gamemode_played_today('Teamdeathmatch',teamdeathmatch_match_limit)==True or gamemode_played_today('all',all_match_limit)==True:
        return True
    else:
        return False

if valorant_played_today() == True:
    print('heh')
    valorant_played = True
    valorant_locked = True
    if valorant_active() == True:
        print('hehe')
        kill_valorant()

while True:
    print(valorant_locked)
    print('loop')

    if valorant_locked == True:
        time.sleep(30)
    elif valorant_locked == False:
        time.sleep(300)

    if valorant_locked == True:
        print('locked')
        if valorant_active() == True:
            time.sleep(1)
            kill_valorant()

    elif valorant_played == True:
        start_eos_timer()
        time.sleep(30)
        valorant_locked = True
        kill_valorant()

    elif valorant_active() == True:
        time.sleep(1)
        while valorant_active() == True and valorant_played == False:
            time.sleep(1)
            if valorant_played_today() == True:
                print('played')
                valorant_played = True
                if valorant_locked == False:
                    start_eos_timer()
                    time.sleep(30)
                    valorant_locked = True
                    kill_valorant()
                break
            time.sleep(15)

