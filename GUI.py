import Tkinter as tk
import pickle
import time as TIME

from PIL import Image, ImageTk
from datetime import *

from library.dataThread import dataThread
from library.event import *
from library.pay import wait_for_payment
#from library.SPPServer import serverThread

event = Event(TO="Brian & Kofi", date=datetime.date)
venue = Tournament(event, "Venue", 1)
singles = Tournament(event, "Singles", 1)
doubles = Tournament(event, "Doubles", 1)

def main():
  #Get info about tournament
  number = raw_input("What number Moal is this? ")
  try:
    num = int(number)
  except ValueError:
    print "Please enter a number."
    exit()
  event.name = "MoaL " + str(num)
  inp = raw_input("Full Reg (F) or Server Reg (S) ")
  if inp == "F": 
    app = GUI(None)
    app.mainloop()
  elif inp == "S":
    app = Simple(None)
    app.mainloop()

class Simple(tk.Tk):
  def __init__(self, parent):
    tk.Tk.__init__(self, parent)
    self.parent = parent
    self.title("Man on a Ledge Registration.")
    self.protocol('WM_DELETE_WINDOW', self.close)
    # Chage to false in release
    self.state = False
    self.toggle_fullscreen()
    self.bind('<F11>', self.toggle_fullscreen)
    self.bind('<Escape>', self.disable_fullscreen)
    self.lock = ''
    #load Data
    #self.event = pickle.load(open("MoaL.pkl", "rb"))
    self.event = event
    moal_pil = Image.open("assets/TOP.gif")
    moal_photo = ImageTk.PhotoImage(moal_pil)
    self.moal_logo = tk.Label(self,  image=moal_photo)
    self.moal_logo.photo = moal_photo
    self.moal_logo.pack(side='left', fill='both')
    
    pitt_smash_pil = Image.open("assets/BOTTOM.gif")    
    pitt_smash_photo = ImageTk.PhotoImage(pitt_smash_pil)
    self.pitt_logo = tk.Label(self, image=pitt_smash_photo)
    self.pitt_logo.photo = pitt_smash_photo
    self.pitt_logo.pack(side='right', fill='both')

    self.thread = dataThread('data', self.event, self.lock)
    self.thread1 = serverThread('server', self.event, self.lock)
    self.thread.start()
    self.thread1.start()

  def toggle_fullscreen(self, event=None):
    self.state = not self.state
    self.attributes("-fullscreen", self.state)
    return "break"

  def disable_fullscreen(self, event=None):
    self.attributes("-fullscreen", False)
    return "break"

  def close(self):
    self.thread.exitFlag = 1
    self.thread1.exitFlag = 1
    while self.thread.isAlive():
      pass
    while self.thread1.isAlive():
      pass
    self.destroy()

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
    self.lock = ''
    # Create event and venue and doubles singles etc.
    #self.event = pickle.load(open("MoaL.pkl", "rb"))
    self.event = event
    # Getting screen size data.
    self.width = self.winfo_screenwidth()
    self.height = self.winfo_screenheight()
    size = (self.height/2, self.height/2)
    self.framewidth = self.width - (self.height/2)
    self.frameheight = self.height/6

    #Setting Data Entry Fields
    self.name_frame = entryFrame(self, self.framewidth, self.frameheight, 
    	                         "Name: ")
    self.name_frame.grid(row=0, column=0, sticky='NSEW')

    self.tag_frame = entryFrame(self, self.framewidth, self.frameheight, 
    	                        "Tag: ")
    self.tag_frame.grid(row=1, column=0, sticky='NSEW')

    self.loc_frame = entryFrame(self, self.framewidth, self.frameheight, 
    	                        "Location: ")
    self.loc_frame.grid(row=2, column=0, sticky='NSEW')

    self.tourn_frame = tournFrame(self, self.framewidth, self.frameheight)
    self.tourn_frame.grid(row=3, column=0, sticky='NSEW')

    self.teammate_frame = entryFrame(self, self.framewidth, self.frameheight, 
    	                             "Teammate: ")
    self.teammate_frame.grid(row=4, column=0, sticky='NSEW')
    self.teammate_frame.entry.configure(state='disabled')

    self.reg_frame = regFrame(self, self.framewidth, self.frameheight)
    self.reg_frame.grid(row=5, column=0, sticky='NSEW')
    
    # Setting Images
    moal_pil = Image.open("assets/TOP.gif")
    moal_pil.thumbnail(size, Image.ANTIALIAS)
    moal_photo = ImageTk.PhotoImage(moal_pil)
    self.moal_logo = tk.Label(self,  image=moal_photo)
    self.moal_logo.photo = moal_photo
    self.moal_logo.grid(row=0, column=1, rowspan=3)

    pitt_smash_pil = Image.open("assets/BOTTOM.gif")    
    pitt_smash_pil.thumbnail(size, Image.ANTIALIAS)
    pitt_smash_photo = ImageTk.PhotoImage(pitt_smash_pil)
    self.pitt_logo = tk.Label(self, image=pitt_smash_photo)
    self.pitt_logo.photo = pitt_smash_photo
    self.pitt_logo.grid(row=3, column=1, rowspan=3)

    #Spawn Thread
    self.thread = dataThread('data', self.event, self.lock)
    self.thread.start()

  def toggle_fullscreen(self, event=None):
    self.state = not self.state
    self.attributes("-fullscreen", self.state)
    return "break"

  def disable_fullscreen(self, event=None):
    self.attributes("-fullscreen", False)
    return "break"

  def teammate(self):
    if self.tourn_frame.doubles.get() == 0:
      self.teammate_frame.entry.configure(state='disabled')
    else:
      self.teammate_frame.entry.configure(state='normal')

  def register(self):    
    name = self.name_frame.var.get()
    tag = self.tag_frame.var.get()
    location = self.loc_frame.var.get()
    if name == '' or tag == '' or location == '':
      return
    singles = self.tourn_frame.singles.get()
    doubles = self.tourn_frame.doubles.get()
    #payment
    self.check_for_payment(1 + singles + doubles)
    entrant = Entrant(self.event, name, tag, location)
    Tournament_Entrant(self.event.tournaments.tournaments[0], entrant)
    #Tournament_Entrant(venue, entrant)
    if singles == 1:
      #print "Singles"
      Tournament_Entrant(self.event.tournaments.tournaments[1], entrant)
      #Tournament_Entrant(singles, entrant)
    if doubles == 1:
      mate = self.teammate_frame.var.get()
      #print mate
      Tournament_Entrant(self.event.tournaments.tournaments[2], entrant, mate)
      #Tournament_Entrant(doubles, entrant)
    self.name_frame.var.set("")
    self.tag_frame.var.set("")
    self.loc_frame.var.set("")
    self.teammate_frame.var.set("")
    self.teammate_frame.entry.configure(state='disabled')
    self.tourn_frame.single_check.deselect()
    self.tourn_frame.double_check.deselect()
    #pickle.dump(self.event, open("MoaL.pkl", "wb"), -1)

  def check_for_payment(self, price):
    pass
    #self.pay = payWindow(self, price)
    #wait_for_payment(price)
    #for i in range(100):
    #    print "BUtt"
    #TIME.sleep(self.pay.get())
    #self.pay.destroy()

  def close(self):
    self.thread.exitFlag = 1
    while self.thread.isAlive():
      pass
    self.destroy()

