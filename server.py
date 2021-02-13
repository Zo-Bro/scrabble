import socket
from _thread import *
import rules
from player import Player
import pickle
class Server:

    def __init__(self, port=5555, max_players=4):
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        self.server = socket.gethostbyname(host_name)
        self.game_model = rules.Scrabble()
        try:
            self.socket.bind((self.server, port))
        except socket.error as e:
            print(str(e))


    def threaded_connection(self, conn, current_player):
        # one of these continuously runs for each new connection. It runs forever.
        conn.send(str.encode(str(current_player))) # when you first connect to the server, you recieve your player number
        name = conn.recv(2048).decode()
        player = self.game_model.players[str(current_player)]
        player.set_name(name)
        needs_tiles = len(player.Get_Inventory()) < 7
        while needs_tiles:
            print("Giving a tile to the player")
            needs_tiles = player.Add_To_Inventory(self.game_model.Get_New_Letter())
        self.game_model.players[str(current_player)] = player
        reply = ''
        while True:
            # when player is inactive, just send the game model.
            in_data = conn.recv(8192) # client sends a DataPacket() with a command, such as "get", "commit turn"
            in_data = pickle.loads(in_data)
            if not in_data:
                break
            else:
                if in_data.cmd == 'commit':
                    if str(current_player) == self.game_model.active_player:

                        result = self.game_model.Process_Turn(in_data) # apply the turn using the data received from
                        #ToDo: Handle when a player makes an illegal play (skip their turn and dont place their tiles on teh board)
                        if result == True:
                           # self.game_model.active_player = str(int(self.game_model.active_player))
                            reply = self.game_model
                        else:
                            reply = self.game_model

                elif in_data.cmd == 'get':
                    reply = self.game_model #
            conn.send(pickle.dumps(reply))
        pass

    def boot_up(self, max_players):
        self.socket.listen(5)
        print("Server booted up. Waiting for connection...")
        self.game_model.New_Game(max_players)
        idCount = 0
        while True:
            conn, addr = self.socket.accept() # the code never goes past here until a new connection is established
            print("Server has accepted connection from: ", addr)
            idCount += 1
            self.game_model.players[str(idCount)] = Player(str(idCount))
            start_new_thread(self.threaded_connection, (conn, idCount,))

if __name__ == '__main__':
    game_model = rules.Scrabble()
    ip_address = '192.168.1.11'
    Server(ip_address, 555, 4, game_model)