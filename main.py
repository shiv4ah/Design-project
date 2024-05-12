from tkinter import *
from PIL import ImageTk,Image
import tkinter

window=tkinter.Tk()
window.geometry("700x600")
window.title("student_attentive")
class sample:
    name="guru"
    text="Student Attentive"

image_0=Image.open('static/class.jpg')nn
bck_end=ImageTk.PhotoImage(image_0)

def login():
    window.destroy()
    import log
def register():
    window.destroy()
    import register
window.mainloop()
