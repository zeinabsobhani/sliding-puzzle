# sliding-puzzle

This repo contains A^* (WIP), DFS and BFS solvers for the sliding puzzle challenge. 

## Prerequisites
- numpy

## How to Use
Module `Board` is responsible for creating objects of board. You can start by creating a random board:
```
n=3
board = Board.get_random_board(n)
```

To solve the board you can use the `Solver` module.
```
solution = Solver(method = 'bfs').solve(board)
```