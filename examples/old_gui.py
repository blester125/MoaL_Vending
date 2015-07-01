#!/usr/bin/python

import Tkinter

#event Class info and what is at the event and who runs it
class Event():
  #TO_name
  #date
  #number_of_entrents
  def __init__(self):
    #list of tournament objects
    self.events = []
    self.entrants = []
    
class Tournament():
  def __init__(self):
    self.name = ""
    self.price = 0
    self.total = 0
    self.team = False

class VendingMachine(Tkinter.Tk):
  def __init__(self, parent):
    Tkinter.Tk.__init__(self, parent)
    self.parent = parent
    self.initialize()
    
  def initialize(self):
    self.grid()
    ''' 
    Get the data for what is happening at the tournament 
    Create the Woorkbook?
    '''
    self.MoaLButton = Tkinter.Button(self, text=u'Create MoaL Event', command=self.OnMoaLButtonClick)
    self.MoaLButton.grid()
    #self.OnMoaLButtonClick()
   
  def OnMoaLButtonClick(self):
    self.event = Event()
    self.event.TO_name = "Brian Lester & Kofi Osei"
    self.event.name = "MoaL 41"
    self.event.date = "3/3/3"
    venue = Tournament()
    venue.name = "Venue"
    venue.price = 1
    Singles = Tournament()
    Singles.name = "Singles"
    Singles.price = 1
    Doubles = Tournament()
    Doubles.name = "Doubles"
    Doubles.price = 1
    Doubles.team = True
    self.event.events.append(venue)
    self.event.events.append(Singles)
    self.event.events.append(Doubles)
    self.MoaLButton.grid_forget()    
    self.EntrantData()
   
  def EntrantData(self):
    #self.grid()
    self.Tag_Variable = Tkinter.StringVar()
    self.Tag_Label = Tkinter.Label(self, text=u'Tag:', anchor="w")
    self.Tag_Label.grid(column=0, row=0, columnspan=1, sticky='EW')
    self.Tag_Entry = Tkinter.Entry(self, textvariable=self.Tag_Variable)
    self.Tag_Entry.grid(column=1, row=0, columnspan=2, sticky='EW')
    self.Name_Variable = Tkinter.StringVar()
    self.Name_Label = Tkinter.Label(self, text=u'Name:', anchor='w')
    self.Name_Label.grid(column=0, row=1, columnspan=1, sticky="EW")
    self.Name_Entry = Tkinter.Entry(self, textvariable=self.Name_Variable)
    self.Name_Entry.grid(column=1, row=1, columnspan=2, sticky='EW')
    self.Location_Variable = Tkinter.StringVar()
    self.Location_Label = Tkinter.Label(self, text=u'Region', anchor='w')
    self.Location_Label.grid(column=0, row=2, columnspan=1, sticky="EW")
    self.Location_Entry = Tkinter.Entry(self, textvariable=self.Location_Variable)
    self.Location_Entry.grid(column=1, row=2, columnspan=2, sticky="EW")
    self.Tournaments_Entered = range(0, len(self.event.events))
    counter = 0
    for tournament in self.event.events:
      if tournament.name == "Venue":
        self.Tournaments_Entered[counter] = Tkinter.Variable()
        self.Tournaments_Entered[counter].set(1)
        counter += 1
        continue
      self.Tournaments_Entered[counter] = Tkinter.Variable()
      self.Tournaments_Entered[counter].set(0)
      if tournament.team == True:
        pass
      self.label = Tkinter.Checkbutton(self, text=tournament.name, variable=self.Tournaments_Entered[counter])
      self.label.grid(column=0, row=counter+3, sticky="EW")
      counter += 1
    
    SaveEntrantButton = Tkinter.Button(self, text=u'Register', command=self.SaveEntrant)
    SaveEntrantButton.grid()
    
  def SaveEntrant(self):
    print self.Tag_Variable.get()
    print self.Name_Variable.get()
    print self.Location_Variable.get()
    for i in self.Tournaments_Entered:
      print i.get()
    
    
if __name__ == '__main__':
  app = VendingMachine(None)
  app.title('Tournament Registration')
  app.geometry('1280x720') 
  app.mainloop()