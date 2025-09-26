# n-Puzzle Solver

This project implements an n-puzzle solver using A* search and Recursive Best-First Search (RBFS) algorithms with Manhattan distance and misplaced tiles heuristics.

## Project Structure

```
n-Puzzle_Solver/
├── src/
│   ├── TileProblem.py      # Core puzzle logic and heuristics
│   ├── puzzleSolver.py     # Main solver with A* and RBFS algorithms
│   ├── puzzleGenerator.py  # Generates random puzzle configurations
│   └── formatCheck.py      # Validates output format
├── puzzles/                # Sample puzzle files
│   ├── puzzle1.txt
│   ├── puzzle2.txt
│   ├── puzzle3.txt
│   ├── puzzle4.txt
│   └── puzzle5.txt
├── generate_puzzle.sh      # Script to generate multiple puzzles
├── run_puzzles.sh         # Script to run solver on multiple puzzles
└── README.md
```

## Code Components

### src/TileProblem.py
The TileProblem class defines the puzzle environment and provides:
- State representation and goal state generation
- Legal action generation (U, D, L, R moves for the blank tile)
- State transition function
- Two heuristic functions:
  - Manhattan distance (h1): Sum of distances each tile is from its goal position
  - Misplaced tiles (h2): Number of tiles not in their correct positions

### src/puzzleSolver.py
Contains the main solving algorithms:
- **A* Search**: Uses a priority queue with f(n) = g(n) + h(n)
- **RBFS (Recursive Best-First Search)**: Memory-efficient alternative to A*
- Supports both heuristics and measures performance metrics

### src/puzzleGenerator.py
Generates puzzle configurations in two modes:
- Random shuffle of tiles
- Systematic generation by applying K random moves to the solved state

## Input Format

Puzzle files should be comma-separated values with empty cells representing the blank tile:
```
1,2,3
4,5,6
,7,8
```

## Usage

### Running the Solver

To solve a single puzzle:
```bash
cd src
python puzzleSolver.py <algorithm> <size> <heuristic> <input_file> <output_file>
```

Parameters:
- algorithm: 1 for A*, 2 for RBFS
- size: Puzzle dimension (3 for 8-puzzle, 4 for 15-puzzle)
- heuristic: 1 for Manhattan distance, 2 for misplaced tiles
- input_file: Path to puzzle input file
- output_file: Path for solution output

Example:
```bash
python puzzleSolver.py 1 3 1 "../puzzles/puzzle1.txt" "output.txt"
```

### Generating Puzzles

To generate a random puzzle:
```bash
cd src
python puzzleGenerator.py <N> <output_file>
```

To generate a puzzle with K moves from solved state:
```bash
cd src
python puzzleGenerator.py <N> <K> <output_file>
```

Example:
```bash
python puzzleGenerator.py 3 puzzle_new.txt
python puzzleGenerator.py 3 20 puzzle_20_moves.txt
```

### Batch Processing

The run_puzzles.sh script processes multiple puzzles:
```bash
./run_puzzles.sh [input_directory] [output_directory] [algorithm] [heuristic]
```

Example:
```bash
./run_puzzles.sh puzzles results 1 1
```

This runs A* with Manhattan distance on all puzzles in the puzzles directory.

### Generating Multiple Puzzles

Use generate_puzzle.sh to create multiple 15-puzzles:
```bash
./generate_puzzle.sh
```

### Format Validation

To check if output format is correct:
```bash
cd src
python formatCheck.py <output_file>
```

## Output Format

Solutions are output as comma-separated move sequences:
- U: Move blank up
- D: Move blank down
- L: Move blank left
- R: Move blank right

Example: `U,R,D,L`

## Sample Puzzles

The project includes sample puzzles:
- puzzle1.txt, puzzle2.txt, puzzle3.txt: 8-puzzles (3x3)
- puzzle4.txt, puzzle5.txt: 15-puzzles (4x4)

## Requirements

- Python 3.x
- Standard libraries: heapq, copy, random, argparse, time, sys, typing, math, re

## Performance Notes

- A* generally finds optimal solutions quickly for smaller puzzles
- RBFS uses less memory but may take longer for complex puzzles  
- Manhattan distance heuristic typically outperforms misplaced tiles heuristic
- 15-puzzles are significantly more challenging than 8-puzzles