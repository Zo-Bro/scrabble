import random
from itertools import combinations
import player as player_
def invert_coord_y(coord):
    x = coord[0]
    y = coord[1]
    y = 14 - y
    return x, y

class DataPacket():
    def __init__(self, cmd='get', mode=1, letters_played=[], coords_played=[], player_id=None):
        self.cmd = cmd
        self.mode = mode # 1 == set letters, # 0 == exchange letters
        self.letters_played = letters_played
        self.coords_played = coords_played
        self.player_id = player_id

class Scrabble():
    def __init__(self):
        self.seed = random.seed()
        self.letter_distribution = {'a':9,
                                    'b':2,
                                    'c':2,
                                    'd':4,
                                    'e':12,
                                    'f':2,
                                    'g':3,
                                    'h':2,
                                    'i':9,
                                    'j':1,
                                    'k':1,
                                    'l':4,
                                    'm':2,
                                    'n':6,
                                    'o':8,
                                    'p':2,
                                    'q':1,
                                    'r':6,
                                    's':4,
                                    't':6,
                                    'u':4,
                                    'v':2,
                                    'w':2,
                                    'x':1,
                                    'y':2,
                                    'z':1
                                    }
        self.letter_value = {       'a':1,
                                    'b':3,
                                    'c':3,
                                    'd':2,
                                    'e':1,
                                    'f':4,
                                    'g':2,
                                    'h':4,
                                    'i':1,
                                    'j':8,
                                    'k':5,
                                    'l':1,
                                    'm':3,
                                    'n':1,
                                    'o':1,
                                    'p':3,
                                    'q':10,
                                    'r':1,
                                    's':1,
                                    't':1,
                                    'u':3,
                                    'v':4,
                                    'w':4,
                                    'x':8,
                                    'y':4,
                                    'z':10
                                    }
        self.special_tiles = {
            # center tile
            (7,7):(1,'l'),
            # triple word scores
            (0,0):(3,'w'),
            (0,7):(3,'w'),
            (0,14):(3,'w'),
            (7, 14):(3,'w'),
            (14,0):(3,'w'),
            (14, 7):(3,'w'),
            (14,14):(3,'w'),
            (7,0):(3,'w'),

            # double word scores
            (1,1):(2, 'w'),
            (2,2):(2, 'w'),
            (3,3):(2, 'w'),
            (4,4):(2, 'w'),
            (13,1):(2, 'w'),
            (12,2):(2, 'w'),
            (11,3):(2, 'w'),
            (10,4):(2, 'w'),
            (1,13):(2, 'w'),
            (2,12):(2, 'w'),
            (3,11):(2, 'w'),
            (4,10):(2, 'w'),
            (10,10):(2, 'w'),
            (11,11):(2, 'w'),
            (12,12):(2, 'w'),
            (13,13):(2, 'w'),

            # triple letter score
            (5,1):(3,'l'),
            (9,1):(3,'l'),
            (5,13):(3,'l'),
            (9,13):(3,'l'),
            (1,5):(3,'l'),
            (5,5):(3,'l'),
            (9,5):(3,'l'),
            (13,5):(3,'l'),
            (1,9):(3,'l'),
            (5,9):(3,'l'),
            (9,9):(3,'l'),
            (13,9):(3,'l'),

            # double letter score
            (3,0):(2,'l'),
            (11,0):(2,'l'),
            (6,2):(2,'l'),
            (8,2):(2,'l'),
            (0,3):(2,'l'),
            (7,3):(2,'l'),
            (14,3):(2,'l'),
            (2,6):(2,'l'),
            (6,6):(2,'l'),
            (8,6):(2,'l'),
            (12,6):(2,'l'),
            (3,7):(2,'l'),
            (11,7):(2,'l'),
            (2,8):(2,'l'),
            (6,8):(2,'l'),
            (8,8):(2,'l'),
            (12,8):(2,'l'),
            (0, 11):(2,'l'),
            (7,11):(2,'l'),
            (14,11):(2,'l'),
            (6,12):(2,'l'),
            (8,12):(2,'l'),
            (3,14):(2,'l'),
            (11,14):(2,'l'),
        }

        self.word_Q = []
        self.score_board = {}
        self.__playboard = []
        self.__temp_playboard = []
        self.players = {} #key == player.ID: value == Player() object

        # game flow vars
        self.current_played_letters = []
        self.current_played_coords = []
        self.active_player = '1' # the id of the active player
        self.total_players = 2
        self.game_end = False
        self.game_start = False

    def New_Game(self, max_players):
        self.total_players = max_players
        self.active_player = '1'
        self.last_active_player = '0'
        self.word_Q = self.Build_Word_Q()
        self.Construct_Empty_Playboard()
        # TODO: UI function for selecting number of players

    def Generate_Players(self, num_players=2):
        for person in range(0, num_players):
            # TODO: UI function get the name for the player
            name_entry = 'Player_' + str(person)
            #player = Player[person]
            #self.players.append(player)
            pass

        # distribute beginning tiles for players
        for Player in self.players:
            need_tiles = True
            while need_tiles:
                need_tiles = Player.Add_To_Inventory(self.Get_New_Letter())

    def Reset_Temp_Playboard(self):
        self.__temp_playboard = []
        for x in range(0, 15):
            row = ['' for y in range(0, 15)]
            self.__temp_playboard.append(row)
        for y in range(0, 15):
            for x in range(0,15):
                self.__temp_playboard[y].pop(x)
                self.__temp_playboard[y].insert(x, self.Get_letter_from_playboard((x,y)))

    def Construct_Empty_Playboard(self):
        self.__playboard = []
        for x in range(0, 15):
            row = ['' for y in range(0, 15)]
            self.__playboard.append(row)

    def Get_Playboard(self):
        return self.__playboard

    def Set_Letter(self, letter='', coord = (), temp=False):
        '''
        Playboard accessed row (y) 1st, column (x) 2nd
        :param letter:
        :param coord:
        :return:
        '''
        if temp == True:
            x = coord[0]
            y = coord[1]
            self.__temp_playboard[y].pop(x)
            self.__temp_playboard[y].insert(x, letter)
        else:
            x = coord[0]
            y = coord[1]
            self.__playboard[y].pop(x)
            self.__playboard[y].insert(x, letter)

    def Build_Word_Q(self):
        positions = []

        high_roll = 0
        for letter, number in self.letter_distribution.items():
            for i in range(0, number):
                roll = random.randrange(0, 500)
                if roll >= high_roll:
                    positions.append([letter, roll])
                    high_roll = roll
                else:
                    for j in range(0, len(positions)):
                        if roll <= positions[j][1]:
                            positions.insert(j, [letter, roll])
                            break
        positions = [item[0] for item in positions]
        return positions

    def Setup_Board(self, size = 15):
        '''
        A standard scrabble board is 15x15 units large.

        :param size:
        :return:
        '''
        size = size

        return

    def Validate_Turn(self, data_packet):
        '''calculates the turn, and then sends to the server'''
        #
    def Order_Letters(self, letters_played, coords_played):
        new_letters = []
        new_coords = []
        letter_coords = [(letters_played[i], coords_played[i]) for i in range(0, len(letters_played))]

        all_x = [coords_played[i][0] for i in range(0, len(coords_played))]
        all_y = [coords_played[i][1] for i in range(0, len(coords_played))]
        all_x = len(set(all_x)) == 1
        if all_x:
            sorted_letters_coords = sorted(letter_coords, key=lambda x: x[1][1])
        else:
            sorted_letters_coords = sorted(letter_coords, key=lambda x: x[1][0])

        for pair in sorted_letters_coords:
            new_letters.append(pair[0])
            new_coords.append(pair[1])
        return new_letters, new_coords

    def Process_Turn(self, data_packet):
        '''

        :param turn_packet: a list of data.
        :return:
        '''
        # criteria for advancing the next turn:
        # if Trading letters:
        # No criteria
        success = False
        self.Reset_Temp_Playboard()
        if data_packet.mode == 0: # trading letters
            new_letters = self.Exchange_Letters(data_packet.letters_played)
            self.players[self.active_player].Exchange_Letters(data_packet.letters_played, new_letters)
            self.last_active_player = self.active_player
            if int(self.active_player) + 1 > self.total_players:
                self.active_player = '1'
            else:
                self.active_player = str(int(self.active_player) + 1)

            success = True
            return success
        else: # attempting to commit a play
            # if Playing at least 1 letter:
            # 1) the letters played are all adjacent to one another
            # 2) the letters played are all in a single direction (vert or horiz)
            # 3) the letters played occupy at least 1 "required spot" (directly adjacent to an already placed tile
            # 4) all new word strings formed are valid words

            all_unique_words_made = []

            # for each letter played, add it to a temp playboard
            # ensure all letters played are in a straight line:
            letters_played = [item.letter for item in data_packet.letters_played]
            letters_played, coords_played = self.Order_Letters(letters_played, data_packet.coords_played)
            for letter, coord in zip(letters_played, coords_played):
                self.Set_Letter(letter, coord, temp=True)
            # for each letter played, see if it constructs any words on the temp playboard (now accounting for if a word is JUST new letters)
            for letter, coord in zip(letters_played, coords_played):
                #coord = invert_coord_y(coord)
                full_words, full_words_coords = self.Detect_words(letter, coord)

                # only keep a successfully constructed word the first time.
                for word, coords in zip(full_words, full_words_coords):
                    if [word, coords] not in all_unique_words_made:
                        all_unique_words_made.append([word, coords])
            score = 0
            is_valid = False
            all_validity_checks = []
            for word_and_coords in all_unique_words_made:
                word = word_and_coords[0]
                coords = word_and_coords[1]
                is_valid = self.Check_Word_Validity(word)
                all_validity_checks.append(is_valid)
                if is_valid:
                    score += self.Calculate_Score(word, coords)
                else:
                    print("INVALID PLAY! ")

            if all(all_validity_checks):
                for word_and_coords in all_unique_words_made:
                    word = word_and_coords[0]
                    coords = word_and_coords[1]
                    for letter, coord in zip(word, coords):
                        self.Set_Letter(letter, coord)
                self.players[self.active_player].Increase_Score(score)
                self.players[self.active_player].Spend_Letters(data_packet.letters_played)
                success = True
            else:
                print("Did not set letters")
                pass

            # reload inventory if needed
            needs_tiles = len(self.players[self.active_player].Get_Inventory()) < 7
            while needs_tiles and len(self.word_Q) > 0:
                needs_tiles = self.players[self.active_player].Add_To_Inventory(self.Get_New_Letter())

            self.last_active_player = self.active_player

            if int(self.active_player) + 1 > self.total_players:
                self.active_player = '1'
                print("Active Player is hard set to 1")
            else:
                self.active_player = str(int(self.active_player) + 1)
                print("Active Player is: " + self.active_player)
            return success

    def Check_Word_Validity(self, word):
        valid_word_text = '2019_word_list.txt'
        valid_words = open(valid_word_text, 'r')
        is_valid = False
        for v_word in valid_words.readlines():
            if v_word.rstrip('\n') == word.upper():
                is_valid = True
        valid_words.close()
        return is_valid

    def Get_New_Letter(self):
        '''
        get the letter from the end of the Q
        :param count:
        :return:
        '''
        return self.word_Q.pop(0)


    def Get_letter_from_playboard(self, coord, temp=False):
        x = coord[0]
        y = coord[1]
        if temp:
            return self.__temp_playboard[y][x]
        else:
            return self.__playboard[y][x]

    def Get_WordQ_Len(self):
        return len(self.word_Q)

    def Detect_playable_spots(self, coords_played = []):
        '''
        returns a list of coordinates that are valid places to place a tile.
        :return:
        '''
        required_spots = [] # one slot of the newly played tiles MUST be in this list (of open spots next to played tiles)
        open_spots = []
        self.Reset_Temp_Playboard()
        if len(coords_played) == 1:
            x = coords_played[0][0]
            y = coords_played[0][1]
            eastern = (x + 1, y)
            western = (x - 1, y)
            northern = (x, y + 1)
            southern = (x, y - 1)
            if self.Get_letter_from_playboard(eastern) == '':
                required_spots.append(eastern)
            else:
                found_empty = False
                while eastern[0] < 14:
                    eastern = self.Add_Coords(eastern, (1,0))
                    if self.Get_letter_from_playboard(eastern) == '':
                        found_empty = True
                        break
                if found_empty:
                    required_spots.append(eastern)

            if self.Get_letter_from_playboard(western) == '':
                required_spots.append(western)
            else:
                found_empty = False
                while western[0] > 0:
                    western = self.Add_Coords(western, (-1,0))
                    if self.Get_letter_from_playboard(western) == '':
                        found_empty = True
                        break
                if found_empty:
                    required_spots.append(western)

            if self.Get_letter_from_playboard(northern) == '':
                required_spots.append(northern)
            else:
                found_empty = False
                while northern[1] < 14:
                    northern = self.Add_Coords(northern, (0,1))
                    if self.Get_letter_from_playboard(northern) == '':
                        found_empty = True
                        break
                if found_empty:
                    required_spots.append(northern)

            if self.Get_letter_from_playboard(southern) == '':
                required_spots.append(southern)
            else:
                found_empty = False
                while southern[1] > 0:
                    southern = self.Add_Coords(southern, (0,-1))
                    if self.Get_letter_from_playboard(southern) == '':
                        found_empty = True
                        break
                if found_empty:
                    required_spots.append(southern)

            return open_spots, required_spots
        for coord in coords_played:
            self.Set_Letter('_', coord, temp=True)
        for y, column in enumerate(self.__temp_playboard):
            for x, value in enumerate(column):
                # get all open spots
                # test required spots
                eastern = (x+1, y)
                western = (x-1, y)
                northern = (x, y+1)
                southern = (x, y-1)
                if value != '': # spot has a tile. test if adjacent tiles are empty
                    required = False
                    if x!= 14 and self.Get_letter_from_playboard(eastern, temp=True) == '': # test east
                        if eastern not in required_spots:
                            required_spots.append(eastern)
                            required = True
                    if x != 0 and self.Get_letter_from_playboard(western, temp=True) == '': # test west
                        if western not in required_spots:
                            required_spots.append(western)
                            required = True

                    if y != 14 and self.Get_letter_from_playboard(northern, temp=True) == '':
                        if northern not in required_spots:
                            required_spots.append(northern)
                            required = True

                    if y != 0 and self.Get_letter_from_playboard(southern, temp=True) == '':
                        if southern not in required_spots:
                            required_spots.append(southern)
                            required = True


                    if self.Get_letter_from_playboard((x, y), temp=True) == '' and not required:
                        if (x, y) not in open_spots:
                            open_spots.append((x, y))

        # required_spots is currently a list of all coords adjacent existing letters.
        # if the player has put down 2 tiles, then we get rid of all required spots that are not in their shared row/column
        spots_to_remove = []
        if len(coords_played) >= 2:
            x1, x2 = coords_played[0][0], coords_played[1][0]
            y1, y2 = coords_played[0][1], coords_played[1][1]
            if x1 == x2:
                for coord in required_spots:
                    if coord[0] != x1:
                        spots_to_remove.append(coord)
            elif y1 == y2:
                for coord in required_spots:
                    if coord[1] != y1:
                        spots_to_remove.append(coord)
            else:
                print("WE HAVE 2 OR MORE LETTERS PLAYED ON THE BOARD, BUT THEY ARE NOT IN A STRAIGHT LINE. SOMETHING IS WRONG.")
            for coord in spots_to_remove:
                required_spots.remove(coord)
        return open_spots, required_spots
    def Detect_words2(self, letter=None, coord=None):
        temp_playboard = self.Get_Temp_Playboard()
        row_at_coord = temp_playboard[coord[1]]
        column_at_coord = [temp_playboard[coord[i][0]] for i in range(0, len(temp_playboard))]
        return

    def Detect_words(self, letter=None, coord=None):
        '''
        Given a letter and its position on the board, look at each adjacent square on the board.
        If there is a letter in any adjacent square, combine the letters into a word until you cant anymore.
        Then, check in the opposite direction
        :param letters: A list of  each letter played this turn
        :param coords: A list of the [x,y] coords of each letter played
        :return: full_words[list]: each element is a word that was created by this play
        :return: full_words_coords[list]: each element is a list of coords that the word with the same element in full_words occupies
         '''
        score = 0

        n_coord = self.Add_Coords(coord, (0, -1))
        if n_coord[1] <= 14:
            n_letter = self.Get_letter_from_playboard(n_coord, temp=True)
        else:
            n_letter = ''

        s_coord = self.Add_Coords(coord, (0, 1))
        if s_coord[1] >= 0:
            s_letter = self.Get_letter_from_playboard(s_coord, temp=True)
        else:
            s_letter = ''

        w_coord = self.Add_Coords(coord, (-1, 0))
        if w_coord[0] >= 0:
            w_letter = self.Get_letter_from_playboard(w_coord, temp=True)
        else:
            w_letter = ''

        e_coord = self.Add_Coords(coord, (1, 0))
        if e_coord[0] <= 14:
            e_letter = self.Get_letter_from_playboard(e_coord, temp=True)
        else:
            e_letter = ''

        e_word_fragment = ''
        e_fragment_coords = []

        w_word_fragment = ''
        w_fragment_coords = []

        n_word_fragment = ''
        n_fragment_coords = []

        s_word_fragment = ''
        s_fragment_coords = []

        full_words = []
        we_coords = []
        ns_coords = []
        full_words_coords = []

        if w_letter != '':
            w_search = True
            while w_search:
                w_word_fragment =  self.Get_letter_from_playboard(w_coord, temp=True) + w_word_fragment
                w_fragment_coords.insert(0, w_coord)
                w_coord = self.Add_Coords(w_coord, (-1,0))
                if w_coord[0] < 0:
                    w_search = False
                    break
                if self.Get_letter_from_playboard(w_coord, temp=True) == '':
                    w_search = False
                    break

        if e_letter != '':
            e_search = True
            while e_search:
                e_word_fragment = e_word_fragment + self.Get_letter_from_playboard(e_coord, temp=True)
                e_fragment_coords.append(e_coord)
                e_coord = self.Add_Coords(e_coord, (1,0))
                if e_coord[0] > 14:
                    e_search = False
                    break
                if self.Get_letter_from_playboard(e_coord, temp=True) == '':
                    e_search = False
                    break

        if n_letter != '':
            n_search = True
            while n_search:
                n_word_fragment = self.Get_letter_from_playboard(n_coord, temp=True) + n_word_fragment
                n_fragment_coords.insert(0, n_coord)
                n_coord = self.Add_Coords(n_coord, (0,-1))
                if n_coord[0] < 0:
                    n_search = False
                    break
                if self.Get_letter_from_playboard(n_coord, temp=True) == '':
                    n_search = False
                    break
                if n_coord == coord:
                    break


            pass
        if s_letter != '':
            s_search = True
            while s_search:
                s_word_fragment =  s_word_fragment + self.Get_letter_from_playboard(s_coord, temp=True)
                s_fragment_coords.append(s_coord)
                s_coord = self.Add_Coords(s_coord, (0, 1))
                if s_coord[0] > 14:
                    s_search = False
                    break
                if self.Get_letter_from_playboard(s_coord, temp=True) == '':
                    s_search = False
                    break
                if s_coord == coord:
                    break

            pass

        # combine any fragments form east to west to create 1 possible word
        if len(e_word_fragment) or len(w_word_fragment):
            full_words.append(w_word_fragment + letter + e_word_fragment)
            we_coords.extend(w_fragment_coords)
            we_coords.append(coord)
            we_coords.extend(e_fragment_coords)

            full_words_coords.append(we_coords)


        # do the same for north to south
        if len(n_word_fragment) or len(s_word_fragment):
            full_words.append(n_word_fragment  + letter + s_word_fragment)
            ns_coords.extend(n_fragment_coords)
            ns_coords.append(coord)
            ns_coords.extend(s_fragment_coords)

            full_words_coords.append(ns_coords)

        return full_words, full_words_coords

    def Exchange_Letters(self, letters=[]):
        out_letters = []
        for letter in letters:
            from_q = self.Get_New_Letter()
            self.word_Q.append(letter)
            out_letters.append(from_q)
        random.shuffle(self.word_Q) # how convenient!
        return out_letters

    def End_Game(self):
        return

    def Calculate_Score(self, word = '', coords = []):
        '''
        takes the board's multiplier spaces into account and calculates the resulting score for this word.

        :param letters:
        :param coords:
        :return:
        '''
        # coord: [multiplier, word/letter]
        grand_total = 0

        word_multiplier = [1]
        for letter, coord in zip(word, coords):
            letter_value = self.letter_value[letter]
            if coord in self.special_tiles.keys():
                bonus = self.special_tiles[coord]
                if bonus[1] == 'w':
                    word_multiplier.append(bonus[0])
                elif bonus[1] == 'l':
                    letter_value = letter_value*bonus[0]
            grand_total += letter_value

        # after all the individual letter scores have been calc,
        # multiply the total by the word multipliers
        for multi in word_multiplier:
            grand_total = grand_total * multi

        return grand_total

    def Add_Coords(self, coord_1 = (), coord_2 = ()):
        '''
        Vector Addition
        :param coord_1:
        :param coord_2:
        :return:
        '''
        x = coord_1[0] + coord_2[0]
        y = coord_1[1] + coord_2[1]
        return (x,y)






if __name__ == '__main__':
    game = Scrabble()
    game.New_Game(2)
    game.players['1'] = player_.Player(1)
    game.players['2'] = player_.Player(2)

    # Testing word placed vertically, letters placed in random order
    words = ['n','k', 'a', 'b']
    coords = [(7,7), (7,8), (7,6), (7,5)]
    data = DataPacket(cmd='commit', letters_played=words, coords_played=coords)
    game.Process_Turn(data)