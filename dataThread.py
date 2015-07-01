import threading
import sys
import os
import time
import msvcrt

from library.event import *

exitFlag = 0

def print_path(path):
  for i in path:
    sys.stdout.write(i.name + '/')

def print_prompt():
  sys.stdout.write("$ ")

def string_compare(string1, string2):
  if string1.upper() == string2.upper():
    return True
  return False

def help_screen():
  print "~~~~~~~~~~~~~~~~~~~~~~~Simple Data Edits~~~~~~~~~~~~~~~~~~~~~~~~"
  print "|Avaiable commands:                                            |"
  print "|  help | h | ?:            Display this screen.               |"
  print "|  list | ls:               Displays list of the current data. |"
  print "|  select line_number:      Select a data object to examine it.|"
  print "|  remove | rm line_number: Remove the data at a line number.  |" 
  print "|  edit line_number:        Edit the data at line_number.      |"
  print "|  back:                    Return to the last peice of data.  |"
  print "|  add:                     Add a peice of data.               |"
  print "|  save:                    Save the data.                     |"
  print "|  q:                       Quit and Save data.                |"
  print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

class dataThread(threading.Thread):
  def __init__(self, name, data, lock):
    threading.Thread.__init__(self)
    self.name = name
    self.exitFlag = 0
    self.flag = 0
    self.data = data
    self.lock = lock

  def run(self):
    print "Starting Thread: " + self.name
    self.access_data_base()
    print "Ending Thread: " + self.name

  def access_data_base(self):
    while not self.exitFlag:
      user_input = self.read_input("Access the Data base? (Y, y): ")
      if user_input != '':
        print ""
        if user_input == 'Y' or user_input == 'y':
          self.start_data_base()

  def read_input(self, caption, timeout=1):
    start_time = time.time()
    if self.flag == 0:
      sys.stdout.write('%s'%(caption))
      self.flag = 1
    inputs = ''
    while True:
      if msvcrt.kbhit():
        char = msvcrt.getche()
        if ord(char) == 13:
          break
        elif ord(char) >= 32:
          inputs += char
      if len(inputs) == 0 and (time.time() - start_time) > timeout:
        break
    if len(inputs) > 0:
      self.flag = 0
      return inputs
    else:
      return ''

  def start_data_base(self):
    print "In database so quitting the GUI can't close me now."
    root = ''
    context = '' 
    path = []
    ## will be the data from the GUI instead.
    try:
      f = open('event.pkl', 'rb')
      root = pickle.load(f)
    except:
      root = Event()
    context = root
    path.append(root)
    user_input = ''
    while user_input != 'q' and user_input != 'Q':
      print_path(path)
      print_prompt()
      user_input = raw_input()
      parts = user_input.split(' ')
      if(string_compare(parts[0], 'help') or string_compare(parts[0], 'h')
          or string_compare(parts[0], '?')):
        help_screen()
    
