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
        self.word_Q = []
        self.game_end = False
        self.score_board = {}
        self.__playboard = []
        self.players = []

    def New_Game(self):
        self.word_Q = self.Randomize_Letters()
        self.Construct_Empty_Playboard()
        # TODO: UI function for selecting number of players
        num_players = 2
        for person in range(0, num_players):
            # TODO: UI function get the name for the player
            name_entry = 'Player_' + str(person)
            player = player_.Player(name=name_entry)
            self.players.append(player)

        # distribute beginning tiles for players
        for Player in self.players:
            need_tiles = True
            while need_tiles:
                need_tiles = Player.Add_To_Inventory(self.word_Q.pop(0))

    def Construct_Empty_Playboard(self):
        self.__playboard = []
        for x in range(0, 15):
            row = ['' for y in range(0, 15)]
            self.__playboard.append(row)

    def Get_Playboard(self):
        return self.__playboard

    def Set_Letter_On_Playboard(self, letter='', coord = []):
        '''
        Playboard accessed row (y) 1st, column (x) 2nd
        :param letter:
        :param coord:
        :return:
        '''
        x = coord[0]
        y = coord[1]
        self.__playboard[y].pop([x])
        self.__playboard[y].insert(x, letter)

    def Randomize_Letters(self):
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

    def Check_Word_Validity(self, letters=[]):
        # TODO: query a scrabble dictionary database online

        return

    def Score_Current_Play(self):
        return

    def Draw_Letters(self):
        '''
        Remove letters from the Queue and add them to the indicated players hand
        :param count:
        :return:
        '''


        return

    def Play_Letters(self, letters=[], coords=[]):
        '''
        Recursive.
        Need to ensure placement of letters is unoccupied, and that any nearby words created are also valid plays
        scoring algorithm per word: (letter*multiplier+letter*multiplier+...)*word_multiplier
        :param letters: A list of  each letter played this turn
        :param coords: A list of the [x,y] coords of each letter played
        :return: Int value of the play
        '''
        score = 0

        for letter, coord in zip(letters, coords):
            if self.__playboard[coord] != '':
                # this spot is occupied by a letter. This is an invalid play
                return 0
            elif self.__playboard[self.Add_Coords(coord, [1, 0])] != '':
                # get the letters in West  direction, construct word, and check if word is valid
                pass
            elif self.__playboard[self.Add_Coords(coord, [-1, 0])] != '':
                # get the letters in East direction, construct word, and check if word is valid
                pass
            elif self.__playboard[self.Add_Coords(coord, [0, 1])] != '':
                # get the letters in North direction, construct word, and check if word is valid
                pass
            elif self.__playboard[self.Add_Coords(coord, [0, -1])] != '':
                # get the letters in South direction, construct word, and check if word is valid
                pass
            else:
                # there are no letters near this new letter. No recursive scoring happens.
                pass

        score += self.Calculate_Score(letters = letters, coords = coords)
        return score


    def Exchange_Letters(self, letters=[]):
        return

    def Enter_Players(self):
        return

    def End_Game(self):
        return

    def Calculate_Score(self, letters = [], coords = []):
        '''
        takes the board's multiplier spaces into account and calculates the resulting score for this word.

        :param letters:
        :param coords:
        :return:
        '''
        # coord: [multiplier, word/letter]
        grand_total = 0
        # TODO: Add all special tile multipliers
        special_tiles = {
            # triple word scores
            [0,0]:[3,'w'],
            [0,7]:[3,'w'],
            [0,14]:[3,'w'],
            [7, 14]: [3, 'w'],
            [14,0]:[3,'w'],
            [14, 7]: [3, 'w'],
            [14,14]:[3,'w'],
            [7,0]:[3,'w'],


        }
        word_multiplier = [1]
        for letter, coord in zip(letters, coords):
            letter_value = self.letter_value[letter]
            if coord in special_tiles.keys():
                bonus = special_tiles[coord]
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

    def Add_Coords(self, coord_1 = [], coord_2 = []):
        '''
        Vector Addition
        :param coord_1:
        :param coord_2:
        :return:
        '''
        return [a+b for a,b in zip(coord_1, coord_2)]

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

    def Sense_Completed_Words(self, letters = [], coords = []):
        '''
        When a letter is placed, this event fires.
        It creates a list of coords for each continuous line of words from N to S or W to E.

        :param letters:
        :param coords:
        :return:
        '''

        return






if __name__ == '__main__':
    game = Scrabble()
    game.New_Game()
    print(game.word_Q)