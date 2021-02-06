
class Player(object):
    def __init__(self, id):
        self.name = None
        self._inventory = []
        self._score = 0
        self._ID =  id # The unique number that identifies a player while online
        self.name_plate = None

    def set_ID(self, id_val):
        self._ID = id_val
        return

    def Get_ID(self):
        return self._ID

    def set_name(self, name):
        self.name = name
        return

    def set_name_plate(self, name_plate):
        self.name_plate = name_plate
        self.name_plate.set_name(self.name)
        return

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

    def Spend_Letters(self, letters=[]):
        '''
        This removes the letter from the inventory,
        so it should only be called when the play has been
        verified as legal.
        :param index:
        :return:
        '''
        for letter in letters:
            index = letters.index(letter)
            self._inventory.pop(index)
        return

    def Exchange_Letters(self, letters_to_remove, letters_to_add):
        for letter in letters_to_remove:
            self._inventory.remove(letter)
        self._inventory.extend(letters_to_add)

    def Increase_Score(self, points=int):
        self._score += points

    def Get_Score(self):
        return self._score
