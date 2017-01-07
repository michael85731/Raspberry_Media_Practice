import time
import RPi.GPIO as GPIO
from subprocess import call
from tkinter import *
from PIL import Image, ImageTk

# 設定起始變數
window = Tk()
label = Label(window)
raw_image = Image.open("balloon(1).gif")
index = 1
image_num = 15
ratio = 0
flag = False
pin = 12

# 設定GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# 設定window & label
window.configure(background = "black")
window.configure(cursor = "none")
window.attributes("-fullscreen", True)
window.attributes("-topmost", True)
window.focus_force()
label.config(borderwidth = 0)
window.update()    # Make sure window will render at this time

# 取得等比例縮放的的image scale ratio
ratio = min( window.winfo_width() / raw_image.size[0], window.winfo_height() / raw_image.size[1])

def action():
  global index
  global ratio

  if index <= image_num:
    switch_image(index)
    index += 1
  else:
    label.pack_forget()
    window.update()
    play_video()
    index = 1
    action()

# 開啟起始圖片
def switch_image(index):
  fileName = "balloon(" + str(index) + ").gif"
  raw_image = Image.open(fileName)
  #raw_image = raw_image.resize( (int(raw_image.size[0] * ratio), int(raw_image.size[1] * ratio)), Image.BILINEAR )
  raw_image = raw_image.resize( (window.winfo_width(), window.winfo_height()), Image.BILINEAR )
  target_image = ImageTk.PhotoImage(raw_image)
  label.image = target_image
  label.config(image = target_image)
  label.pack()
  window.update()

# 播放影片
def play_video():
  call(["omxplayer", "-o", "local", "qqbz.mp4"])

# 點螢幕關機
def shutdown(e):
  call(["shutdown", "-h", "now"])

window.bind("<B1-Motion>", shutdown)
action() # 執行第一次

while True:
  window.update()
  button_state = GPIO.input(pin)

  if flag != button_state:
    if button_state:
      action()
    flag = button_state


window.mainloop()
