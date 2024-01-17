import numpy as np
import warnings


class Board:
    """
    Class that creates a board Object. The board object has the following arguments:
    dim: Dimension of the board. The board is always square. Ex: 3 means a 3x3 board.
    board: 2D numpy array representing the board
    One of these should be specified for a board object to initiate. If the dim is passed, the initialized
    board would be the board in solved state (or goal). eg: np.array([[1,2,3],[4,5,6],[7,8,0]])
    If the board is specified, the dimension would be set as the shape of the board.
    """

    def __init__(self, dim: int = None, board: np.ndarray = None):
        if dim is None and board is None:
            raise Exception("provide either dim or board arguments")

        if dim is None:
            dim = board.shape[0]

        self.dim = dim
        self._max_no = dim * dim

        if board is None:
            board = self.goal_board()

        if board.shape[0] != board.shape[1]:
            warnings.warn("init warning")
            print(
                f"Board array should be square, the input board has the shape ({board.shape})"
            )

        if dim != board.shape[0]:
            warnings.warn("init warning")
            print(
                f"dim and the board dimensions do not match. The dim would be set as the shape of the board, {dim}!={board.shape[0]}"
            )

        self.board = board
        self.initial_board = self.board.copy()

    @property
    def board_key(self):
        """
        the board key, the key is a string of sequence of all elements.
        Example: the board np.array([[1,2,3],[4,5,6],[7,8,0]]) has the key '123456780'
        """
        return "".join([str(x) for x in self.board.flatten()])

    def goal_board(self):
        """
        creates the solved state of the board. eg: np.array([[1,2,3],[4,5,6],[7,8,0]])
        """
        board = np.r_[: self.dim][None, :] + [
            [1 + i] for i in range(0, self._max_no, self.dim)
        ]
        board[-1, -1] = 0
        return board

    def get_new_states(self):
        """
        generates possible new boards given the current board.
        Returns:
            states (Dict): dictionary where key is the movement that generates the new board, and values are new board objects.
            eg: {'r': <new_board>} meaning that moving 0 to the 'right' generated the <new_board>
            'r' stands for 'right', 'l': 'left', 'u': 'up' and 'd': 'down'.
        """
        zero_i, zero_j = np.where(self.board == 0)
        zero_i, zero_j = zero_i[0], zero_j[0]
        states = {}
        candidates = {
            "u": (zero_i - 1, zero_j),
            "d": (zero_i + 1, zero_j),
            "l": (zero_i, zero_j - 1),
            "r": (zero_i, zero_j + 1),
        }
        for key in candidates.keys():
            i, j = candidates[key]
            if i >= 0 and j >= 0 and i < self.dim and j < self.dim:
                states[key] = Board.from_arr(
                    self.slide(self.board.copy(), zero_i, zero_j, i, j)
                )
        return states

    def play(self, moves: str):
        """
        Given a string of moves play the board. the function updates self.board attribute in place.
        Args:
            moves (str): a string of moves made up of the move characters "l","r","u","d",
        """
        zero_i, zero_j = np.where(self.board == 0)
        zero_i, zero_j = zero_i[0], zero_j[0]

        for char in moves:
            if char == "u":
                i, j = zero_i - 1, zero_j
            elif char == "d":
                i, j = zero_i + 1, zero_j
            elif char == "l":
                i, j = zero_i, zero_j - 1
            elif char == "r":
                i, j = zero_i, zero_j + 1
            else:
                raise Exception(f"unknown move character {char}")

            Board.slide(self.board, zero_i, zero_j, i, j)
            zero_i, zero_j = i, j

    @staticmethod
    def count_inversions(flat_board: np.ndarray) -> int:
        """
        method counting the inversions of a flat board
        Args:
            flat_board (1D-array): flattened 2D array eg: [1,2,3,4,5,6,7,8,0]
        Retuens:
            inversion_count (int): number of inversions
        """
        inversion_count = 0
        _max_no = len(flat_board)
        for i in range(0, _max_no):
            for j in range(i + 1, _max_no):
                if (
                    flat_board[j] != 0
                    and flat_board[i] != 0
                    and flat_board[i] > flat_board[j]
                ):
                    inversion_count += 1
        return inversion_count

    @staticmethod
    def is_solvable(board: np.ndarray) -> bool:
        """
        Determine if the board is solvable. Uses inversion_counts.
        Args:
            board (np.array): 2D array of the board
        Returns:
            (bool): True if the board is solvable, False otherwise
        """
        flat_board = board.flatten()
        cinv = Board.count_inversions(flat_board)
        if cinv % 2 == 0:
            return True
        return False

    @classmethod
    def get_random_board(cls, dim: int, max_iter: int = 1000):
        """
        Generates a random board object.
        Args:
            dim (int): the dimension of the board
            max_iter (int): number of iterations to generate a solvable board. default 1000.
        """
        max_iter = 1000
        i = 0
        while i < max_iter:
            board = np.random.choice(dim * dim, dim * dim, replace=False).reshape(
                dim, dim
            )
            if Board.is_solvable(board):
                return cls(dim=dim, board=board)
            i += 1
        print("max iterations reached, please try again!")

        return None

    @classmethod
    def from_arr(cls, arr: np.ndarray):
        """
        Generates a board object for a 2D array.
        Args:
            arr (np.array): 2D array representing the state of the board
        """
        assert (
            arr.shape[0] == arr.shape[1]
        ), f"The input array should be square. the provided array has shape ({arr.shape})"
        n = arr.shape[0]
        return cls(dim=n, board=arr)

    @staticmethod
    def slide(board: np.ndarray, i1: int, j1: int, i2: int, j2: int) -> np.ndarray:
        """
        slide two tiles on the board.
        Args:
            board (np.array): 2D array representing the board
            i1,j1: row and column position of the first tile
            i2,j2: row and column position of the second tile
        Returns:
            board (np.array): rearranged 2D array
        """
        board[i1, j1], board[i2, j2] = board[i2, j2], board[i1, j1]
        return board

    def __eq__(self,other):
        return np.all(self.board == other.board)

    def __lt__(self, other):
        return self.board[0,0]<other.board[0,0]
    
    def __le__(self, other):
        return self.board[0,0]<=other.board[0,0]