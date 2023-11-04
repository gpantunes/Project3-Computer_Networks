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
nack2 = 2 # Lost packet
ack = 0 # All good to go

client_address = 0


# Dictionary Sliding window
current = 0
packet_payload = []
packetSize = 0

slidingWindow ={
     "key": current,
     "packet": packet_payload,
     "packetSize" : 0 
}


def main():
    global client_address, current, packet_payload, packetSize
    print("UDP server up and listening")
    #localPort = int(sys.argv[1])

    #senderIP = int(sys.argv[1])

    #senderPort = int(sys.argv[2])

    #receiverIP = int(sys.argv[3])

    #receiverPort = int(sys.argv[4])

    fileName = "pila.txt" #sys.argv[5]

    windowSizeInBlocks = 4#int(sys.argv[6])


    UDPServerSocket.bind((localIP, localPort))
    

     
     # Have to check if there's a file with such name 
    if not os.path.exists(fileName) :
     print(f"nack1{nack1} - File name provided doesn't exist")
     sys.exit() #Forcely exit program


    with open(fileName, 'rb') as file:
     data = file.read()    
     # Create an array in each element has maximum 1024b of info
     packet_payload = [data[i:i+1024] for i in range(0, len(data), 1024)]

     packetSize = len(packet_payload)



    while(True):
      
          #Gonna send windowSizeInBlocks at a time
          bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)#Recieves the dumped request from the client
          #Ack or Nack
          message = bytesAddressPair[0]  
          client_address = bytesAddressPair[1]

          status = pickle.loads(message) #Loads the dumped request from the client

          

          if status != ack:
              dealWithLostChilds(status)
          
          sendPackets = {
               "key": [i for i in range(current ,current + windowSizeInBlocks)], # store the numbers visited
               "packet": slidingWindow["packet"][current : current + windowSizeInBlocks] # store the data visited
          }
          current += windowSizeInBlocks
          
          
          resp = pickle.dumps(sendPackets)

          serverReply(resp)
     

#void 
def dealWithLostChilds(lostChild):
     global current
     current = lostChild
 


def serverReply(resp):
  rand = random.randint(0,10)
  if rand >=3:
      UDPServerSocket.sendto(resp, client_address)
  

main()


