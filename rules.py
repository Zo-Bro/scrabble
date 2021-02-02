import random
import player as player_


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
        self.players = []

        # game flow vars
        self.current_played_letters = []
        self.current_played_coords = []
        self.active_player = 0
        self.total_players = 2
        self.p1_went = False
        self.p2_went = False
        self.p3_went = False
        self.p4_went = False
        self.active = False
        self.game_end = False

    def New_Game(self):
        self.word_Q = self.Build_Word_Q()
        self.Construct_Empty_Playboard()
        # TODO: UI function for selecting number of players

    def Generate_Players(self, num_players=2):
        for person in range(0, num_players):
            # TODO: UI function get the name for the player
            name_entry = 'Player_' + str(person)
            player = player_.Player(name=name_entry)
            self.players.append(player)

        # distribute beginning tiles for players
        for Player in self.players:
            need_tiles = True
            while need_tiles:
                need_tiles = Player.Add_To_Inventory(self.Get_New_Letter())

    def Construct_Empty_Playboard(self):
        self.__playboard = []
        for x in range(0, 15):
            row = ['' for y in range(0, 15)]
            self.__playboard.append(row)

    def Get_Playboard(self):
        return self.__playboard

    def Set_Letter(self, letter='', coord = ()):
        '''
        Playboard accessed row (y) 1st, column (x) 2nd
        :param letter:
        :param coord:
        :return:
        '''
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

    def Next_Turn(self):
        self.active_player = self.active_player + 1 % self.total_players
        return

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

    def Get_letter_from_playboard(self, coord):
        x = coord[0]
        y = coord[1]
        return self.__playboard[y][x]

    def Detect_words(self, letter=None, coord=None):
        '''
        Given a letter and its position on the board, look at each adjacent square on the board.
        If there is a letter in any adjacent square, combine the letters into a word until you cant anymore.
        Then, check in the opposite direction
        :param letters: A list of  each letter played this turn
        :param coords: A list of the [x,y] coords of each letter played
        :return: Int value of the play
        '''
        score = 0

        n_coord = self.Add_Coords(coord, (0, 1))
        if n_coord[1] <= 14:
            n_letter = self.Get_letter_from_playboard(n_coord)
        else:
            n_letter = ''

        s_coord = self.Add_Coords(coord, (0, -1))
        if s_coord[1] >= 0:
            s_letter = self.Get_letter_from_playboard(s_coord)
        else:
            s_letter = ''

        w_coord = self.Add_Coords(coord, (-1, 0))
        if w_coord[0] >= 0:
            w_letter = self.Get_letter_from_playboard(w_coord)
        else:
            w_letter = ''

        e_coord = self.Add_Coords(coord, (1, 0))
        if e_coord[0] <= 14:
            e_letter = self.Get_letter_from_playboard(e_coord)
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
                w_word_fragment =  self.Get_letter_from_playboard(w_coord) + w_word_fragment
                w_fragment_coords.insert(0, w_coord)
                w_coord = self.Add_Coords(w_coord, (-1,0))
                if w_coord[0] < 0:
                    w_search = False
                    break
                if self.Get_letter_from_playboard(w_coord) == '':
                    w_search = False
                    break

        if e_letter != '':
            e_search = True
            while e_search:
                e_word_fragment = e_word_fragment + self.Get_letter_from_playboard(e_coord)
                e_fragment_coords.append(e_coord)
                e_coord = self.Add_Coords(e_coord, (1,0))
                if e_coord[0] > 14:
                    e_search = False
                    break
                if self.Get_letter_from_playboard(e_coord) == '':
                    e_search = False
                    break

        if n_letter != '':
            n_search = True
            while n_search:
                n_word_fragment = self.Get_letter_from_playboard(n_coord) + n_word_fragment
                n_fragment_coords.insert(0, n_coord)
                n_coord = self.Add_Coords(n_coord, (0,1))
                if n_coord[0] > 14:
                    n_search = False
                    break
                if self.Get_letter_from_playboard(n_coord) == '':
                    n_search = False
                    break


            pass
        if s_letter != '':
            s_search = True
            while s_search:
                s_word_fragment =  s_word_fragment + self.Get_letter_from_playboard(s_coord)
                s_fragment_coords.append(s_coord)
                s_coord = self.Add_Coords(s_coord, (0,-1))
                if s_coord[0] < 0:
                    s_search = False
                    break
                if self.Get_letter_from_playboard(s_coord) == '':
                    s_search = False
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
            full_words.append(n_word_fragment + letter + s_word_fragment)
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

    def Enter_Players(self):
        return

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

    def Construct_Word_String(self, letters = [], coords = []):
        '''
        given the letters and their coordinates in any order,
        create a word by putting the letters in order from either N > S or W > E
        If letters are not in this vector, reject the placement.

        Can I use vector math to calculate this easily?


        :param letters:
        :param coords:
        :return:
        '''
        return






if __name__ == '__main__':
    game = Scrabble()
    game.New_Game()
    print(game.word_Q)