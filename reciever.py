import socket
import pickle
import sys
import select
import os
import random

transferCompleted = False
serverAddressPort = ("127.0.0.1", 20001)

windowBlockSize = 0
windowSizeInBlocks = 0



UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  #Create UDP client socket


DONE = 3 # File received successufully
nack1 = 1 # File does not exist
nack2 = 2 # Lost packet
ack = 0 # All good to go

#Dictionary Sliding Window
current = 0
packet_paylod = []
status = ack


slidingWindow ={
    "key": current,
    "packet": packet_paylod
}




def getFileName():
    i = 0
    file_name = ''
    while True:
        file_name = f'untitled{i}.txt'
        if not os.path.exists(file_name):
            break
        i += 1
    return file_name


def main():
    global serverAddressPort


    receiverIP = "127.0.0.1"#int(sys.argv[1])

    receiverPort = 54321#int(sys.argv[2])

    fileName = getFileName() #int(sys.argv[3])

    UDPClientSocket.bind((receiverIP, receiverPort))

    windowSpecs, serverAddressPort = UDPClientSocket.recvfrom(2048)
    windowBlockSize, windowSizeInBlocks = pickle.loads(windowSpecs)

    if os.path.exists(fileName):
        print(f"nack{nack1} - File name provided already exist")
        sys.exit() # Forcely exit


    with open(fileName, 'wb') as file:

        while(True):

        
            data, serverAddressPort = UDPClientSocket.recvfrom(windowSizeInBlocks * windowBlockSize) #Tirei o load daqui para testar
            status, npack, data = pickle.loads(data)

            if data == 3:
                break
            if status == ack:        
                if npack == slidingWindow['key']:
                    file.write(data)
                    slidingWindow['key'] += 1

                else: #Go-Back-N strategy
                    print("Lost packet")
                    dealWithACK(nack2, slidingWindow['key']-1)
                    

                dealWithACK(ack, slidingWindow['key']-1)
                
            
            elif status == DONE:
                print("File received sucessully")
                break
             
            


def dealWithACK(ackVal, lostChild):
    rand = random.randint(0,10)
    if rand >=1:
        print("mandow ack")
        dumpedLostChild = pickle.dumps((ackVal, lostChild))
        UDPClientSocket.sendto(dumpedLostChild, serverAddressPort)
    else: print("perdeu ack")
    return 0

    

main()