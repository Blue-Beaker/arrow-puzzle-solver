#! /bin/python3
import threading
from PIL import ImageGrab
from PIL import Image
import time
from pykeyboard import PyKeyboardEvent
import tkinter
from tkinter import ttk
from tkinter import IntVar
from tkinter import StringVar
import os
import ctypes
from pymouse import PyMouse
import copy
#Make sure your latency is low or this script can make lots of mistakes before solving
#Change these values if the script doesn't work.
#Take a screenshot with the button and get the x0,y0,dx,dy values from the picture.
windowWidth=540
windowHeight=950
x0=50   #X of Topmost cell in the leftmost column
y0=435  #Y of Topmost cell in the leftmost column
dx=67   #dX of 2 horizonal cells
dy=78   #dY of 2 vertical cells
scrcpy_path="scrcpy"    #Replace with your path to scrcpy
adb_path="adb"          #Replace with your path to adb

colors=[]
class KeyDown(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
    def tap(self, keycode, character, press):
        global kill
        if press:
            if keycode==76:
                kill=1

def rgb2num(rgb):
    global mode
    if rgb[0]<=20:
        num=1
    elif mode.get()==0 and rgb[0]>=60:
        num=2
    elif rgb[0]<=35:
        num=2
    elif rgb[0]<=45:
        num=3
    elif rgb[0]<=60:
        num=4
    elif rgb[0]<=75:
        num=5
    elif rgb[0]<=90:
        num=6
    else:
        num=0
    return num
def packcoords(x,y):
    global x0,y0,dx,dy
    outx=x0+x*dx
    outy=y0-x*0.5*dy+y*dy
    return outx,outy
def clickNum(x,y,num):
    x=int(x+root.winfo_x()+root.winfo_width())
    y=int(y+root.winfo_y())
    mouse=PyMouse()
    for i in range(0,num):
        mouse.click(x,y)
        time.sleep(0.01)
def connect():
    global ip
    os.system(f"{adb_path} connect {ip.get()}")
def scrcpy():
    global size,bitrate
    os.system(f"{scrcpy_path} --stay-awake --crop 1080:1900:0:0 -m {windowHeight} --codec-options bitrate=2000000")
def run():
    global size,bitrate
    threading.Thread(target=scrcpy,daemon=True).start()
def grab(wx,wy,width,height):
    global screen
    screen = ImageGrab.grab((wx,wy,wx+width,wy+height))
    colors=[]
    print("")
    for y in range(0,7):
        colors.append([])
        for x in range (0,7):
            colors[y].append(0)
            if abs(x-y)<=3:#ensure borders
                color=rgb2num(screen.getpixel(packcoords(x,y)))
                colors[y][x]=color
            print(colors[y][x],end="")
        print("")
    return colors
def simulateClick(x,y,clicks,colors):
    global mode
    xys=[[-1,-1],[0,-1],[-1,0],[0,0],[1,0],[0,1],[1,1]]
    for xy in xys:
        x2=x+xy[0]
        y2=y+xy[1]
        if x2>=0 and x2<=6 and y2>=0 and y2<=6:
            if colors[y2][x2]>=1:
                colors[y2][x2]=colors[y2][x2]+clicks
                if mode.get()==0:
                    while colors[y2][x2]>2:
                        colors[y2][x2]=colors[y2][x2]-2
                else:
                    while colors[y2][x2]>6:
                        colors[y2][x2]=colors[y2][x2]-6
numDictHard={
    "1121":[0,1,0,0],
    "1212":[0,1,1,0],
    "1222":[0,0,1,0],
    "2112":[1,0,0,0],
    "2122":[0,0,0,1],
    "2211":[0,0,1,1],
    "2221":[1,0,1,0]
}
numDictExpert={
    "1141":[0,3,0,0],
    "1216":[0,1,1,2],
    "1246":[2,0,1,4],
    "1315":[4,0,0,2],
    "1345":[2,1,0,0],
    "1414":[0,3,1,0],
    "1444":[0,0,1,0],
    "1513":[4,2,0,0],
    "1543":[0,1,0,2],
    "1612":[2,1,1,0],
    "1642":[0,2,1,4],
    "2116":[1,4,0,0],
    "2146":[0,0,0,5],
    "2215":[0,4,1,1],
    "2245":[0,1,1,1],
    "2314":[1,0,0,4],
    "2344":[4,0,0,1],
    "2413":[1,1,1,0],
    "2443":[3,0,1,2],
    "2512":[5,0,0,0],
    "2542":[2,0,0,3],
    "2611":[0,2,1,3],
    "2641":[1,0,1,4],
    "3115":[0,0,0,4],
    "3145":[2,5,0,0],
    "3214":[0,1,1,0],
    "3244":[0,4,1,0],
    "3313":[4,0,0,0],
    "3343":[1,0,0,3],
    "3412":[3,0,1,1],
    "3442":[0,0,1,4],
    "3511":[0,4,0,0],
    "3541":[0,1,0,0],
    "3616":[1,0,1,3],
    "3646":[4,0,1,0],
    "4114":[3,0,0,0],
    "4144":[0,0,0,3],
    "4213":[2,0,1,1],
    "4243":[1,2,1,0],
    "4312":[1,0,0,2],
    "4342":[0,2,0,1],
    "4411":[0,0,1,3],
    "4441":[3,0,1,0],
    "4516":[1,2,0,0],
    "4546":[2,0,0,1],
    "4615":[0,2,1,1],
    "4645":[1,0,1,2],
    "5113":[0,0,0,2],
    "5143":[0,3,0,2],
    "5212":[0,1,1,4],
    "5242":[2,0,1,0],
    "5311":[0,2,0,0],
    "5341":[0,5,0,0],
    "5416":[0,3,1,2],
    "5446":[0,0,1,2],
    "5515":[2,0,0,0],
    "5545":[0,1,0,4],
    "5614":[1,0,1,1],
    "5644":[0,2,1,0],
    "6112":[0,3,0,1],
    "6142":[0,0,0,1],
    "6211":[2,0,1,5],
    "6241":[0,1,1,3],
    "6316":[1,0,0,0],
    "6346":[1,3,0,0],
    "6415":[0,0,1,1],
    "6445":[0,3,1,1],
    "6514":[0,1,0,3],
    "6544":[3,1,0,0],
    "6613":[0,2,1,5],
    "6643":[1,0,1,0]
}

def screenshot():
    grab(root.winfo_x()+root.winfo_width(),root.winfo_y(),windowWidth,windowHeight)
    screen.save("arrowpuzzle.png")
def clickOrSimulate(colors,click=0):
    for y in range(0,7):
        for x in range (6,-1,-1):
            color=colors[y][x]
            if abs(x-y)<=3:
                if color>1 and abs(x-y-1)<=3 and y<6:
                    cx,cy=packcoords(x,y+1)
                    if mode.get()==1:
                        if click==1:
                            clickNum(cx+5,cy+5,7-color)
                        colors=simulateClick(x,y+1,7-color,colors)
                    else:
                        if click==1:
                            clickNum(cx+5,cy+5,1)
                        colors=simulateClick(x,y+1,1,colors)
                    return 1
def autoclick(colors):
    global mode,kill
    colorstmp=copy.deepcopy(colors)
    while (not kill and clickOrSimulate(colorstmp,0))==1:
        pass
    bottom=colorstmp[6][3:7]
    bottom.reverse()
    bottomnum=""
    for i in bottom:
        bottomnum=bottomnum+str(i)
    if bottomnum=="1111":
        clickTop=[0,0,0,0]
    elif mode.get()==1:
        clickTop=numDictExpert[bottomnum]
    else:
        clickTop=numDictHard[bottomnum]
    for x in range(0,4):
        cx,cy=packcoords(x,0)
        clickNum(cx+5,cy+5,clickTop[x])
        simulateClick(x,0,clickTop[x],colors)
    while (not kill and clickOrSimulate(colors,1)==1):
        pass
    return 1
        
def automate():
    global root,kill,colors
    kill=0
    clickNum(100,100,10)
    finalcolors=[
        [2,2,2,2,0,0,0],
        [2,2,2,2,2,0,0],
        [2,2,2,2,2,2,0],
        [2,2,2,2,2,2,2],
        [0,2,2,2,2,2,2],
        [0,0,2,2,2,2,2],
        [0,0,0,2,2,2,2]]
    while(not kill):
        global windowWidth,windowHeight
        colors=grab(root.winfo_x()+root.winfo_width(),root.winfo_y(),windowWidth,windowHeight)
        if colors==finalcolors:
            clickNum(250,900,1)
            time.sleep(0.5)
            colors=grab(root.winfo_x()+root.winfo_width(),root.winfo_y(),windowWidth,windowHeight)
        while ((not kill) and autoclick(colors)<1):
            pass
        time.sleep(0.1)
root=tkinter.Tk()
root.geometry("200x200+100+100")
root.title("ArrowPuzzleAuto")
try:    #windows
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
except:
    ScaleFactor=75
style=ttk.Style()
try:
    style.theme_use("vista")
except:
    style.theme_use("default")
ip=StringVar()
mode=IntVar()
mode.set(1)
ipLabel=ttk.Label(root,text="ip")
ipLabel.place(relx=0,rely=0,relheight=0.2,relwidth=1)
ttk.Entry(ipLabel,textvariable=ip).place(relx=0.3,rely=0,relheight=1,relwidth=0.7)
connectButton=ttk.Button(root,text="Connect",command=connect)
connectButton.place(relx=0,rely=0.2,relheight=0.2,relwidth=0.5)
ttk.Label(root,text="F10 to stop").place(relx=0,rely=0.4,relheight=0.2,relwidth=0.5)

ttk.Button(root,text="Run",command=run).place(relx=0.5,rely=0.2,relheight=0.2,relwidth=0.5)
ttk.Button(root,text="Automate",command=automate).place(relx=0,rely=0.8,relheight=0.2,relwidth=1)
ttk.Button(root,text="Screenshot",command=screenshot).place(relx=0.5,rely=0.4,relheight=0.2,relwidth=0.5)
ttk.Radiobutton(root,text="Hard",variable=mode,value=0).place(relx=0,rely=0.6,relheight=0.2,relwidth=0.5)
ttk.Radiobutton(root,text="Expert",variable=mode,value=1).place(relx=0.5,rely=0.6,relheight=0.2,relwidth=0.5)


def killThread():
    KeyDown().run()
threading.Thread(target=killThread,daemon=True).start()

root.mainloop()
