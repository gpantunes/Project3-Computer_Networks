#Author Guilherme Antunes nº 62621
#Author Rodrigo Loução nº

import socket
import pickle
import os
import random
import sys
import select

windowBlockSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 


DONE = 3 # File sent sucessufully
nack1 = 1 # File does not exist
nack2 = 2 # Lost packet
ack = 0 # All good to go

client_address = 0



senderIP = "127.0.0.1"#int(sys.argv[1])

senderPort = 20001#int(sys.argv[2])

receiverIP = "127.0.0.1"#int(sys.argv[3])

receiverPort = 54321#int(sys.argv[4])

fileName = "pila.txt" #sys.argv[5]

windowSizeInBlocks = 4#int(sys.argv[6])


UDPServerSocket.bind((senderIP, senderPort))



def main():
    print("UDP server up and listening")

    UDPServerSocket.sendto(pickle.dumps((windowSizeInBlocks, windowBlockSize)), (receiverIP, receiverPort))
     
     # Have to check if there's a file with such name 
    if not os.path.exists(fileName) :
     print(f"nack1{nack1} - File name provided doesn't exist")
     sys.exit() #Forcely exit program



    with open(fileName, 'rb') as file:
          data = file.read()    
    
    # Create an array in each element has maximum 1024b of info
    packet_payload = [data[i:i+1024] for i in range(0, len(data), 1024)]

    # Dictionary Sliding window
    slidingWindow ={
          "key": 1,
          "packets": packet_payload,
          "nextPack" : 1
     }



     #While there's still packets to read
    while slidingWindow["key"] <= len(packet_payload):

          #Iterates from slidingWindow['nextPack']
          for current in range(slidingWindow["nextPack"], min(slidingWindow["nextPack"] + min(windowSizeInBlocks, 10), len(packet_payload) + 1)):
          #Gonna send windowSizeInBlocks at a time
               data_packet = pickle.dumps((0, current, packet_payload[current - 1]))
               senderReply(data_packet, (receiverIP, receiverPort))

          if waitForReply(2):
               resp, _ = UDPServerSocket.recvfrom(4096)
               status, ack_num = pickle.loads(resp)

               if status == nack2:
                    print(f"Lost packet{ack_num}")
                    dealWithLostChilds(slidingWindow,ack_num)
                    continue


               slidingWindow["key"] = ack_num + 1
         
          slidingWindow["nextPack"] = slidingWindow["key"]

     #Send DONE message 
    data_packet = pickle.dumps((3, 0, 0))
    UDPServerSocket.sendto(data_packet, (receiverIP, receiverPort)) 
    print("File sent sucessfully")     


def dealWithLostChilds(slidingWindow,lostChild):
    slidingWindow['key'] = lostChild
    return 0
 


def senderReply(resp, address):
  rand = random.randint(0,10)
  if rand >=1:
     UDPServerSocket.sendto(resp, address)   
  


def waitForReply(timeout):
    rx, _, _ = select.select([UDPServerSocket], [], [], timeout)
    if not rx:
        return False
    else:
        return True



main()