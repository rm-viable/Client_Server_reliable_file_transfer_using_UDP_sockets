import socket
import sys
import os
import time
try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()
serverName = 'localhost'
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msgg1 = 'The connection is established'
clientSocket.sendto(msgg1.encode(),(serverName, serverPort))

def my_client_main():
    myMessage = input("Please enter a command: \n$ get [file_name]\n$ put [file_name]\n$ rename [old_file_name] [new_file_name]\n$ list \n$ exit\n ")
    clientSocket.sendto(myMessage.encode(),(serverName, serverPort))
    myCommand=myMessage.split()
    eff1 = myCommand[0]
    try:
        if eff1 == 'put': #code for the put command
            try:
                smclient, clientAddress12 = clientSocket.recvfrom(4096)
                myMessgn = smclient.decode('utf8')
                print(myMessgn)
                print("Will start sending now if the file exists in the client directory...")
            
                if myMessgn == "Establishing put...": #myMessgn from server
                    if os.path.isfile(myCommand[1]):
            
                        fp = 0
                        flsize = os.stat(myCommand[1])
                        pck = flsize.st_size  
                        print("File size in bytes: " + str(pck))
                        sp = int(pck / 4096)
                        sp = sp + 1
                        print("Number of packets to be sent: " + str(sp))
                        spp = str(sp)
                        myspp = spp.encode('utf8')
                        clientSocket.sendto(myspp, clientAddress12)
                        myspc = int(sp)
                        filM = open(myCommand[1], "rb")
            
                        while myspc != 0:
            
                            filT = filM.read(4096)
                            clientSocket.sendto(filT, clientAddress12)
                            time.sleep(.002)
                            fp += 1
                            myspc -= 1
                            print("Sending Packet number:" + str(fp))
            
                        filM.close()
            
                        print("Sent to client")
                    
                    else:
                        clientSocket.sendto('0'.encode(), clientAddress12)
                        print("File does not exist in client directory.")
                        my_client_main()
                    
            except ConnectionResetError as msgp1:
                print('The server is stopped '+str(msgp1))
                sys.exit()
    
                
    
        elif eff1 == 'get':
            try:
                msgcc, clientAddress1 = clientSocket.recvfrom(51200)
               
                if msgcc.decode() == '0':
                    print('Sorry! The file does not exist in server directory.')
                    my_client_main()
                else:
                    msgcs = msgcc.decode('utf8')
                    print(msgcs)
                    
                    largefile = open(myCommand[1], "wb")
                    d = 0
                    try:
                        my_n, countaddress = clientSocket.recvfrom(4096)
            
                    except ConnectionResetError as msgp2:
                        print('The server is stopped '+str(msgp2))
                        sys.exit()
            
                    except:
                        print("Error occurred!")
                        sys.exit()
            
                    my_np = my_n.decode('utf8')
                    mynpp = int(my_np)
                    print("Client will start receiving now if server has the requested file...")
                    while mynpp != 0:
                        clfile, clientAddrn = clientSocket.recvfrom(4096)
                        dataS = largefile.write(clfile)
                        d += 1
                        print("Received packet number:" + str(d))
                        mynpp = mynpp - 1
            
                    largefile.close()
                    print("File received!")

            except ConnectionResetError as msgpp1:
                print('The server is stopped '+str(msgpp1))
                sys.exit()

            except:
                print("error occurred!")
                sys.exit()
                    
    
        elif eff1 == 'rename':
            try:
                rename = 'mv'
                clientSocket.sendto(rename.encode(),(serverName, serverPort))
                clientSocket.sendto(myCommand[1].encode(),(serverName, serverPort))
                clientSocket.sendto(myCommand[2].encode(),(serverName, serverPort))
                mmgg1,serverAddress = clientSocket.recvfrom(2048)
                print(mmgg1.decode())
                my_client_main()
            except ConnectionResetError as msgp3:
                print('The server is stopped '+str(msgp3))
                sys.exit()
        
        elif eff1 == 'list':
            try:
                modifiedMessage1,serverAddress = clientSocket.recvfrom(2048)
                print (modifiedMessage1.decode())
                my_client_main()
            except ConnectionResetError as msgp:
                print('The server is stopped '+str(msgp))
                sys.exit()
                
        elif eff1 == 'exit':
            try:
                pass
            except ConnectionResetError as msgpnn:
                print('The server is stopped '+str(msgpnn))
                sys.exit()

        else:
            c1 = ''
            for items in myCommand:
                c1 += items
            print("You have entered: "+c1)
            print('\n')
            print("Invalid input format.\n Please try again.")
            my_client_main()
            
    except ConnectionResetError as msgpp3:
        print('The server is stopped '+str(msgpp3))
        sys.exit()

while True:
    my_client_main()
    
        
