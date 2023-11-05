import socket
import pickle
import sys
import select
import os

transferCompleted = False
serverAddressPort   = ("172.17.0.2", 20001)
chunkSize = 4096
chunkOffset = 0




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


    receiverIP = (sys.argv[1])

    receiverPort = int(sys.argv[2])

    fileName = (sys.argv[3])

    UDPClientSocket.bind((receiverIP, receiverPort))

    if os.path.exists(fileName):
        print(f"nack1{nack1} - File name provided already exist")
        sys.exit() # Forcely exit


    with open(fileName, 'wb') as file:

        while(True):

        
            data, senderAddress = UDPClientSocket.recvfrom(chunkSize) #Tirei o load daqui para testar
            status, npack, data = pickle.loads(data)

            if data == 3:
                break
            #Todo tranquilaço
            if status == ack:        
                if npack == slidingWindow['key']:
                    file.write(data)
                    slidingWindow['key'] += 1
                else: #Go-Back-N strategy
                    print("Lost packet")
                    dumpedAck = pickle.dumps((nack2,slidingWindow['key']-1))
                    UDPClientSocket.sendto(dumpedAck, senderAddress)

                dumpedAck = pickle.dumps((1,slidingWindow['key']-1))
                UDPClientSocket.sendto(dumpedAck, senderAddress)
            
            elif status == DONE:
                print("File received sucessully")
                break
             
            


def dealWithLostChilds(lostChild):
    dumpedLostChild = pickle.dumps(lostChild)
    UDPClientSocket.sendto(dumpedLostChild, serverAddressPort)
    return 0

    

main()