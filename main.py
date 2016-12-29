from subprocess import call
from tkinter import *
from PIL import Image, ImageTk

# 設定起始變數
window = Tk()
label = Label(window)
raw_image = Image.open("balloon(1).gif")
index = 1
image_num = 16
ratio = 0

# 設定window & label
window.configure(background = "black")
window.attributes("-fullscreen", True)
window.attributes("-topmost", True)
window.focus_force()
label.config(borderwidth = 0)
window.update()    # Make sure window will render at this time

# 取得正確的image scale ratio
ratio = min( window.winfo_width() / raw_image.size[0], window.winfo_height() / raw_image.size[1])

# 開啟起始圖片
def switch_image(e):
  global index
  global ratio

  if index < image_num:
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
