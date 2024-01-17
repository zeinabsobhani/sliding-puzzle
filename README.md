# sliding-puzzle

This repo contains A^* , DFS and BFS solvers for the sliding puzzle challenge. 

## Prerequisites
- numpy

## How to Use
Module `Board` is responsible for creating objects of board. You can start by creating a random board:
```
n=3
board = Board.get_random_board(n)
```

To solve the board you can use the `Solver` module. The method can be "astar", "bfs", or "dfs".
```
solution = Solver(method = 'bfs').solve(board)
print(solution)
----
"ldrrud"
```
The solution is the combination of moves to solve the board.
To check if the solution solves the board, you can play the board.
```
board.play(solution)
print(board.board)
----
[[1,2,3],[4,5,6],[7,8,0]]
```

