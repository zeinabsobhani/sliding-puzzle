from board import Board
from collections import defaultdict
from heapq import *
import warnings

class Solver:
    # The opposite of every move is stored in this dictionary.
    # This is used to rule out the repetetive moves that undo the previous move.
    OPPOSITES = {"l": "r", "r": "l", "u": "d", "d": "u"}

    def __init__(self, method="bfs", score = 'manhattan'):
        self.method = method
        self.solution_moves = ""
        self.score = score

    def BFS(self, board: Board):
        """
        Implementation of BFS approach to find the shortest path.
        Args:
            board (Board): A board object to solve
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

    def DFS(self, board: Board):
        """
        Implementation of DFS approach to find a solution. Important: the solution will not be the shortest path.
        Args:
            board (Board): A board object to solve
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

            for move, state in new_states.items():
                key = state.board_key
                if not key in seen_states_dict and move != oppo:
                    stack.append(state)
                    seen_states_dict[key] = hist + move
                if key == goal:
                    print("found!")
                    self.solution_moves = seen_states_dict[key]
                    return seen_states_dict[key]

            key0 = stack[-1].board_key

        print("No Solution Found! Make sure the board is solvable.")
        return ""
    
    @staticmethod
    def manhattan_distance(board, goal):
        """
        Calculate the manhattan distance between the board and the goal
        Args:
            board (np.array): the board
            goal (np.array): the target board
        Returns:
            (int): the distance value
        """
        
        result = 0
        n = board.shape[0]
        for i in range(n):
            for j in range(n):
                result += abs(board[i][j] - goal[i][j])

        return result

    @staticmethod
    def misplaced_tiles(board, goal):
        """
        Calculate the misplaced tiles distance between the board and the goal
        Args:
            board (np.array): the board
            goal (np.array): the target board
        Returns:
            (int): the distance value
        """
        
        result = 0
        n = board.shape[0]
        for i in range(n):
            for j in range(n):
                if board[i][j]!=goal[i][j]:
                    result+=1

        return result

    def hueristic_score(self, board, goal, method = 'manhattan'):
        """
        Wrapper function for calculating the heuristic score
        """
        if method == 'manhattan':
            return self.manhattan_distance(board, goal)

        if method == 'misplaced':
            return self.misplaced_tiles(board, goal)
    

    def AStar(self, board, score = 'manhattan'):
        """
        Implementation of AStar approach to find a solution.
        Args:
            board (Board): A board object to solve
            score (str): 'manhattan' or 'misplaced'. scoring function to use for the heuristic algorithm, Default to 'manhattan'.
        Returns:
            solution_moves (str): string of moves to solve the puzzle. example: "ldru" meaning "left","down","right","up". 
        """
        dim = board.dim
        goal = Board(dim)
        goal_key = goal.board_key
        q = []
        score_val = self.hueristic_score(board.board,goal.board, method = score) 

        # using heap improves performance. Selecting min(score) in O(1) time.
        heappush(q, (score_val, board))

        key0 = board.board_key
        seen_states_dict = defaultdict(str)
        seen_states_dict[key0] = ""

        while q:
            hist = seen_states_dict[key0]
            oppo = ""
            if hist:
                oppo = self.OPPOSITES[hist[-1]]

            parent = heappop(q)
            new_states = parent[1].get_new_states()

            for move, state in new_states.items():
                key = state.board_key
                if not key in seen_states_dict and move != oppo:
                    score_val = self.hueristic_score(state.board,goal.board, method = score) 
                    # penalty the steps taken so far (the level of the node in the tree)
                    score_val += len(hist)

                    heappush(q, (score_val, state))
                    seen_states_dict[key] = hist + move
                if key == goal_key:
                    print("found!")
                    self.solution_moves = seen_states_dict[key]
                    q = []
                    return self.solution_moves

            key0 = q[0][1].board_key

    def solve(self, board):
        """
        Wrapper function to solve the board with a selected method.
        """
        if self.method == 'bfs':
            solution = self.BFS(board)
        elif self.method == "dfs":
            solution = self.DFS(board)
        elif self.method == 'astar':
            solution = self.AStar(board, self.score)
        else:
            raise Exception("method not recognized")
        return solution
    
