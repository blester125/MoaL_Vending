import sys
import pickle

class contain(object):
  def __init__(self, name="Master"):
    self.name = name
    self.objects = []

  def add(self):
    name = raw_input("Enter name of new object: ")
    self.add_object(myObject(name))
    print name + " was Added."

  def add_object(self, item):
    self.objects.append(item)

  def list_object(self):
    for i, j in enumerate(self.objects):
      print str(i+1) + ": " + j.get_name()

  def get_item(self, number):
    try:
      return self.objects[number]
    except:
      print 'Object ' + str(number + 1) + ' does not exist'
      return None

  def remove_item(self, number):
    item = self.objects.pop(number - 1)
    print item.name + " was Removed."

  def start_edit(self, numebr):
    print "This Item cannot be Edited"

  def get_name(self):
    return self.name
    
class myObject(object):
  def __init__(self, name):
    self.name = name
    self.location = "here"
    self.objects = ['a', 'b', 'c', 'd']

  def list_object(self):
    print "1: Name = " + self.name
    print "2: Locaiton = " + self.location
    print "3: objects"
    for i, j in enumerate(self.objects):
      print "  " + str(i + 1) + ": " + j

  def get_name(self):
    return self.name

  def get_item(self, number):
    print "You cannot use select in this context."
    return None
  
  def remove_item(self, number):
    item = self.objects.pop(number - 1)
    print item + " was Removed."

  def add(self):
    item = raw_input("Enter a New Letter: ")
    self.objects.append(item)
    print item + " was Added."
  
  def start_edit(self, number):
    if number == 1:
      user_input = raw_input("Enter new value for Name: ")
      if user_input == '':
        return 
      self.name = user_input
    if number == 2:
      user_input = raw_input("Enter new value for Location: ")
      if user_input == '':
        return 
      self.location = user_input

def print_path(path):
  for i in path:
    sys.stdout.write(i.name + '/')


def select(context, path, number):
  item = context.get_item(number)
  if item is not None:
    path.append(item)
    return item
  return context

def back(path):
  path.pop()
  return path[-1]

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

def string_compare(string1, string2):
  if string1.upper() == string2.upper():
    return True
  return False

def main():
  root = ''
  context = ''
  path = []
  try:
    f = open("ex_data_base.pkl", "rb")
    root = pickle.load(f)
  except:
    root = contain()
  context = root
  path.append(root)
  user_input = ''
  while user_input != 'q' and user_input != 'Q':
    print_path(path)
    print_prompt()
    user_input = raw_input()
    parts = user_input.split(' ')
    ## Help command.
    if(string_compare(parts[0], 'help') or string_compare(parts[0], 'h')
         or string_compare(parts[0], '?')):
      help_screen()      
    ## List command.
    elif string_compare(parts[0], 'list') or string_compare(parts[0], 'ls'):
      context.list_object()  
    ## Select command.
    elif string_compare(parts[0], 'select'):
      if len(parts) == 1:
        print "Usage: select line_number."
        continue
      try:
        number = int(parts[1])
      except:
        print "'select' command takes an integer."
        continue
      context = select(context, path, number - 1)

      
    ## Back command.
    elif string_compare(parts[0], 'back'):
      if len(path) <= 1:
        continue
      context = back(path)
    ## Remove command.
    elif string_compare(parts[0], 'remove') or string_compare(parts[0], 'rm'):
      if len(parts) == 1:
        print "Usage: remove line_number | rm line_number."
        continue
      try:
        number = int(parts[1])
      except:
        print "'remove' command takes an integer."
        continue
      context.remove_item(number)
    ## Edit command.
    elif string_compare(parts[0], 'edit'):
      if len(parts) == 1:
        print "Usage: edit line_number."
        continue
      try:
        number = int(parts[1])
      except:
        print "'edit' command takes an integer."
        continue
      context.start_edit(number)
    ## Add command.
    elif string_compare(parts[0], 'add'):
      context.add()
    ## Save command.
    elif string_compare(parts[0], 'save'):
      pickle.dump(root, open("ex_data_base.pkl", "wb"), -1)
      print "Data has been saved."
    ## Unrecognized command.
    elif (not(string_compare(parts[0], 'q') or string_compare(parts[0], 'Q'))):
      print parts[0] + ' is not a valid command.'
      help_screen()
  pickle.dump(root, open("ex_data_base.pkl", "wb"), -1)

if __name__ == '__main__':
  main()