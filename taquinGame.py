from copy import copy
from time import sleep
from algorithm import AstarAlgorithm
from ialgorithm import IAlgorithm
from random import randrange

class CLITaquin():
    def __init__(self, algorithm , board=None):
        self.algorithm = algorithm
        self.END = 0
        self.TEMPLATE = """
        _________________
        |     |     |     |
        |  (  |  é  |  "  |
        |_____|_____|_____|
        |     |     |     |
        |  @  |  &  |  ç  |
        |_____|_____|_____|
        |     |     |     |
        |  -  |  è  |  )  |
        |_____|_____|_____|
        """  
            # î
            # | columns and rows identifiers.
        self.TEMPLATE_LIST = ['(','é','"','@','&','ç','-','è',')']
        
        if (board == None):
            self.BOARD = [' ', '1', '2', '3', '4', '5', '6', '7', '8'] #final board
            self.generate = True
        else :
            self.BOARD = board
            self.generate = False
        self.CONFIG = {'rows':3,'cols':3}
        self.ROUND = 0

    def draw(self):
        curr_BOARD = copy(self.TEMPLATE)
        for i in range(len(self.BOARD)):
            curr_BOARD = curr_BOARD.replace(self.TEMPLATE_LIST[i], self.BOARD[i])
        print(curr_BOARD)
        del curr_BOARD
    
    def move(self, x):
        space = self.BOARD.index(' ')
        new_space = self.BOARD.index(x)
        self.BOARD[space] , self.BOARD[new_space] = self.BOARD[new_space] , self.BOARD[space]

    def update(self): 
        self.draw()
        x = str(self.algorithm.move(self.BOARD, self.CONFIG))
        if (self.is_valid(x)):
            self.move(x)
            if self.is_won():
                self.END=1
        else :
            self.END=-1

    def is_won(self):
        won = True
        i = 0
        while (won &
         (i< (len(self.BOARD) -1))
         ):
            i = i+1
            won = (self.BOARD[i-1] <= self.BOARD[i])
        return won

    def shuffle(self, complexity):
        tools = IAlgorithm()    
        for _ in range(complexity):
            options = [ str(o) for o in tools._possible_moves(self.BOARD, self.CONFIG) ]
            x = options[randrange(len(options))]
            self.move(x)
        return self.BOARD

    def autoGenerate(self):    
        if(self.generate):
            _i = None
            while (not _i):
                _i = input("Tapez un niveau de complexité [1;oo[ : ")
            complexity = int(_i)
            self.shuffle(complexity)
            print("l'état initiale est générée.")
        

    def is_valid(self, x):
        # x being the piece we want to move
        zero = 0
        try :
            self.BOARD.index(zero)
        except ValueError :
            zero = ' '
        empty = self.BOARD.index(zero)
        valid_moves=[]
        # top
        if((empty-int(self.CONFIG['cols']) > 0)):
            valid_moves.append(self.BOARD[empty-int(self.CONFIG['cols'])])        
        # bottom
        if((empty+int(self.CONFIG['cols'])) < (int(self.CONFIG['cols']*int(self.CONFIG['rows'])))):
            valid_moves.append(self.BOARD[empty+int(self.CONFIG['cols'])])        
        # left
        if(empty % int(self.CONFIG['cols']) > 0 ):
            valid_moves.append(self.BOARD[empty-1])
        # right
        if ((empty+1) % int(self.CONFIG['cols']) > 0 ):
            valid_moves.append(self.BOARD[empty+1])
        return x in valid_moves

    def main(self):
        if(self.generate):
            self.autoGenerate()
        while(self.END==0):
            self.ROUND += 1
            self.update()
            sleep(1)
        if (self.END == -1):
            print("Pathetic.")
        else :
            self.draw()
            print("profondeur de la solution: "+str(self.ROUND))
            print("Nombre des noeuds visités: "+str(self.algorithm.visit_nodes))
            


if __name__ == "__main__":
    print("*** Jeu De Taquin ***")
    choise = '1'
    while(choise != '2' or choise != '1' or choise != '3'):
        choise = input("1-Donner l'état initiale\n2-Générer automatiquement\n3-quitter\n")
        if choise == '2' :
            CLITaquin(AstarAlgorithm()).main()
        elif choise == '1' :
            board = input("insérez l'état initial sous la forme d'une chaine et remplacez la case vide par un espace\n ")
            CLITaquin(AstarAlgorithm(),list(board)).main()
        elif choise == '3':
            break
        

    