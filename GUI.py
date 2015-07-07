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
    self.bind('<Escape>', self.disable_fullscreen)
    lock = ''
    self.data = []
    self.singles = tk.IntVar()
    self.doubles = tk.IntVar()
    self.name_label = tk.Label(self, text="Name:", anchor='e', 
                                 justify='right', font=("MS Gothic", 68))
    self.name_label.grid(row=0, column=0, sticky='NSEW')
    self.name_entry = tk.Entry(self, width=22, font=("MS Gothic", 68))
    self.name_entry.grid(row=0, column=1, sticky='EW')
    self.tag_label = tk.Label(self, text="Tag:", anchor='e', justify='left',
                                font=("MS Gothic", 72))
    self.tag_label.grid(row=1, column=0, sticky='NSEW')            
    self.tag_entry = tk.Entry(self, width=22, font=("MS Gothic", 68))
    self.tag_entry.grid(row=1, column=1, sticky='EW')
    self.loc_label = tk.Label(self, text="Location:", anchor='e', 
                               justify='right', font=("MS Gothic", 68))
    self.loc_label.grid(row=2, column=0, sticky='NSEW')
    self.loc_entry = tk.Entry(self, width=22, font=("MS Gothic", 68))
    self.loc_entry.grid(row=2, column=1, sticky='EW')
    self.singles_check = tk.Checkbutton(self, text="Melee Singles", 
                                         variable=self.singles, 
                                         font=("MS Gothic", 68))
    self.singles_check.grid(row=3, column=1)
    self.doubles_check = tk.Checkbutton(self, text="Melee Doubles", 
                                         command=self.teammate, 
                                         variable=self.doubles,
                                         font=("MS Gothic", 68))
    self.doubles_check.grid(row=4, column=1)
    self.teammate_label = tk.Label(self, text="Teammate:", anchor='e', 
                                    justify='right', font=("MS Gothic", 68))
    self.teammate_label.grid(row=5, column=0, sticky='NSEW')
    self.teammate_entry = tk.Entry(self, state='disabled', width=22, 
                                    font=("MS Gothic", 68))
    self.teammate_entry.grid(row=5, column=1, sticky='EW')
    self.register = tk.Button(self, text="Register", font=("MS Gothic", 68),
                               command=self.register)
    self.register.grid(row=6, column=1, pady=40)
    moal_photo = tk.PhotoImage(file="assets/MoaL.gif")
    self.moal_logo = tk.Label(self,  image=moal_photo)
    self.moal_logo.photo = moal_photo
    self.moal_logo.grid(row=0, column=3, rowspan=3)
    pitt_smash_photo = tk.PhotoImage(file="assets/PittSmash.gif")
    self.pitt_logo = tk.Label(self, image=pitt_smash_photo)
    self.pitt_logo.photo = pitt_smash_photo
    self.pitt_logo.grid(row=3, column=3, rowspan=4)
    self.thread = dataThread('test', self.data, lock)
    self.thread.start()

  def toggle_fullscreen(self, event=None):
    self.state = not self.state
    self.attributes("-fullscreen", self.state)
    return "break"

  def disable_fullscreen(self, event=None):
    self.attributes("-fullscreen", False)
    return "break"

  def teammate(self):
    if self.doubles.get() == 0:
      self.teammate_entry.configure(state='disabled')
    else:
      self.teammate_entry.configure(state='normal')

  def register(self):
    pass

  def close(self):
    self.thread.exitFlag = 1
    while self.thread.isAlive():
      pass
    self.destroy()

if __name__ == '__main__':
  app = GUI(None)
  app.mainloop()