import bluetooth
import threading

from library.event import *

name="bt_server"
uuid="00001101-0000-1000-8000-00805F9B34FB"

def runServer():
    serverSocket=bluetooth.BluetoothSocket(bluetooth.RFCOMM )
    port=bluetooth.PORT_ANY
    serverSocket.bind(("",port))
    # print "Listening for connections on port: ", port   
    serverSocket.listen(1)
    port=serverSocket.getsockname()[1]

    # the missing piece
    bluetooth.advertise_service( serverSocket, "SampleServer",
                       service_id = uuid,
                       service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                       profiles = [ bluetooth.SERIAL_PORT_PROFILE ] 
                     )

    inputSocket, address=serverSocket.accept()
    # print "Got connection with" , address
    data=inputSocket.recv(1024)
    # print "received [%s] \n " % data    
    inputSocket.close()
    serverSocket.close()  
    return data

class serverThread(threading.Thread):
  def __init__(self, name, data, lock):
    threading.Thread.__init__(self)
    self.name = name
    self.exitFlag = 0
    self.data = data
    self.lock = lock

  def run(self):
    print "Starting Thread: " + self.name 
    while not self.exitFlag:
      data = runServer()
      self.register(data)
    print "\nEnding Thread: " + self.name

  def register(self, data):
    parts = data.split(';')
    name = parts[0]
    tag = parts[1]
    location = parts[2]
    singles = parts[3]
    doubles = parts[4]
    if name == '' or tag == '' or location == '':
      return
    entrant = Entrant(self.data, name, tag, location)
    Tournament_Entrant(self.data.tournaments.tournaments[0], entrant)
    if singles == '1':
      Tournament_Entrant(self.data.tournaments.tournaments[1], entrant)
    if doubles != '':
      Tournament_Entrant(self.data.tournaments.tournaments[2], entrant, 
                         doubles)

if __name__ == '__main__':
    #data = runServer()  
    data = "Brian;Mordicon;PGH;1;Kofi"
    