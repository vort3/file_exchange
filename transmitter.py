import socket
import os
import Tkinter as tk
import tkFileDialog


KB = 1024
MB = 1024 * KB

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

sock = socket.socket()
sock.connect_ex((host, 25565))

print "connected to", host

root = tk.Tk()
root.withdraw()
file = tkFileDialog.askopenfilename()
size = os.path.getsize(file)

push_and_pull(size)
print 'size confirmed', size

with open(file, 'rb', 4*MB) as obj:
    s = 0
    c = 0
    for part in obj.readlines():
        c += 1
        sock.send(part)
        s += part.__sizeof__()
        percents = (s*100)/(size)
        if c % 500 == 0:
            print "Current:", s, "\t\tExpected:", 
            print size, '\t', percents, '%'
    sock.send("END_OF_FILE"*16)

print "sent"

pull_and_push(size)
print "file size confirmed"

sock.close()
