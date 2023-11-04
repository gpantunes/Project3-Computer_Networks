import socket
import pickle
import sys
import select
import os

transferCompleted = False
serverAddressPort   = ("127.0.0.1", 20001)
chunkSize = 4096
chunkOffset = 0

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  #Create UDP client socket


nack1 = 1 # File does not exist
nack2 = 2 # Lost packet
ack = 0 # All good to go

#Dictionary Sliding Window
current = 0
packet_paylod = []

slidingWindow ={
    "key": current,
    "packet": packet_paylod[current]
}




def getFileName():
    i = 0
    file_name = ''
    while True:
        file_name = f'broNoWork{i}.txt'
        if not os.path.exists(file_name):
            break
        i += 1
    return file_name


def main():
    #global serverPort
    global serverAddressPort


    receiverIP = int(sys.argv[1])

    receiverPort = int(sys.argv[2])

    fileName = int(sys.argv[3])

    #serverAddressPort = (("127.0.0.1", serverPort))

    if not os.path.exists(fileName):
        print(f"nack1{nack1} - File name provided doesn't exist")
        sys.exit() # Forcely exit


    with open(fileName, 'wb') as file:

        while(True):
           

            if waitForReply():

                data = UDPClientSocket.recvfrom(chunkSize) #Tirei o load daqui para testar
                response = pickle.loads(data[0])

                receivedPackets = response["key"]
                
                status = checkIfLostData(response)

                #Todo tranquilaço
                if status == ack:        
                    slidingWindow['packet'] += receivedPackets['packets']   
                    slidingWindow['key'] += receivedPackets['key']
                    
                    for i in range(receivedPackets['packets']):
                        file.write(receivedPackets['packets'][i])

                    dumpedAck = pickle.dumps(status)
                    UDPClientSocket.send(dumpedAck)
                else:   
                    dealWithLostChilds(status)


    
# Check if the keys received are in a sequence,
# If not, means there is data that was lost
# @return, ack if no data lost
# @return, keyElement[i], where it repesents number of the packet lost
def checkIfLostData(response):
    keyElements = response['key']
    count = keyElements[0]

    for i in range(keyElements):
        if count != keyElements[i]:
            return keyElements[i]

    return ack


def dealWithLostChilds(lostChild):
    dumpedLostChild = pickle.dumps(lostChild)
    UDPClientSocket.send(dumpedLostChild)
    return 0

        

def waitForReply():
    rx, _, _ = select.select([UDPClientSocket], [], [], 1)
    print(rx)
    if not rx:
        return False
    else:
        return True


main()