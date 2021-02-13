import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def boot(self, server, port=5555, name='<PLACE_HOLDER>'):
        self.server = server # local
        self.port = port
        self.addr = (self.server, self.port)
        self.player = self.Connect(name)

    def Get_Player(self):
        return self.player

    def Connect(self, name):
        try:
            self.client.connect(self.addr)
            in_data = self.client.recv(2048)
            print("Network recv connection confirmation. ")
            print("Data Recieved: " + in_data.decode())
            self.client.send(str.encode(name)) # send the name the player picked so it is assigned to the player ID
            return  in_data.decode() # the very first thing we get is the actual player number.
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data)) # send data
            in_data = self.client.recv(8192)
            return pickle.loads(in_data)
        except socket.error as e:
            print(str(e))

