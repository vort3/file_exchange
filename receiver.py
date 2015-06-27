import socket


KB = 1024
MB = 1024 * KB
filebuffer = 4 * KB

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

def getsize(path):
    with file(path) as f:
        f.seek(0, 2)
        return f.tell()


listener = socket.socket()
listener.bind(('', 25565))
listener.listen(5)
sock, addr = listener.accept()
print "accepted", addr

expected = int(pull_and_push())
print "Expected size is", expected

filename = "D:\\test.jpg"
with open(filename, 'wb+') as f:
    s = 0
    c = 0
    trash = None
    while s != expected:
        c += 1
        obj = sock.recv(filebuffer)
        if not obj:
            continue
        f.write(obj)
        s += len(obj)
        percents = (s*100)/(expected)
        if c % 100 == 0:
            print "Current:", s, "\t\tExpected:", 
            print expected, '\t', percents, '%'


push_and_pull(getsize(filename))
print "File recieved and file size checked"

sock.close()
