import socket
import Tkinter as tk
import tkFileDialog


KB = 1024
MB = 1024 * KB
filebuffer = 4 * KB

# host = '78.132.190.8'
host = 'vort3.ddns.net'

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


sock = socket.socket()
sock.connect_ex((host, 25565))
print "connected to", host

root = tk.Tk()
root.withdraw()
filename = tkFileDialog.askopenfilename()

size = getsize(filename)
push_and_pull(size)
print 'size confirmed', size

with open(filename, 'rb', filebuffer) as obj:
    c = 0
    part = obj.read(filebuffer)
    s = len(part)
    while part != "":
        c += 1
        sock.send(part)
        percents = (s*100)/(size)
        if c % 100 == 0:
            print "Current:", s, "\t\tExpected:", 
            print size, '\t', percents, '%'
        part = obj.read(filebuffer)
        s += len(part)


print "sent"
pull_and_push(size)
print "file size confirmed"

sock.close()
