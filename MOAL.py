import Tkinter

from library.event import *
from library.excel import *

class RegWindow(Tkinter.Tk):
  def __init__(self, parent):
    Tkinter.Tk.__init__(self, parent)
    self.title("Man On A Ledge Registration.")
    self.reg_button = Tkinter.Button(self, text="Register")
    self.reg_button.pack()
    self.geometry("500x300+100+100")
  
if __name__ == '__main__':
  app = RegWindow(None)
  app.mainloop()