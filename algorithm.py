from copy import copy
import time
from time import sleep
from ialgorithm import IAlgorithm

# definetly not a*. doesnt even work ffs
class AstarAlgorithm(IAlgorithm):
    def __init__(self): 
        self.name = "A* algorithm"
        self.solved = False
        self.searched_once = False
        self.solution = []
        self.iterations = 0
        self.depth = -1
        
        


    def distance_de_manhattan(self, xA, yA, xB, yB ):
        return abs(xB-xA) + abs(yB-yA)
    
    def piece_mal_placee(self, xA, yA, xB, yB ):
        if (xA != xB or yA != yB ):
            return 1
        else:
            return 0

    class Node():
        # could be a node factory, with heuristic implemented here. but yeah
        # this is ugly. but yeah
        visit = 0
        def __init__(self, parent, move, board):
            self.__class__.visit +=1
            self.parent = parent
            self.move = move
            self.board = board
            
            if self.parent == None:
                self.g = 0
            else :
                self.g = self.parent.g + 1
            self.h = 0
            self.f = self.h + self.g

        def equals(self, node):
            return (self.board == node.board)

        def in_list(self, node_list):
            for node in node_list:
                if(self.equals(node)):
                    return True
            return False

    def heuristic1(self, board, final_board):
        total_manhattan = 0
        for i in range(len(board)):
            if(board[i] != 0):
                xA = int(board.index(i))/3
                yA = int(board.index(i))%3
                xB = int(final_board.index(i))/3
                yB = int(final_board.index(i))%3 
                total_manhattan += self.distance_de_manhattan(xA, yA, xB, yB)
        return total_manhattan
    
    def heuristic2(self, board , final_board):
        total_pieces_mal_placees = 0
        for i in range(len(board)):
            if(board[i] != 0):
                xA = int(board.index(i))/3
                yA = int(board.index(i))%3
                xB = int(final_board.index(i))/3
                yB = int(final_board.index(i))%3  
                total_pieces_mal_placees += self.piece_mal_placee(xA, yA, xB, yB)
        return total_pieces_mal_placees

    def Astar(self, initial_board , final_board):
        # Initlialize the graph for A* :
            
        #choisir l'heuristique
        choise_heuristic = input("1-heuristique 1 : somme des distances de chaque pièce à sa position finale\n2-heuristique 2 : nombre de piéces mal placées\n")
        print("presser entrer pour commencer.")
        input()
        print("Recherche de la solution.....")
        sleep(1)
        
        #déclarer le noeud initial 
        node0 = self.Node(parent=None, move=None, board=initial_board) # initial node
        node0.g = 0
        if choise_heuristic == '1':
            node0.h = self.heuristic1(initial_board,final_board)
        elif choise_heuristic == '2':
            node0.h = self.heuristic2(initial_board,final_board)
        node0.f = node0.h + node0.g

    
        
        #open_node <- créer une liste contient le noeud initial
        open_nodes = [node0]
        closed_nodes = []
        
        if (initial_board == final_board):
            self.solved = True
            self.solution = [0]

        self.searched_once = True
        self.iterations += 1
        

        # Nous recherchons tant qu'il y a des nœuds sur lesquels rechercher..
        while( (len(open_nodes) > 0) ):
            self.iterations += 1
            
            # selection de meilleur noeud par tri de la liste ouverte par rapport f :
            sorted(open_nodes, key=lambda node: node.f)
            curr_node = open_nodes[0]
            print("Rechrche Solution : nombre d'itération courant", self.iterations);
            print("Rechrche Solution : noeud courrant",curr_node.board)
            
            # si curr_node est le but, sortir de la boucle avec succès en retournant le chemin; 
            if(curr_node.board == final_board):
                self.solved = True
                self.solution = self.path_from_node(curr_node)
                return self.solution

            open_nodes.remove(curr_node)
            closed_nodes.append(curr_node)
            
            
            #next_nodes est le tableau des noeuds successeurs du noeud curr_node
            next_nodes = []
            for move in self._possible_moves(curr_node.board, self.config): 
                new_node = self.Node(parent=curr_node, board=self._simulate_move(move, curr_node.board), move=move)
                
                if choise_heuristic == '1':
                    new_node.h = self.heuristic1(initial_board,final_board)
                elif choise_heuristic == '2':
                    new_node.h = self.heuristic2(initial_board,final_board)
                # new_node.g is set automatically. And so shoud h and loss be... but yeah
                new_node.f = new_node.h + new_node.g
                next_nodes.append(new_node)
            
            #si on n'est pas des successeurs du noeud courant
            if(next_nodes == []):
                print("Error, next nodes is empty.")
                return
            #on boucle les noeuds successeurs de noeud courant 
            for node in next_nodes :
                if  not (node.in_list(closed_nodes)):
                    if not node.in_list(open_nodes):
                        open_nodes.append(node)
                    else :
                        for node_from_open_nodes in open_nodes:
                            if node.equals(node_from_open_nodes):
                                if node_from_open_nodes.g > node.g :
                                    open_nodes.remove(node_from_open_nodes)
                                    open_nodes.append(node)

                                break
        self.solved = False
        
    def path_from_node(self, node):
        path = []
        while(node.parent != None):
            path.append(node.move)
            node = node.parent
        
        return path
    


    def move(self, board, final_abord, config):
        if not self.searched_once :
            self.board = copy(board)
            self.board[self.board.index(' ')] = 0
            self.board = [ int(ele) for ele in self.board ]
            self.config = config    
            start_time = time.time()
            self.searched_once = True  
            
            self.Astar(self.board, final_abord )
            if self.solved :
                print("____Résolu dans {}secondes ({} iterations)____".format((time.time() - start_time), self.iterations ))
                try:
                    return str(self.solution.pop())
                except IndexError:
                    return str(None)
            else :
                return None
        else :
            if self.solution : 
                if self.solved :
                    return str(self.solution.pop() ) 
                else :
                    return None
           

