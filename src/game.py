"""
Main game logic and state management.
Handles game flow, scoring, and user input processing.
"""

import pyxel
from board import Board
from tetromino import Tetromino
from typing import Optional


class TetrisGame:
    """Main Tetris game controller."""
    
    FALL_SPEED_TABLE = [
        48, 43, 38, 33, 28, 23, 18, 13, 8, 6,
        5, 5, 5, 4, 4, 4, 3, 3, 3, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
    ]
    MOVE_DELAY = 8
    INITIAL_MOVE_DELAY = 15
    LOCK_DELAY = 15
    LOCK_DELAY_EXTENSION = 5
    
    def __init__(self, board_width: int = 10, board_height: int = 20, start_level: int = 1):
        """
        Initialize the game.
        
        Args:
            board_width: Width of the game board
            board_height: Height of the game board
            start_level: Starting level for testing
        """
        self.board = Board(board_width, board_height)
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.held_piece: Optional[Tetromino] = None
        self.can_swap = True
        
        self.score = 0
        self.high_score = 0
        self.start_level = max(1, start_level)
        self.lines_cleared = (self.start_level - 1) * 10
        self.level = self.start_level
        self.game_over = False
        self.paused = False
        self.combo = 0
        
        self.clearing_lines = []
        self.clear_animation_timer = 0
        self.level_up_timer = 0
        self.score_popup = 0
        self.score_popup_timer = 0
        self.tetris_timer = 0
        self.shake_timer = 0
        self.particles = []
        self.spin_message = ""
        self.spin_message_timer = 0
        self.last_rotation_was_spin = False
        
        self.jump_scare_active = False
        self.jump_scare_timer = 0
        self.fall_counter = 0
        self.fall_speed = self.calculate_fall_speed(self.level)
        
        self.move_left_counter = 0
        self.move_right_counter = 0
        self.move_down_counter = 0
        
        self.lock_delay_timer = 0
        self.piece_on_ground = False
        
        self.spawn_new_piece()
    
    def spawn_new_piece(self):
        """Spawn a new tetromino at the top of the board."""
        if self.next_piece is None:
            self.next_piece = Tetromino()
        
        self.current_piece = self.next_piece
        self.current_piece.x = self.board.width // 2 - 2
        self.current_piece.y = 0
        
        self.next_piece = Tetromino()
        
        self.lock_delay_timer = 0
        self.piece_on_ground = False
        self.can_swap = True
        self.last_rotation_was_spin = False
        
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """
        Try to move the current piece.
        
        Args:
            dx: Change in x position
            dy: Change in y position
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.current_piece or self.game_over or self.paused:
            return False
        
        self.current_piece.x += dx
        self.current_piece.y += dy
        
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        
        if self.piece_on_ground:
            self.lock_delay_timer = min(self.lock_delay_timer + self.LOCK_DELAY_EXTENSION, self.LOCK_DELAY)
        
        return True
    
    def rotate_piece(self, clockwise: bool = True):
        """
        Try to rotate the current piece.
        
        Args:
            clockwise: True for clockwise rotation, False for counterclockwise
        """
        if not self.current_piece or self.game_over or self.paused:
            return
        
        if clockwise:
            self.current_piece.rotate_clockwise()
        else:
            self.current_piece.rotate_counterclockwise()
        
        rotation_successful = False
        if not self.board.is_valid_position(self.current_piece):
            for dx in [0, -1, 1, -2, 2]:
                self.current_piece.x += dx
                if self.board.is_valid_position(self.current_piece):
                    rotation_successful = True
                    break
                self.current_piece.x -= dx
            
            if not rotation_successful:
                if clockwise:
                    self.current_piece.rotate_counterclockwise()
                else:
                    self.current_piece.rotate_clockwise()
                self.last_rotation_was_spin = False
                return
        else:
            rotation_successful = True
        
        if rotation_successful and self.current_piece.shape_type in ['T', 'S', 'Z']:
            self.last_rotation_was_spin = self.check_spin()
        else:
            self.last_rotation_was_spin = False
        
        if self.piece_on_ground:
            self.lock_delay_timer = min(self.lock_delay_timer + self.LOCK_DELAY_EXTENSION, self.LOCK_DELAY)
    
    def check_spin(self) -> bool:
        """Check if the last rotation was a spin (3+ corners occupied)."""
        if not self.current_piece:
            return False
        
        corners = [
            (self.current_piece.x + 0, self.current_piece.y + 0),
            (self.current_piece.x + 2, self.current_piece.y + 0),
            (self.current_piece.x + 0, self.current_piece.y + 2),
            (self.current_piece.x + 2, self.current_piece.y + 2),
        ]
        
        occupied_corners = 0
        for cx, cy in corners:
            if (cx < 0 or cx >= self.board.width or 
                cy < 0 or cy >= self.board.height or
                self.board.get_cell(cx, cy) != 0):
                occupied_corners += 1
        
        return occupied_corners >= 3
    
    def hold_piece(self):
        """Swap current piece with held piece."""
        if not self.can_swap or self.game_over or self.paused or not self.current_piece:
            return
        
        if self.held_piece is None:
            self.held_piece = Tetromino(self.current_piece.shape_type)
            self.spawn_new_piece()
        else:
            temp_type = self.held_piece.shape_type
            self.held_piece = Tetromino(self.current_piece.shape_type)
            self.current_piece = Tetromino(temp_type)
            self.current_piece.x = self.board.width // 2 - 2
            self.current_piece.y = 0
            
            self.lock_delay_timer = 0
            self.piece_on_ground = False
        
        self.can_swap = False
        self.last_rotation_was_spin = False
    
    def hard_drop(self):
        """Drop piece instantly and lock it."""
        if not self.current_piece or self.game_over or self.paused:
            return
        
        drop_distance = 0
        while self.move_piece(0, 1):
            drop_distance += 1
        
        self.score += drop_distance * 2
        self.lock_current_piece()
    
    def lock_current_piece(self):
        """Lock the current piece and spawn a new one."""
        if not self.current_piece:
            return
        
        self.board.lock_tetromino(self.current_piece)
        
        full_lines = [y for y in range(self.board.height) 
                      if all(self.board.grid[y][x] != 0 for x in range(self.board.width))]
        
        if full_lines:
            self.clearing_lines = full_lines
            self.clear_animation_timer = 8
            self.combo += 1
            
            if pyxel.rndf(0, 1) < 0.05:
                self.jump_scare_active = True
                self.jump_scare_timer = 10
                self.shake_timer = 30
                pyxel.play(1, 1, loop=False)
            
            lines = len(full_lines)
            self.lines_cleared += lines
            
            spin_bonus = 0
            spin_name = ""
            if self.last_rotation_was_spin and self.current_piece.shape_type in ['T', 'S', 'Z']:
                piece_name = self.current_piece.shape_type
                if lines == 1:
                    spin_bonus = 800 * self.level
                    spin_name = f"{piece_name}-SPIN!"
                elif lines == 2:
                    spin_bonus = 1200 * self.level
                    spin_name = f"{piece_name}-SPIN DOUBLE!"
                elif lines == 3:
                    spin_bonus = 1600 * self.level
                    spin_name = f"{piece_name}-SPIN TRIPLE!"
                
                if spin_name:
                    self.spin_message = spin_name
                    self.spin_message_timer = 80
                    self.shake_timer = max(self.shake_timer, 12)
            
            line_scores = [0, 100, 300, 500, 800]
            score_gained = line_scores[min(lines, 4)] * self.level + spin_bonus
            
            if self.combo > 1:
                score_gained += 50 * self.combo * self.level
            
            self.score += score_gained
            self.score_popup = score_gained
            self.score_popup_timer = 60
            
            if self.score > self.high_score:
                self.high_score = self.score
            
            self.shake_timer = 4 + (lines * 2)
            
            if lines >= 4:
                self.tetris_timer = 80
            
            old_level = self.level
            self.level = (self.lines_cleared // 10) + 1
            if self.level > old_level:
                self.level_up_timer = 90
            
            self.fall_speed = self.calculate_fall_speed(self.level)
            
            for y in full_lines:
                for x in range(0, self.board.width, 3):
                    color = self.board.grid[y][x] if self.board.grid[y][x] != 0 else 7
                    self.particles.append({
                        'x': x, 'y': y,
                        'dx': pyxel.rndf(-1, 1), 'dy': pyxel.rndf(-2, -0.5),
                        'life': 20, 'color': color
                    })
        else:
            self.combo = 0
        
        if self.board.is_game_over():
            self.game_over = True
        elif self.clear_animation_timer == 0:
            self.spawn_new_piece()
    
    def update(self):
        """Update game state (called every frame)."""
        for p in self.particles[:]:
            p['x'] += p['dx'] * 0.1
            p['y'] += p['dy'] * 0.1
            p['dy'] += 0.15
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)
        
        if self.clear_animation_timer > 0:
            self.clear_animation_timer -= 1
            if self.clear_animation_timer == 0:
                self.board.clear_lines()
                self.clearing_lines = []
                if not self.game_over:
                    self.spawn_new_piece()
            return
        
        if self.level_up_timer > 0:
            self.level_up_timer -= 1
        
        if self.score_popup_timer > 0:
            self.score_popup_timer -= 1
        
        if self.tetris_timer > 0:
            self.tetris_timer -= 1
        
        if self.shake_timer > 0:
            self.shake_timer -= 1
        
        if self.spin_message_timer > 0:
            self.spin_message_timer -= 1
        
        if self.jump_scare_timer > 0:
            self.jump_scare_timer -= 1
        
        if self.game_over:
            return
        
        if pyxel.btnp(pyxel.KEY_P):
            self.paused = not self.paused
        
        if self.paused:
            return
        
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_X):
            self.rotate_piece(clockwise=True)
        if pyxel.btnp(pyxel.KEY_Z):
            self.rotate_piece(clockwise=False)
        
        if pyxel.btnp(pyxel.KEY_C):
            self.hold_piece()
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.hard_drop()
            return
        
        if pyxel.btn(pyxel.KEY_LEFT):
            self.move_left_counter += 1
            if self.move_left_counter == 1 or \
               (self.move_left_counter > self.INITIAL_MOVE_DELAY and 
                self.move_left_counter % self.MOVE_DELAY == 0):
                self.move_piece(-1, 0)
        else:
            self.move_left_counter = 0
        
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.move_right_counter += 1
            if self.move_right_counter == 1 or \
               (self.move_right_counter > self.INITIAL_MOVE_DELAY and 
                self.move_right_counter % self.MOVE_DELAY == 0):
                self.move_piece(1, 0)
        else:
            self.move_right_counter = 0
        
        if pyxel.btn(pyxel.KEY_DOWN):
            self.move_down_counter += 1
            if self.move_down_counter % max(2, self.fall_speed // 10) == 0:
                if not self.move_piece(0, 1):
                    if not self.piece_on_ground:
                        self.piece_on_ground = True
                        self.lock_delay_timer = self.LOCK_DELAY
                else:
                    self.score += 1
        else:
            self.move_down_counter = 0
        
        self.fall_counter += 1
        if self.fall_counter >= self.fall_speed:
            self.fall_counter = 0
            if self.move_piece(0, 1):
                self.piece_on_ground = False
                self.lock_delay_timer = 0
            else:
                if not self.piece_on_ground:
                    self.piece_on_ground = True
                    self.lock_delay_timer = self.LOCK_DELAY
        
        if self.piece_on_ground:
            self.lock_delay_timer -= 1
            if self.lock_delay_timer <= 0:
                self.lock_current_piece()
    
    def reset(self):
        """Reset the game to initial state."""
        self.board.reset()
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.lines_cleared = (self.start_level - 1) * 10
        self.level = self.start_level
        self.game_over = False
        self.paused = False
        self.fall_counter = 0
        self.fall_speed = self.calculate_fall_speed(self.level)
        self.combo = 0
        self.clearing_lines = []
        self.clear_animation_timer = 0
        self.level_up_timer = 0
        self.score_popup = 0
        self.score_popup_timer = 0
        self.tetris_timer = 0
        self.shake_timer = 0
        self.particles = []
        self.lock_delay_timer = 0
        self.piece_on_ground = False
        self.held_piece = None
        self.can_swap = True
        self.spin_message = ""
        self.spin_message_timer = 0
        self.last_rotation_was_spin = False
        self.jump_scare_active = False
        self.jump_scare_timer = 0
        self.next_piece = None
        self.spawn_new_piece()

    def calculate_fall_speed(self, level: int) -> int:
        """Calculate fall speed using NES-style frames-per-row table."""
        index = max(0, min(level - 1, len(self.FALL_SPEED_TABLE) - 1))
        return self.FALL_SPEED_TABLE[index]
