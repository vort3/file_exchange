import socket
import os


KB = 1024
MB = 1024 * KB

def push_and_pull(msg):
    msg = str(msg)
    reply = None
    while reply != msg*4:
        sock.send(msg)
        reply = sock.recv(1*KB)
        if not reply:
            continue
        break

def pull_and_push(e=None):
    input = None
    while input == None:
        input = sock.recv(1*KB)
        if not input:
            continue
    if e != None:
        sock.send(str(e)*4)
        return
    sock.send(input*4)
    return input


listener = socket.socket()
listener.bind(('', 25565))
listener.listen(5)
sock, addr = listener.accept()
print "accepted", addr

expected = int(pull_and_push())
print "Expected size is", expected

with open("D:\\test.jpg", 'wb+') as f:
    s = 0
    c = 0
    trash = None
    while s <= expected+512*KB:
        c += 1
        obj = sock.recv(4*MB)
        if not obj:
            continue
        if "END_OF_FILE" in obj:
            obj, trash = obj.split('END_OF_FILE', 1)
        f.write(obj)
        s += obj.__sizeof__()
        percents = (s*100)/(expected)
        if c % 100 == 0:
            print "Current:", s, "\t\tExpected:", 
            print expected, '\t', percents, '%'
        if trash:
            break


s = os.path.getsize("D:\\test.jpg")
push_and_pull(s)
print "File recieved and file size checked"

sock.close()
