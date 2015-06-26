import socket


listener = socket.socket()
listener.bind(('', 25565))
listener.listen(5)
sock, addr = listener.accept()
print "accepted", addr

with open("D:\\test.jpg", 'wb+') as f:
    while True:      
        obj = sock.recv(4096)
        if not obj:
            continue
        if obj == "END_OF_FILE"*16:
            break
        f.write(obj) 
   

sock.send('Received')