#!/usr/bin/python

import Tkinter

class simpleapp_tk(Tkinter.Tk):
  def __init__(self, parent):
    Tkinter.Tk.__init__(self, parent)
    self.parent = parent
    self.initialize()
    
  def initialize(self):
    self.grid()
    
    self.entryVariable = Tkinter.StringVar()
    self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
    self.entry.grid(column=0, row=0, sticky='EW')
    self.entry.bind("<Return>", self.OnPressEnter)
    self.entryVariable.set(u'Enter Text Here!')
    
    button = Tkinter.Button(self, text=u'Click me!', command=self.OnButtonClick)
    button.grid(column=1, row=0)
    
    self.labelVariable = Tkinter.StringVar()
    label = Tkinter.Label(self, textvariable=self.labelVariable, anchor="w", fg="white", bg="blue")
    label.grid(column=0, row=1, columnspan=2, sticky="EW")
    self.labelVariable.set(u'Hello!')
    
    self.grid_columnconfigure(0, weight=1)
    self.resizable(True, False)
    self.update()
    self.geometry(self.geometry())
    self.entry.focus_set()
    self.entry.selection_range(0, Tkinter.END)
    
  def OnButtonClick(self):
    print "You Clicked the Button!"
    self.labelVariable.set(self.entryVariable.get() + " (You Clicked the Button!)")
    self.entry.focus_set()
    self.entry.selection_range(0, Tkinter.END)
    
  def OnPressEnter(self, event):
    print "You pressed Enter!"
    self.labelVariable.set(self.entryVariable.get() + " (You pressed Enter!)")
    self.entry.focus_set()
    self.entry.selection_range(0, Tkinter.END)
    
if __name__ == "__main__":
  app = simpleapp_tk(None)
  app.title('my Application')
  app.mainloop()
  