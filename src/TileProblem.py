from typing import List, Tuple, Optional, Iterable, Dict
import math

Action = str  # One of: "U", "D", "L", "R"

class TileProblem:
    def __init__(self, initial_state: List[List[Optional[int]]]):
        """
        initial_state: 2D list representing the puzzle.
            Example (3x3 / 8-puzzle):
                [[1, 2, 3],
                 [4, 5, 6],
                 [None, 7, 8]]
        None represents the blank tile.
        """
        self.initial_state = initial_state
        self.size = len(initial_state)

        # Basic structural checks
        assert self.size >= 2, "Puzzle must be at least 2x2."
        for row in initial_state:
            assert len(row) == self.size, "Initial state must be an N x N grid."

        self.goal_state = self._make_goal_state()


    def actions(self, state: List[List[Optional[int]]]) -> List[Action]:
        """
        Return the list of legal actions from the given state.
        Actions move the BLANK (None): "U", "D", "L", "R".
        """
        r, c = self._find_blank(state)
        moves: List[Action] = []

        ############ write your code between these blocks

        # add legal actions based on blank position (r, c) and board size

        ################################

        ROWS, COLS = self.size, self.size

        # Check UP
        if ((r-1) >= 0):
            moves.append("U")
        
        # Check Down
        if ((r+1) < ROWS):
            moves.append("D")

        # Check Left
        if ((c-1) >= 0):
            moves.append("L")
        
        if((c+1) < COLS):
            moves.append("R")

        return moves

    def result(self, state: List[List[Optional[int]]], action: Action) -> List[List[Optional[int]]]:
        """
        Return the new state after applying the action to move the blank.
        """
        r, c = self._find_blank(state)

        ############ write your code between these blocks

        # compute new blank position (nr, nc), assert it's in-bounds, and swap

        ################################

        ROWS, COLS = self.size, self.size
        nr, nc = r, c

        if action == "U":
            nr -= 1
        
        if action == "D":
            nr += 1
        
        if action == "L":
            nc -= 1
        
        if action == "R":
            nc += 1

        

        assert (nr >= 0 and nr < ROWS) and (nc >= 0 and nc < COLS)
        blank_r, blank_c = self._find_blank(state)
        
        state[blank_r][blank_c], state[nr][nc] = state[nr][nc], state[blank_r][blank_c]

        return state



    def goal_test(self, state: List[List[Optional[int]]]) -> bool:
        """Check if the puzzle is solved."""
        return state == self.goal_state

    # Placeholder function
    def step_cost(self, state: List[List[Optional[int]]], action: Action, next_state: List[List[Optional[int]]]) -> int:

        return 1
    
    def heuristic(self, state, h_option):
        distance_map = {}
        ROWS, COLS = len(self.goal_state), len(self.goal_state[0])

        for r in range(ROWS):
            for c in range(COLS):
                tile = self.goal_state[r][c]
                if tile:
                    distance_map[tile] = [r, c]

        if h_option == "manhattan":
            total_distance = 0
            for r in range(ROWS):
                for c in range(COLS):
                    tile = state[r][c]
                    if tile:
                        nr, nc = distance_map[tile]
                        curr_distance = (abs(nr - r)) + (abs(nc - c))
                        total_distance += curr_distance
            return total_distance
        
        if h_option == "missing":
            total_missing = 0
            for r in range(ROWS):
                for c in range(COLS):
                    tile = state[r][c]
                    if tile:
                        nr, nc = distance_map[tile]
                        if nr != r or nc != c:
                            total_missing += 1
            return total_missing
        
        return 1

            




    # ---------- Helpers ----------

    def _make_goal_state(self) -> List[List[Optional[int]]]:
        """Return the solved puzzle configuration as a 2D list with blank at the last cell."""
        n = self.size
        tiles = list(range(1, n * n)) + [None]
        return [tiles[i * n:(i + 1) * n] for i in range(n)]

    def _find_blank(self, state: List[List[Optional[int]]]) -> Tuple[int, int]:
        """Locate the (row, col) of the blank tile (None)."""
        for r in range(self.size):
            for c in range(self.size):
                if state[r][c] is None:
                    return (r, c)
        raise ValueError("No blank tile (None) found in state")

    def flatten(state: List[List[Optional[int]]]) -> List[Optional[int]]:
        """Return a 1D list view of the state (useful for hashing/printing/debug)."""
        return [cell for row in state for cell in row]

    def __str__(self) -> str:
        return "\n".join(" ".join("_" if v is None else str(v) for v in row) for row in self.initial_state)

    