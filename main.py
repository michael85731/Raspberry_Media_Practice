import subprocess
import RPi.GPIO as GPIO
from subprocess import PIPE
from time import sleep
from tkinter import *
from PIL import Image, ImageTk

# 設定起始變數
window = Tk()
label = Label(window)
index = 0
image_num = 15
ratio = 0
button_flag = False
audio_flag = False
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

# 建立讀取pump音效的process
audio = subprocess.Popen(["omxplayer", "--loop", "--no-osd", "pump.wav"], stdin = PIPE, bufsize = 1)
audio.stdin.write("p".encode())
audio.stdin.flush()

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
  subprocess.call(["omxplayer", "-o", "local", "explode.mp4"])
  subprocess.call(["omxplayer", "-o", "local", "after.mp4"])

# 變換audio_flag
def change_audio_flag():
  audio.stdin.write("p".encode())
  audio.stdin.flush()
  audio_flag = not(audio_flag)

# 播放pum音效
def play_pump():
  global audio_flag

  if not(audio_flag):
    audio.stdin.write("\x1b[D".encode())
    audio.stdin.flush()
    change_audio_flag()
    sleep(1.2)
  else:
    notify_all()
    change_audio_flag()
    audio.stdin.write("\x1b[D".encode())
    audio.stdin.flush()
    change_audio_flag()
    sleep(1.2)

  change_audio_flag()

# 點螢幕關機
def shutdown(e):
  subprocess.call(["shutdown", "-h", "now"])

window.bind("<B1-Motion>", shutdown)
action() # 執行第一次

# 不斷讀取GPIO，並執行對應method
while True:
  window.update()
  button_state = GPIO.input(pin)

  if button_flag != button_state:
    if button_state:
      action()
    button_flag = button_state

window.mainloop()
