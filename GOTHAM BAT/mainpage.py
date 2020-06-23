import tkinter
import os
from PIL import ImageTk,Image


window = tkinter.Tk()
window.title("Gotham Bat")
window.geometry("840x580")
canvas=tkinter.Canvas(window,width=1000,height=1000)

image=ImageTk.PhotoImage(Image.open('imgs2\\main_bg.jpg'))

canvas.create_image(0,0,anchor='nw',image=image)
canvas.place(x=0,y=0,relwidth=1, relheight=1)



# background_image=tkinter.PhotoImage('C:\\Users\\333ya\\Desktop\\Flappy Bird AI incomplete - Copy\\imgs\\main_bg.jpg')
# background_label = tkinter.Label(window, image=background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
# # background_label.image=background_image

def single_player():
	os.system('single_player.py')

def ai_player():
	os.system('ai_player.py')

def p1_vs_p2():
	os.system('p1_vs_p2.py')

def ai_vs_p1():
	os.system('ai_vs_p1.py')

def train_ai():
	os.system('train_ai.py')

single_player=tkinter.Button(window, text ="Single Player", command = single_player).place(x=400,y=80)
ai_player=tkinter.Button(window, text ="AI Player", command = ai_player).place(x=400,y=110)
p1_vs_p2=tkinter.Button(window, text ="Player1 Vs Player2", command = p1_vs_p2).place(x=400,y=140)
ai_vs_p1=tkinter.Button(window, text ="AI Vs Player", command = ai_vs_p1).place(x=400,y=170)
train_ai=tkinter.Button(window, text ="Train AI", command = train_ai).place(x=400,y=200)
window.mainloop()