from subprocess import call
from tkinter import *
from PIL import Image, ImageTk

# 設定window
window = Tk()
window.configure(background = "black")
window.attributes("-fullscreen", True)
window.attributes("-topmost", True)
window.focus_force()
window.update()    # Make sure window will render at this time

# 設定起始變數
raw_image = Image.open("balloon(1).gif")
target_image = ImageTk.PhotoImage(raw_image)
label = Label(window, image=target_image)
label.config(borderwidth = 0)
ratio = min( window.winfo_width() / raw_image.size[0], window.winfo_height() / raw_image.size[1])
index = 1

# 開啟起始圖片
def switch_image(e):
  global index
  global ratio

  if index < 16:
    fileName = "balloon(" + str(index) + ").gif"
    raw_image = Image.open(fileName)
    raw_image = raw_image.resize( (int(raw_image.size[0] * ratio), int(raw_image.size[1] * ratio)), Image.BILINEAR )
    target_image = ImageTk.PhotoImage(raw_image)
    label.image = target_image
    label.config(image = target_image)
    label.pack()

    index += 1
  else:
    label.pack_forget()
    window.update()
    play_video()
    index = 1
    switch_image(0)

# 播放影片
def play_video():
  call(["omxplayer", "-o", "local", "qqbz.mp4"])

window.bind("<KeyPress>", switch_image) # 設定接到訊號時的方法

switch_image(0) # 執行第一次

window.mainloop()
