from board import Board
from collections import defaultdict


class Solver:
    # The opposite of every move is stored in this dictionary.
    # This is used to rule out the repetetive moves that undo the previous move.
    OPPOSITES = {"l": "r", "r": "l", "u": "d", "d": "u"}

    def __init__(self, method="bfs"):
        self.method = method
        self.solution_moves = ""

    def BFS(self, board: Board):
        """
        Implementation of BFS approach to find the shortest path.
        Returns:
            solution_moves (str): string of moves to solve the puzzle. example: "ldru" meaning "left","down","right","up".
        """
        dim = board.dim
        goal = Board(dim).board_key
        q = [board]

        key0 = board.board_key
        seen_states_dict = defaultdict(str)
        seen_states_dict[key0] = ""

        while q:
            hist = seen_states_dict[key0]
            oppo = ""
            if hist:
                oppo = self.OPPOSITES[hist[-1]]

            new_states = q[0].get_new_states()

            q.pop(0)

            for move, state in new_states.items():
                key = state.board_key
                if not key in seen_states_dict and move != oppo:
                    q.append(state)
                    seen_states_dict[key] = hist + move
                if key == goal:
                    print("found!")
                    self.solution_moves = seen_states_dict[key]
                    return seen_states_dict[key]

            key0 = q[0].board_key

        print("No Solution Found! Make sure the board is solvable.")
        return ""

    def DFS(self,board: Board):
        """
        Implementation of DFS approach to find a solution. Important: the solution will not be the shortest path.
        Returns:
            solution_moves (str): string of moves to solve the puzzle. example: "ldru" meaning "left","down","right","up". 
        """
        dim = board.dim
        goal = Board(dim).board_key
        stack = [board]
        
        key0 = board.board_key
        seen_states_dict = defaultdict(str)
        seen_states_dict[key0] = ""
        
        while stack:
            
            hist = seen_states_dict[key0]
            oppo = ""
            if hist:
                oppo = self.OPPOSITES[hist[-1]]
            
            new_states = stack[-1].get_new_states()
            
            stack.pop(-1)
            
            for move,state in new_states.items():
                key = state.board_key
                if not key in seen_states_dict and move!=oppo:
                    stack.append(state)
                    seen_states_dict[key] = hist + move
                if key == goal:
                    print("found!")
                    self.solution_moves = seen_states_dict[key]
                    return seen_states_dict[key]

            key0 = stack[-1].board_key

        print("No Solution Found! Make sure the board is solvable.")
        return ""
    
    def solve(self, board):
        if self.method == 'bfs':
            solution = self.BFS(board)
        elif self.method == 'dfs':
            solution = self.DFS(board)
        else:
            raise Exception("method not recognized")
        return solution
