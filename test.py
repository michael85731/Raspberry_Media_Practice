import pygame
from tkinter import *

# 設定window
window = Tk()
window.resizable(0, 0)
window.configure(background = "black")
window.attributes("-fullscreen", True)
window.attributes("-topmost", True)
window.focus_force()

# 播放影片


## 顯示圖片，起始設第一張圖片
#photo = PhotoImage(file="balloon(01).gif")
#label = Label(window, image=photo)
#label.config(width=500)
#label.config(height=500)
#label.pack()

## 設定press button時的事件
#index = 2
#def press(e):
  #global index

  #if index < 16:
    #if index < 10:
      #fileName = "balloon(" + "0" + str(index) + ").gif"
    #elif index >= 10 and index < 16:
      #fileName = "balloon(" + str(index) + ").gif"

    #newPhoto = PhotoImage(file=fileName)
    #label.config(image = newPhoto)
    #label.image = newPhoto

    #index += 1
  #else:
    #print("play video")

## 設定press事件
#window.bind("<KeyPress>", press)

window.mainloop()
