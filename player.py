class Player(object):
    def __init__(self, name=''):
        self.name = name
        self._inventory = []
        self._score = 0
        self._ID =  0 # The unique number that identifies a player while online

    def Set_ID(self, id_val):
        self._ID = id_val
        return

    def Get_ID(self):
        return self._ID

    def Get_Inventory(self):
        return self._inventory

    def Add_To_Inventory(self, letter = str):
        '''
        This adds a single letter to the inventory
        verifies that the player never gets more than 7 tiles

        :param letter:
        :return:
        '''
        if len(self._inventory) + 1 <= 7:
            self._inventory.append(letter)
            return True
        else:
            return False

    def Spend_Letter(self, index=int):
        '''
        This removes the letter from the inventory,
        so it should only be called when the play has been
        verified as legal.
        :param index:
        :return:
        '''
        return self._inventory.pop(index)

    def Increase_Score(self, points=int):
        self._score += points

    def Get_Score(self):
        return self._score
