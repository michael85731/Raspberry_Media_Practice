import time
import simpleaudio as sa
import RPi.GPIO as GPIO
from subprocess import call
from tkinter import *
from PIL import Image, ImageTk

# 設定起始變數
window = Tk()
label = Label(window)
index = 0
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
window.focus_force()
label.config(borderwidth = 0)
window.update()    # Make sure window will render at this time

# 取得等比例縮放的的image scale ratio
raw_image = Image.open("balloon(1).gif")
ratio = min( window.winfo_width() / raw_image.size[0], window.winfo_height() / raw_image.size[1])

# 讀取所有圖片
target_images = []
for i in range(1, image_num + 1):
  fileName = "balloon(" + str(i) + ").gif"
  raw_image = Image.open(fileName)
  raw_image = raw_image.resize( (window.winfo_width(), window.winfo_height()), Image.BILINEAR )
  target_images.append(ImageTk.PhotoImage(raw_image))

# 讀取pump音效
raw_audio = open("pump.wav", "rb")
raw_audio = raw_audio.read()
target_audio = sa.WaveObject(raw_audio, 2, 2, 44100)

def action():
  global index

  if index < image_num:
    switch_image(index)
    if index != 0:
      play_pump()
    index += 1
  else:
    label.pack_forget()
    window.update()
    play_video()
    index = 0
    action()

  window.update()

# 切換圖片
def switch_image(index):
  label.image = target_images[index]
  label.config(image = target_images[index])
  label.pack()

# 播放影片
def play_video():
  call(["omxplayer", "-o", "local", "explode.mp4"])
  call(["omxplayer", "-o", "local", "after.mp4"])

# 播放pum音效
def play_pump():
  target_audio.play()

# 點螢幕關機
def shutdown(e):
  call(["shutdown", "-h", "now"])

window.bind("<B1-Motion>", shutdown)
action() # 執行第一次

# 不斷讀取GPIO，並執行對應method
while True:
  window.update()
  button_state = GPIO.input(pin)

  if flag != button_state:
    if button_state:
      action()
    flag = button_state


window.mainloop()
