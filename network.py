import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.1.9'  # local
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.Connect()

    def Get_Player(self):
        return self.pos

    def Connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() # the very first thing we get is the actual player number.
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data)) # send data
            in_data = self.client.recv(2048)
            return pickle.loads(in_data)
        except socket.error as e:
            print(str(e))

