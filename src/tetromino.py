"""
Tetromino (piece) definitions and logic.
Each tetromino has a shape, color, and rotation states.
"""

import random
from typing import List, Tuple


class Tetromino:
    """Represents a Tetris piece with its shape, position, and rotation."""
    
 
    SHAPES = {
        'I': [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            [[0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]

        ],
        'O': [
            [[0, 0, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]]
        ],
        'T': [
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 0, 0]]
        ],
        'S': [
            [[0, 0, 0, 0],
             [0, 0, 1, 1],
             [0, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 1, 0]]
        ],
        'Z': [
            [[0, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 1, 0],
             [0, 1, 1, 0],
             [0, 1, 0, 0]]
        ],
        'J': [
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 0, 0]],
            [[0, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 0, 1, 0]]
        ],
        'L': [
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0]],
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [1, 0, 0, 0]],
            [[0, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 1, 0],
             [1, 1, 1, 0],
             [0, 0, 0, 0]]
        ],
    }

    
    COLORS = {
        'I': 12,  
        'O': 10,  
        'T': 13,  
        'S': 11,  
        'Z': 8,   
        'J': 5,   
        'L': 9 ,   
    }
    
    def __init__(self, shape_type: str | None = None, x: int = 3, y: int = 0):
        """
        Initialize a tetromino.
        
        Args:
            shape_type: Type of tetromino (I, O, T, S, Z, J, L). Random if None.
            x: Initial x position on the board
            y: Initial y position on the board
        """
        if shape_type is None:
            shape_type = random.choice(list(self.SHAPES.keys()))
        
        self.shape_type = shape_type
        self.rotations = self.SHAPES[shape_type]
        self.color = self.COLORS[shape_type]
        self.rotation_index = 0
        self.x = x
        self.y = y
    
    @property
    def shape(self) -> List[List[int]]:
        """Get the current rotation state of the tetromino."""
        return self.rotations[self.rotation_index]
    
    def rotate_clockwise(self):
        """Rotate the tetromino 90 degrees clockwise."""
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
    
    def rotate_counterclockwise(self):
        """Rotate the tetromino 90 degrees counterclockwise."""
        self.rotation_index = (self.rotation_index - 1) % len(self.rotations)
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """
        Get the absolute positions of all blocks in this tetromino.
        
        Returns:
            List of (x, y) tuples representing block positions
        """
        blocks = []
        for row in range(4):
            for col in range(4):
                if self.shape[row][col]:
                    blocks.append((self.x + col, self.y + row))
        return blocks
    
    def clone(self) -> 'Tetromino':
        """Create a copy of this tetromino."""
        new_tetromino = Tetromino(self.shape_type, self.x, self.y)
        new_tetromino.rotation_index = self.rotation_index
        return new_tetromino
