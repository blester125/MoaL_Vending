import threading
import sys
import os
import time
import pickle

from library.event import *
from library.challonge import *

exitFlag = 0
OS = sys.platform
if OS == 'win32':
  import msvcrt
if OS == 'linux' or OS == 'linux2':
  import select as sel

USERNAME = ''
API_KEY = ''
config_file = open("config.txt", 'r')
for line in config_file:
  parts = line.split(":")
  if parts[0] == "username":
    if parts[1].endswith('\n'):
      parts[1] = parts[1][:-1]
    USERNAME = parts[1]
  elif parts[0] == "APIKey":
    if parts[1].endswith('\n'):
      parts[1] = parts[1][:-1]
    API_KEY = parts[1]
  
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

def output(root, tourntype):
  if string_compare(tourntype, "singles"):
    #fetch singles list
    tourntype = "Singles"
    ent_list = fetch_singles(root)
    ent_list = seed_sort(ent_list)
  elif string_compare(tourntype, "doubles"):
    #fetch doubles list
    tourntype = "Doubles"
    ent_list = fetch_doubles(root)
  else:
    return
  #create tournament
  api.set_credentials(USERNAME, API_KEY)
  bracket_name = root.name + " Melee " + tourntype
  bracket_url = bracket_name.replace(" ", "")
  t = tournaments.create(bracket_name, bracket_url, subdomain="moal",
                               tournament_type="double elimination")
  #add entrants
  fout = open(bracket_url + ".txt", 'w+')
  for i in ent_list:
    fout.write(i + "\n")
    participants.create(t['id'], i)
  fout.close

def fetch_singles(root):
  list = []
  #change to look for singles
  for i in root.tournaments.tournaments[1].entrants:
    list.append(i.tag) 
  return list

def fetch_doubles(root):
  list = []
  #make list
  #change to look for doubles
  for i in root.tournaments.tournaments[2].entrants:
    team = ''
    for j in i.tournaments:
      if j.name == "Doubles":
        team = j.get_teammate()
    item = (i.tag, team)
    list.append(item)
  remove_doubles(list)
  list2 = []
  for i in list:
    list2.append(i[0] + " + " + i[1])
  return list2

def remove_doubles(list):
  for i in list:
    person_1 = i[0]
    person_2 = i[1]
    for j in list:
      if string_compare(j[0], person_2) and string_compare(j[1], person_1):
        list.remove(j)

def seed_sort(ent_list):
  seed_list = []
  new_list = []
  fin = open("seed.txt", "r")
  for line in fin:
    line = line[:-1]
    seed_list.append(line)
  for i in seed_list:
    if i in ent_list:
      new_list.append(i)
      ent_list.remove(i)
  for i in ent_list:
    new_list.append(i)
  fin.close()
  return new_list
  for i in new_list:
    print i

def pizza(root):
	total_pizza = 0
	for i in root.entrants.entrants:
		total_pizza += i.pizza
	print "Buy " + str(total_pizza / 6.0) + " Pizza(s)"

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

  # rewrite to make it look better for linux
  def access_data_base(self):
    while not self.exitFlag:
      if OS == 'win32':
        user_input = self.read_input("Access the Data base? (Y, y): ")
      elif OS == 'linux2':
        user_input = self.read_in("Access the Data base? (Y, y): ")
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

  # rewrite to make it look better for linux
  def read_in(self, caption, timeout=1):
    start_time = time.time()
    line = ''
    if self.flag == 0:
      sys.stdout.write('%s'%(caption))
      self.flag = 1
    while True:
      if sys.stdin in sel.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        line = line[:-1]
        if line != '':
          self.flag = 0
          return line
      if (time.time() - start_time) > timeout:
        if line != '':
          self.flag = 0
        return ''

  def start_data_base(self):
    root = ''
    context = '' 
    path = []
    root = self.data
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
          continue
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
      elif string_compare(parts[0], 'add'):
        context.add()
      elif string_compare(parts[0], 'output'):
        if len(parts) == 1:
          print "Usage: output singles|doubles"
          continue
        #if (not string_compare(parts[1], "singles") or 
        #    not string_compare(parts[1],  "doubles")):
        #  print 'Please specify "singles" or "doubles"'
        #  continue
        output(root, parts[1])
      elif string_compare(parts[0], 'pizza'):
      	pizza(root)
      elif not(string_compare(parts[0], 'q') 
                and string_compare(parts[0], 'Q')):
        print (parts[0] + " is not a valid command.  "
          "Enter 'help' for a list of commands.")
   ## pickle.dump(root, open(root.get_name() + ".pkl", "wb"), -1