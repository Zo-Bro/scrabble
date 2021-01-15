#temp testing remote repo

class Player(object):
    def __init__(self, name=''):
        self.name = name
        self.__inventory = []
        self.__score = 0

    def Get_Inventory(self):
        return self.__inventory

    def Add_To_Inventory(self, letter = str):
        '''
        This adds a single letter to the inventory
        verifies that the player never gets more than 7 tiles

        :param letter:
        :return:
        '''
        if len(self.__inventory) + 1 <= 7:
            self.__inventory.append(letter)
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
        return self.__inventory.pop(index)

    def Increase_Score(self, points=int):
        self.__score += points

    def Get_Score(self):
        return self.__score
