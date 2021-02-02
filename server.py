import socket
from _thread import *

server = '192.168.1.9'  # local
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(5)
print("Server booted up. Waiting for connection...")

connected = set()
games = {}
idCount = 0

def threaded_connection(conn):
    pass

while True:
    conn, addr = s.accept()
    print("Server has accepted connection from: ", addr)

    start_new_thread(threaded_connection, (conn,))
