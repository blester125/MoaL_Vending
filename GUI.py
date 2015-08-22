import Tkinter as tk
import pickle

from dataThread import dataThread

from library.event import *

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
    #create event and venue and doubles singles etc.
    self.event = pickle.load(open("MoaL.pkl", "rb"))
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
    self.thread = dataThread('test', self.event, lock)
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
    name = self.name_entry.get()
    tag = self.tag_entry.get()
    location = self.loc_entry.get()
    if name == '' or tag == '' or location == '':
      return
    entrant = Entrant(self.event, name, tag, location)
    Tournament_Entrant(self.event.tournaments.tournaments[0], entrant)
    #Tournament_Entrant(venue, entrant)
    if self.singles.get() == 1:
      Tournament_Entrant(self.event.tournaments.tournaments[1], entrant)
      #Tournament_Entrant(singles, entrant)
    if self.doubles.get() == 1:
      mate = self.teammate_entry.get()
      Tournament_Entrant(self.event.tournaments.tournaments[2], entrant, mate)
      #Tournament_Entrant(doubles, entrant)
    self.name_entry.delete(0, 'end')
    self.tag_entry.delete(0, 'end')
    self.loc_entry.delete(0, 'end')
    self.teammate_entry.delete(0, 'end')
    #pickle.dump(self.event, open("MoaL.pkl", "wb"), -1)

  def close(self):
    self.thread.exitFlag = 1
    while self.thread.isAlive():
      pass
    self.destroy()

if __name__ == '__main__':
  app = GUI(None)
  app.mainloop()