class entryFrame(tk.Frame):
  def __init__(self, parent, w, h, labeltext):
    tk.Frame.__init__(self, parent, width=w, height=h, colormap="new")
    self.parent = parent
    self.pack_propagate(0)
    self.var = tk.StringVar()
    self.label = tk.Label(self, text=labeltext, anchor='e', justify='right', 
    	                  font=('MS GOTHIC', 54))
    self.label.pack(side="left", fill="both")
    self.entry = tk.Entry(self, textvariable=self.var, 
                          font=('MS GOTHIC', 54))
    self.entry.pack(side="right")

class tournFrame(tk.Frame):
  def __init__(self, parent, w, h):
    tk.Frame.__init__(self, parent, width=w, height=h, colormap="new")
    self.parent = parent
    self.pack_propagate(0)
    self.singles = tk.IntVar()
    self.doubles = tk.IntVar()
    self.single_check = tk.Checkbutton(self, text='Melee Singles',
                                        variable=self.singles,
                                        font=('MS GOTHIC', 36))
    self.single_check.pack(side='left', fill='both')
    self.double_check = tk.Checkbutton(self, text='Melee Doubles', 
    	                               command=self.parent.teammate, 
    	                               variable=self.doubles, 
    	                               font=('MS GOTHIC', 36))
    self.double_check.pack(side='right', fill='both') 

class regFrame(tk.Frame):
  def __init__(self, parent, w, h):
    tk.Frame.__init__(self, parent, width=w, height=h, colormap="new")
    self.parent = parent
    self.pack_propagate(0)
    self.button = tk.Button(self, text="Register", 
                            command=self.parent.register, 
                            font=('MS GOTHIC', 54))
    self.button.place(relx=.5, rely=.5, anchor='center')

class payWindow(tk.Toplevel):
  def __init__(self, parent, price):
    tk.Toplevel.__init__(self)
    self.title("Please Pay")
    self.parent = parent
    self.label = tk.Label(self, text="Please Pay $" + str(price))
    self.label.pack()
    self.time = 3

  def get(self):
    return self.time

if __name__ == '__main__':
  main()