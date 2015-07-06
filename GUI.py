import Tkinter as tk
import time

from dataThread import dataThread

class GUI(tk.Tk):
  def __init__(self, parent):
    tk.Tk.__init__(self, parent)
    self.parent = parent
    self.title("Man on a Ledge Registration.")
    self.protocol('WM_DELETE_WINDOW', self.close)
    ## Change to false in release.
    self.state = True
    self.toggle_fullscreen()
    self.bind('<F11>', self.toggle_fullscreen)
    lock = ''
    self.data = []
    self.singles = tk.IntVar()
    self.doubles = tk.IntVar()
    self.name_label = tk.Label(self, text="Name: ", anchor='e', 
                                 justify='right')
    self.name_label.grid(row=0, column=0, sticky='NSEW')
    self.name_entry = tk.Entry(self)
    self.name_entry.grid(row=0, column=1)
    self.tag_label = tk.Label(self, text="Tag: ", anchor='e', justify='left')
    self.tag_label.grid(row=1, column=0, sticky='NSEW')            
    self.tag_entry = tk.Entry(self)
    self.tag_entry.grid(row=1, column=1)
    self.loc_label = tk.Label(self, text="Location: ", anchor='e', 
                               justify='right')
    self.loc_label.grid(row=2, column=0, sticky='NSEW')
    self.loc_entry = tk.Entry(self)
    self.loc_entry.grid(row=2, column=1)
    self.singles_check = tk.Checkbutton(self, text="Melee Singles", 
                                         variable=self.singles)
    self.singles_check.grid(row=3, column=1)
    self.doubles_check = tk.Checkbutton(self, text="Melee Doubles", 
                                         command=self.teammate, 
                                         variable=self.doubles)
    self.doubles_check.grid(row=4, column=1)
    self.teammate_label = tk.Label(self, text="Teammate: ", anchor='e', 
                                    justify='right')
    self.teammate_label.grid(row=5, column=0, sticky='NSEW')
    self.teammate_entry = tk.Entry(self, state='disabled')
    self.teammate_entry.grid(row=5, column=1)
    self.thread = dataThread('test', self.data, lock)
    self.thread.start()

  def toggle_fullscreen(self, event=None):
    self.state = not self.state
    self.attributes("-fullscreen", self.state)
    return "break"

  def teammate(self):
    if self.doubles.get() == 0:
      self.teammate_entry.configure(state='disabled')
    else:
      self.teammate_entry.configure(state='normal')

  def close(self):
    self.thread.exitFlag = 1
    while self.thread.isAlive():
      pass
    self.destroy()

if __name__ == '__main__':
  app = GUI(None)
  app.mainloop()
