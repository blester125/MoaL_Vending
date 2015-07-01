import Tkinter
import time

from dataThread import dataThread

class GUI(Tkinter.Tk):
  def __init__(self, parent):
    Tkinter.Tk.__init__(self, parent)
    self.parent = parent
    self.title("TESTING")
    self.protocol('WM_DELETE_WINDOW', self.close)
    self.geometry("200x100")
    self.button = Tkinter.Button(self, text="YOO", command=self.add)
    self.button.pack()
    self.entry = Tkinter.Entry(self)
    self.entry.pack()
    self.data = ['apple', 'banana', 'grape']
    lock = ''
    self.thread = dataThread('test', self.data, lock)
    self.thread.start()

  def add(self):
    if self.entry.get() != '':
      self.data.append(self.entry.get())
      self.entry.delete(0, 'end')

  def close(self):
    self.thread.exitFlag = 1
    while self.thread.isAlive():
      pass
    self.destroy()

if __name__ == '__main__':
  app = GUI(None)
  app.mainloop()
