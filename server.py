import socket
from _thread import *

server = '192.168.1.9'  # local
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Server booted up. Waiting for connection...")


def threaded_connection(conn):
    conn.send(str.encode("Connected"))
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                print("Disconnected. No data received from Client.")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply))
        except socket.error as e:
            print(str(e))
            break
    print("Lost Connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Server has accepted connection from: ", addr)

    start_new_thread(threaded_connection, (conn,))
