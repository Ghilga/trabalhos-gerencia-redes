from tkinter import *
from tkinter import ttk

defaultFont='futura'

window = Tk()
window.title('Network Manager')
window.geometry('620x620')

frame = ttk.Frame(window, padding=10, relief=SUNKEN)
frame.grid()

deviceInfoLabel = Label(frame, text='testLabel', font=defaultFont, )
deviceInfoLabel.grid(row=0,column=0)

window.mainloop()