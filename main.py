from subprocess import call
from tkinter import *

# 設定window
window = Tk()
window.resizable(0, 0)
window.configure(background = "black")
window.attributes("-fullscreen", True)
window.attributes("-topmost", True)
window.focus_force()

# 顯示起始圖片(第一張圖片)
photo = PhotoImage(file="balloon(01).gif")
label = Label(window, image=photo)
label.config(width=500)
label.config(height=500)
label.pack()

# 播放影片
def play_video():
  call(["omxplayer", "-o", "local", "qqbz.mp4"])

# 設定接到訊號時的方法
index = 2
def switch_image(e):
  global index

  if index < 16:
    fileName = "balloon(" + str(index) + ").gif"
    newPhoto = PhotoImage(file=fileName)
    label.config(image = newPhoto)
    label.image = newPhoto

    index += 1
  else:
    play_video()
    index = 2

# 設定接到訊號時的方法
window.bind("<KeyPress>", switch_image)

window.mainloop()
