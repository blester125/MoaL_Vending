import threading
import sys
import os
import time
import msvcrt
import pickle

from library.event import *

exitFlag = 0

def print_path(path):
  for i in path:
    if isinstance(i, Entrant):
      word = i.get_tag()
    else:
      word = i.get_name()
    sys.stdout.write(word + '/')

def print_prompt():
  sys.stdout.write("$ ")

def back(path):
  path.pop()
  return path[-1]

def string_compare(string1, string2):
  if string1.upper() == string2.upper():
    return True
  return False

def help_screen():
  print "~~~~~~~~~~~~~~~~~~~~~~~Simple Data Edits~~~~~~~~~~~~~~~~~~~~~~~~~~"
  print "|Avaiable commands:                                              |"
  print "|  help | h | ?:             Display this screen.                |"
  print "|  list | ls:                Displays list of the current data.  |"
  print "|  select | cd line_number:  Select a data object to examine it. |"
  print "|  remove | rm line_number:  Remove the data at a line number.   |" 
  print "|  edit (Entrant only):      Edit the data of an Entrant.        |"
  print "|  back:                     Return to the last peice of data.   |"
  print "|  save:                     Save the data.                      |"
  print "|  q:                        Quit and Save data.                 |"
  print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

def select(context, path, number):
  number = number - 1
  item = context.get_item(number)
  if item is not None:
    path.append(item)
    return item
  return context

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
    print "\nEnding Thread: " + self.name

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
    except IOError:
      root = Event()
    context = root
    path.append(root)
    user_input = ''
    while user_input != 'q' and user_input != 'Q':
      print_path(path)
      print_prompt()
      user_input = sys.stdin.readline()
      user_input = user_input[:-1]
      user_input = user_input.strip()
      parts = user_input.split(' ')
      if(string_compare(parts[0], 'help') or string_compare(parts[0], 'h')
          or string_compare(parts[0], '?')):
        help_screen()
      elif string_compare(parts[0], 'list') or string_compare(parts[0], 'ls'):
        context.list_object()
      elif (string_compare(parts[0], 'select') 
              or string_compare(parts[0], 'cd')):
        if len(parts) == 1:
          print "Usage: select line_number."
          continuegit 
        try:
          number = int(parts[1])
        except ValueError:
          print "'select' command takes an integer."
          continue
        context = select(context, path, number)
      elif string_compare(parts[0], 'back'):
        if len(path) == 1:
          continue
        context = back(path)
      elif string_compare(parts[0], 'edit'):
        context.edit()
      elif string_compare(parts[0], 'save'):
        pickle.dump(root, open(root.get_name() + ".pkl", "wb"), -1)
        print "Data has been saved."
      elif not(string_compare(parts[0], 'q') 
                and string_compare(parts[0], 'Q')):
        print (parts[0] + " is not a valid command.  "
          "Enter 'help' for a list of commands.")
    pickle.dump(root, open(root.get_name() + ".pkl", "wb"), -1)