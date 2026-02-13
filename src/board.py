from typing import List
from tetromino import Tetromino


class Board:
    """Manages the Tetris game board and piece placement."""
    
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.grid: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, tetromino: Tetromino) -> bool:
        """
        Check if a tetromino can be placed at its current position.
        
        Args:
            tetromino: The tetromino to check
            
        Returns:
            True if the position is valid, False otherwise
        """
        for x, y in tetromino.get_blocks():
            if x < 0 or x >= self.width or y >= self.height:
                return False
            
            if y >= 0 and self.grid[y][x] != 0:
                return False
        
        return True
    
    def lock_tetromino(self, tetromino: Tetromino):
        """
        Lock a tetromino into the board grid.
        
        Args:
            tetromino: The tetromino to lock in place
        """
        for x, y in tetromino.get_blocks():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = tetromino.color
    
    def clear_lines(self) -> int:
        """
        Clear all complete lines from the board.
        
        Returns:
            Number of lines cleared
        """
        lines_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            if all(self.grid[y][x] != 0 for x in range(self.width)):
                del self.grid[y]
                self.grid.insert(0, [0] * self.width)
                lines_cleared += 1
            else:
                y -= 1
        
        return lines_cleared
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over (blocks in the top row).
        
        Returns:
            True if game is over, False otherwise
        """
        return any(self.grid[0][x] != 0 for x in range(self.width))
    
    def get_cell(self, x: int, y: int) -> int:
        """
        Get the color value of a cell.
        
        Args:
            x: Column index
            y: Row index
            
        Returns:
            Color value (0 if empty)
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return 0
    
    def reset(self):
        """Clear the board."""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
