from copy import copy


class IAlgorithm :
    def _possible_moves(self, board, config):  
        zero = 0
        try :
            board.index(zero)
        except ValueError :
            zero = ' '
        empty = board.index(zero)
        valid_moves=[]
        # top
        if((empty-int(config['cols']) > 0)):
            valid_moves.append(board[empty-int(config['cols'])])
        
        # bottom
        if((empty+int(config['cols'])) < (int(config['cols']*int(config['rows'])))):
            valid_moves.append(board[empty+int(config['cols'])])
        
        # left
        if(empty % int(config['cols']) > 0 ):
            valid_moves.append(board[empty-1])
        # right
        if ((empty+1) % int(config['cols']) > 0 ):
            valid_moves.append(board[empty+1])

        return valid_moves

    def _simulate_move(self, move, board):
        zero = 0
        try :
            board.index(zero)
            move = int(move)
        except ValueError :
            zero = ' '
        new_board = copy(board)
        old_0 = new_board.index(zero)
        new_0 = new_board.index(move)
        new_board[old_0], new_board[new_0] = new_board[new_0], new_board[old_0]
        return new_board


debug_template = """
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
debug_template_list = ['(','é','"','@','&','ç','-','è',')']
debug_board = [' ', '1', '2', '3', '4', '5', '6', '7', '8']
debug_config = {'rows':3,'cols':3}

