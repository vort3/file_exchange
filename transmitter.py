import socket


host = '78.132.240.95'
# host = 'vort3.ddns.net'

sock = socket.socket()
sock.connect_ex((host, 25565))

print "connected to", host

with open("D:\\test.jpg", 'rb', 4096) as obj:
    for part in obj.readlines():
        sock.send(part)

sock.send("END_OF_FILE"*16)

print "sent"

while True:
    reply = sock.recv(4096)
    if not reply:
        continue
    break

print reply
sock.close()