import socket
import pickle
import os
import random
import sys

localIP     = "127.0.0.1"
localPort = 20001
bufferSize = 32768

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

nack1 = 1 # File does not exist
nack2 = 2 # Invalid offset
ack = 0 # All good to go

client_address = 0


def main():
    global client_address
    print("UDP server up and listening")
    #localPort = int(sys.argv[1])

    UDPServerSocket.bind((localIP, localPort))

    while(True):
      
          bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)#Recieves the dumped request from the client
          message = bytesAddressPair[0]  
          client_address = bytesAddressPair[1]

          request=pickle.loads(message)#loads the dumped request from the client
          fileName , offset , chunkSize = request

          errcode = check4Nack(fileName, offset)

          with open(fileName, 'rb') as file:
               file.seek(offset)
               print(offset)
               data = file.read(chunkSize - 25) 
               resp = pickle.dumps((errcode, len(data), data))
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
  rand = random.randint(0,9)
  print(rand)
  if rand >=1:
      print("tentou mandar")
      UDPServerSocket.sendto(resp, client_address)
  

main()


