import socket
import pickle
import sys
import select
import os

transferCompleted = False
serverAddressPort   = ("127.0.0.1", 20001)
chunkSize = 4096
chunkOffset = 0
fileName = "pila.txt"

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  #Create UDP client socket


nack1 = 1 # File does not exist
nack2 = 2 # Invalid offset
ack = 0 # All good to go

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
    global chunkSize

    #serverPort = int(sys.argv[1])

    #fileName = sys.argv[2]
    #chunkSize = int(sys.argv[3])
    
    #serverAddressPort = (("127.0.0.1", serverPort))

    with open(getFileName(), 'wb') as file:
        chunkOffset = 0

        while(True):
            request = pickle.dumps((fileName, chunkOffset, chunkSize)) 
            UDPClientSocket.sendto(request, serverAddressPort)

            print("inicio")
            if waitForReply():

                data = UDPClientSocket.recvfrom(chunkSize) #Tirei o load daqui para testar
                response = pickle.loads(data[0])

                bytesTransferred = response
                serverAddressPort = data[1];

                errcode = bytesTransferred[0]
                print(errcode)

                if errcode == nack1:
                    print("File does not exist")
                elif errcode == nack2:
                    print("Invalid offset")
                else:      
                    file.write(bytesTransferred[2])
                    chunkOffset += bytesTransferred[1]
                    print(bytesTransferred[1] + 25)
                    if bytesTransferred[1] + 25 < chunkSize:
                        break


            print("ciclo")
    

    file.close()


        

def waitForReply():
    print("rx")
    rx, _, _ = select.select([UDPClientSocket], [], [], 1)
    print(rx)
    if not rx:
        print("false")
        return False
    else:
        print("true")
        return True


main()