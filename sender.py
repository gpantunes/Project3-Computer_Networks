import socket
import pickle
import os
import random
import sys

localIP     = "127.0.0.1"
localPort = 20001
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

nack1 = 1 # File does not exist
nack2 = 2 # Invalid offset
ack = 0 # All good to go

client_address = 0


window = []
windowSize = 4
seqNum = 0


def main():
    global client_address
    global seqNum
    print("UDP server up and listening")
    #localPort = int(sys.argv[1])

    UDPServerSocket.bind((localIP, localPort))

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)#Recieves the dumped request from the client
    message = bytesAddressPair[0]  
    client_address = bytesAddressPair[1]

    request=pickle.loads(message)#loads the dumped request from the client
    fileName, chunkSize = request

    while(True):
      
          offset = seqNum * chunkSize
          errcode = check4Nack(fileName, offset)

          if checkWindow():

          with open(fileName, 'rb') as file:
               file.seek(offset)
               print(offset)
               data = file.read(chunkSize - 29) 
               resp = pickle.dumps((errcode, seqNum, len(data), data))
               #print(resp)
        
               serverReply(resp)
          
          file.close()


def check4Nack(fileName, offset):
     errcode = 0
     if not os.path.exists(fileName):
          errcode = nack1
     elif offset >= os.path.getsize(fileName):
          errcode = nack2
     else:
        errcode = ack   
     return errcode
     

def serverReply(resp):
  global seqNum

  rand = random.randint(0,10)
  print(rand)
  if rand >=3:
      print("tentou mandar")
      window[seqNum] = pickle.loads(resp)
      seqNum += 1
      UDPServerSocket.sendto(resp, client_address)
  


def checkWindow():
     


main()


