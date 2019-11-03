import socket
import sys
import os
import time
serverPort = int(sys.argv[1])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')
inc_message1, clientAddress = serverSocket.recvfrom(2048)
print(inc_message1.decode())


def get(l,d):
    try:    
        if os.path.isfile(d):
            msgNY = "File check OK "
            msgEnCY = msgNY.encode('utf-8')
            serverSocket.sendto(msgEnCY, clientAddress)
    
            i = 0
            pack = os.stat(d)
            packSize = pack.st_size  # Calculating number of packets
            print("File size in bytes:" + str(packSize))
            ords = int(packSize / 4096)
            ords = ords + 1
            sizes = str(ords)
            size_f = sizes.encode('utf8')
            serverSocket.sendto(size_f, clientAddress)
    
            fun = int(ords)
            bitR_S = open(d, "rb")
            while fun != 0:
                bitR = bitR_S.read(4096)
                serverSocket.sendto(bitR, clientAddress)
                time.sleep(.002)
                i += 1
                fun -= 1
                print("Sending Packet number:" + str(i))
            bitR_S.close()
            print("File sent from server")
            my_main()

    
        else:
            print("File doesn't exist in server directory!")
            serverSocket.sendto('0'.encode(), clientAddress)
            my_main()

    except ConnectionResetError as msgp:
        print('The server is stopped'+str(msgp))
        sys.exit()


def put(a,b):
    print("Handshake for put")
    mymsg = "Establishing put..."
    msgtocl = mymsg.encode('utf-8')
    serverSocket.sendto(msgtocl, clientAddress)

    print("Put file from client in progress...")
    if a == "put":
        try:
            cg, clntaddress = serverSocket.recvfrom(4096)  # number of packet
            if cg.decode() == '0':
                print('File is not present at the client directory!')
                my_main()

            else:
                mylargefile = open(b, "wb")
                mmt = 0
                print("Receiving packets will start now if file exists.")
                cr = cg.decode('utf8')
                cr = int(cr)
                while cr != 0:
                    smserver, serverAddress11 = serverSocket.recvfrom(4096)
                    dataS = mylargefile.write(smserver)
                    mmt += 1
                    cr = cr - 1
                    print("Received packet number:" + str(mmt))
        

                mylargefile.close()
                print("File received completely!")
                my_main()
                
        except ConnectionResetError:
            print("Exiting")
            sys.exit()
        except:
            print("error occurred!")
            sys.exit()
        
def list_files():
    try:
        os.system("ls -lrt | awk '{print $8,$9}' > new1.txt")
        fileHandle1n = open('new1.txt','r')
        msg_nw = fileHandle1n.read()
        fileHandle1n.close()
        finalMsg11 = msg_nw.encode()
        serverSocket.sendto(finalMsg11,clientAddress)
        my_main()
    except ConnectionResetError as msgp:
        print('The server is stopped'+str(msgp))
        sys.exit()

	
def rename():
    while True:
        command, clientAddress = serverSocket.recvfrom(2048)
        oldFile, clientAddress = serverSocket.recvfrom(2048)
        newFile, clientAddress = serverSocket.recvfrom(2048)
        nmm=' '
        mycmd=(str(command.decode())+nmm+str(oldFile.decode())+nmm+str(newFile.decode()))
        os.system(mycmd)
        mmgg = 'The rename is successful.'
        serverSocket.sendto(mmgg.encode(),clientAddress)
        my_main()

def serverexit():
    print("Exit triggered by client. Closing server!")
    serverSocket.close()
    sys.exit()


def my_main():
    print ('The server is ready to receive \n')
    try:
        incoming_message, clientAddr = serverSocket.recvfrom(4096)
    except ConnectionResetError:
        print("Exiting")
        sys.exit()
    effs = incoming_message.decode('utf8')
    effsn = effs.split()
    if effsn[0] == 'get':
        get(effsn[0],effsn[1])
    elif effsn[0] == 'put':
        put(effsn[0],effsn[1])
    elif effsn[0] == 'list':
        list_files()
    elif effsn[0] == 'rename':
        rename()
    elif effsn[0] == 'exit':
        serverexit()
while True:
    my_main()