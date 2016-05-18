import socket
import wavGen
import os

TCP_IP = '127.0.0.1'
TCP_PORT = 44444
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        mystring = data.split(",")
    if mystring[0] == "get_file":
        filename = mystring[1]+'.wav'
        wavGen.wavGen(filename,"rand")
        s.send("send_file,name,size," +filename+ "," + str(os.stat(filename).st_size))
        f = open(filename,'rb')
        print 'Sending...'
        l = f.read(1024)
        while (l):
            print 'Sending...'
            s.send(l)
            l = f.read(1024)
        f.close()
        print "Done Sending"
        print s.recv(1024)
    #for s in mystring:
    #    print s
    #print "mystring[0]:", mystring[0]
    #data = "server echo : " + data
    conn.send("ok")  # echo
conn.close()
