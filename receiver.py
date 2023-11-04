#Author: Guilherme Antunes 62621
#Author: Rodrigo Loução 63627

import socket
import pickle
import sys
import select
import os
import time 


UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  #Create UDP client socket


nack1 = 1 # File does not exist
nack2 = 2 # Invalid offset
ack = 0 # All good to go

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
   
    startTime = time.time()

    hostServer = "127.0.0.1" #sys.argv[1]

    serverPort = 12345 #int(sys.argv[2])

    fileName = "testede20mb.txt" #sys.argv[3]  
    
    chunkSize = 4096 #int(sys.argv[4])
    
    serverAddressPort = ((hostServer, serverPort))

    fileToWrite = getFileName()

    with open(fileToWrite, 'wb') as file:
        chunkOffset = 0

        while(True):
            elapsed_time = time.time() - startTime
            print(f'It is taking {elapsed_time:.2f} seconds.')


            request = pickle.dumps((fileName, chunkOffset, chunkSize)) 
            UDPClientSocket.sendto(request, serverAddressPort)


            if waitForReply():

                data = UDPClientSocket.recvfrom(chunkSize) #Tirei o load daqui para testar
                response = pickle.loads(data[0])

                bytesTransferred = response
                serverAddressPort = data[1]

                errcode = bytesTransferred[0]

                if errcode == nack1:
                    print("File does not exist")
                elif errcode == nack2:
                    print("Invalid offset")
                else:      
                    file.write(bytesTransferred[2])
                    chunkOffset += bytesTransferred[1]
                    if bytesTransferred[1] + 25 < chunkSize:
                        break


            progress = (os.path.getsize(fileToWrite) / os.path.getsize(fileName)) * 100
            print(f"Download progress ==> {progress:.2f}%") 

    

    file.close()


    print(f"Rate KBytes per second: {(os.path.getsize(fileToWrite)  / elapsed_time / 1024 ):.2f} kbps")



def waitForReply():
    rx, _, _ = select.select([UDPClientSocket], [], [], 1)
    if not rx:
        return False
    else:
        return True


main()