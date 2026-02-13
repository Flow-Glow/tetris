import pyxel
from game import TetrisGame


class Renderer:    
    BLOCK_SIZE = 8
    BOARD_OFFSET_X = 50
    BOARD_OFFSET_Y = 10
    
    def __init__(self, game: TetrisGame, jump_scare_image: pyxel.Image):
        """
        Initialize the renderer.
        
        Args:
            game: The TetrisGame instance to render
            jump_scare_image: Full-screen image for the jump scare
        """
        self.game = game
        self.jump_scare_image = jump_scare_image
        self.board_width_px = game.board.width * self.BLOCK_SIZE
        self.board_height_px = game.board.height * self.BLOCK_SIZE
    
    def draw(self):
        """Main draw function called every frame."""
        pyxel.cls(0)
        
        title = "TETRIS"
        title_x = pyxel.width // 2 - len(title) * 2
        pyxel.text(title_x, 2, title, 7)
        
        shake_x = 0
        shake_y = 0
        if self.game.shake_timer > 0:
            intensity = self.game.shake_timer / 3
            shake_x = int(pyxel.rndf(-intensity, intensity))
            shake_y = int(pyxel.rndf(-intensity, intensity))
        
        original_x = self.BOARD_OFFSET_X
        original_y = self.BOARD_OFFSET_Y
        
        self.BOARD_OFFSET_X += shake_x
        self.BOARD_OFFSET_Y += shake_y
        
        self.draw_board()
        self.draw_placed_blocks()
        
        if self.game.clear_animation_timer > 0:
            self.draw_line_clear_effect()
        
        self.draw_current_piece()
        self.draw_ghost_piece()
        self.draw_particles()
        
        self.BOARD_OFFSET_X = original_x
        self.BOARD_OFFSET_Y = original_y
        
        self.draw_ui()
        
        if self.game.tetris_timer > 0:
            self.draw_tetris()
        
        if self.game.level_up_timer > 0:
            self.draw_level_up()
        
        if self.game.score_popup_timer > 0:
            self.draw_score_popup()
        
        if self.game.combo > 1 and self.game.clear_animation_timer > 0:
            self.draw_combo()
        
        if self.game.spin_message_timer > 0:
            self.draw_spin_message()
        
        if self.game.jump_scare_timer > 0:
            self.draw_jump_scare()
        
        if self.game.paused:
            self.draw_pause_screen()
        elif self.game.game_over:
            self.draw_game_over_screen()
    
    def draw_board(self):
        """Draw the game board with borders and grid."""
        x = self.BOARD_OFFSET_X
        y = self.BOARD_OFFSET_Y
        w = self.board_width_px
        h = self.board_height_px
        
        for row in range(0, self.game.board.height, 2):
            for col in range(0, self.game.board.width, 2):
                if self.game.board.get_cell(col, row) == 0:
                    px = x + col * self.BLOCK_SIZE
                    py = y + row * self.BLOCK_SIZE
                    pyxel.pset(px + self.BLOCK_SIZE - 1, py + self.BLOCK_SIZE - 1, 1)
        
        border_color = 7
        if self.game.level_up_timer > 60:
            border_color = 10 if (self.game.level_up_timer // 4) % 2 == 0 else 7
        
        pyxel.rectb(x - 2, y - 2, w + 4, h + 4, 1)
        pyxel.rectb(x - 1, y - 1, w + 2, h + 2, border_color)
    
    def draw_placed_blocks(self):
        """Draw all blocks that have been placed on the board."""
        for row in range(self.game.board.height):
            for col in range(self.game.board.width):
                color = self.game.board.get_cell(col, row)
                if color != 0:
                    self.draw_block(col, row, color)
    
    def draw_current_piece(self):
        """Draw the active falling piece."""
        if not self.game.current_piece:
            return
        
        for x, y in self.game.current_piece.get_blocks():
            if y >= 0:
                self.draw_block(x, y, self.game.current_piece.color)
    
    def draw_ghost_piece(self):
        """Draw a ghost/shadow of where the piece will land."""
        if not self.game.current_piece or self.game.game_over:
            return
        
        ghost = self.game.current_piece.clone()
        while self.game.board.is_valid_position(ghost):
            ghost.y += 1
        ghost.y -= 1
        
        for x, y in ghost.get_blocks():
            if y >= 0:
                px = self.BOARD_OFFSET_X + x * self.BLOCK_SIZE
                py = self.BOARD_OFFSET_Y + y * self.BLOCK_SIZE
                pyxel.rectb(px, py, self.BLOCK_SIZE, self.BLOCK_SIZE, 7)
                pyxel.rectb(px + 1, py + 1, self.BLOCK_SIZE - 2, self.BLOCK_SIZE - 2, 7)
    
    def draw_block(self, grid_x: int, grid_y: int, color: int):
        """
        Draw a single block at grid coordinates.
        
        Args:
            grid_x: Grid column
            grid_y: Grid row
            color: Pyxel color index
        """
        px = self.BOARD_OFFSET_X + grid_x * self.BLOCK_SIZE
        py = self.BOARD_OFFSET_Y + grid_y * self.BLOCK_SIZE
        
        pyxel.rect(px, py, self.BLOCK_SIZE, self.BLOCK_SIZE, color)
        pyxel.line(px, py, px + self.BLOCK_SIZE - 1, py, 7)
        pyxel.line(px, py, px, py + self.BLOCK_SIZE - 1, 7)
        pyxel.line(px + self.BLOCK_SIZE - 1, py + 1, 
                   px + self.BLOCK_SIZE - 1, py + self.BLOCK_SIZE - 1, 0)
        pyxel.line(px + 1, py + self.BLOCK_SIZE - 1, 
                   px + self.BLOCK_SIZE - 1, py + self.BLOCK_SIZE - 1, 0)
    
    def draw_ui(self):
        """Draw UI elements (score, next piece, controls)."""
        ui_x = self.BOARD_OFFSET_X + self.board_width_px + 10
        ui_y = self.BOARD_OFFSET_Y
        
        pyxel.text(ui_x, ui_y, "SCORE", 7)
        pyxel.text(ui_x, ui_y + 8, str(self.game.score), 10)
        
        if self.game.high_score > 0:
            pyxel.text(ui_x, ui_y + 16, f"HI:{self.game.high_score}", 6)
        
        pyxel.text(ui_x, ui_y + 28, "LINES", 7)
        pyxel.text(ui_x, ui_y + 36, str(self.game.lines_cleared), 10)
        
        pyxel.text(ui_x, ui_y + 48, "LEVEL", 7)
        pyxel.text(ui_x, ui_y + 56, str(self.game.level), 10)
        
        if self.game.combo > 1:
            pyxel.text(ui_x, ui_y + 66, f"x{self.game.combo} COMBO", 8)
        
        pyxel.text(ui_x, ui_y + 78, "NEXT", 7)
        pyxel.rectb(ui_x - 1, ui_y + 87, 26, 26, 7)
        self.draw_next_piece(ui_x, ui_y + 88)
        
        hold_x = self.BOARD_OFFSET_X-30
        hold_y = 10
        hold_color = 17
        pyxel.text(hold_x, hold_y, "HOLD", hold_color)
        if self.game.held_piece:
            self.draw_held_piece(hold_x, hold_y + 10)
        
        if self.game.piece_on_ground and self.game.lock_delay_timer > 0:
            bar_y = self.BOARD_OFFSET_Y + self.board_height_px + 3
            bar_width = int((self.game.lock_delay_timer / self.game.LOCK_DELAY) * self.board_width_px)
            pyxel.rect(self.BOARD_OFFSET_X, bar_y, self.board_width_px, 3, 1)
            if bar_width > 0:
                color = 11 if bar_width > self.board_width_px // 3 else 8
                pyxel.rect(self.BOARD_OFFSET_X, bar_y, bar_width, 3, color)
        
    def draw_next_piece(self, x: int, y: int):
        """Draw the next piece preview, centered."""
        if not self.game.next_piece:
            return
        
        min_col, max_col = 4, 0
        min_row, max_row = 4, 0
        for row in range(4):
            for col in range(4):
                if self.game.next_piece.shape[row][col]:
                    min_col = min(min_col, col)
                    max_col = max(max_col, col)
                    min_row = min(min_row, row)
                    max_row = max(max_row, row)
        
        offset_x = (3 - (max_col - min_col)) * 3
        offset_y = (3 - (max_row - min_row)) * 3
        
        for row in range(4):
            for col in range(4):
                if self.game.next_piece.shape[row][col]:
                    px = x + (col - min_col) * 6 + offset_x
                    py = y + (row - min_row) * 6 + offset_y
                    pyxel.rect(px, py, 5, 5, self.game.next_piece.color)
    
    def draw_held_piece(self, x: int, y: int):
        """Draw the held piece preview, centered and dimmed if unavailable."""
        if not self.game.held_piece:
            return
        
        min_col, max_col = 4, 0
        min_row, max_row = 4, 0
        for row in range(4):
            for col in range(4):
                if self.game.held_piece.shape[row][col]:
                    min_col = min(min_col, col)
                    max_col = max(max_col, col)
                    min_row = min(min_row, row)
                    max_row = max(max_row, row)
        
        offset_x = (3 - (max_col - min_col)) * 3
        offset_y = (3 - (max_row - min_row)) * 3
        
        color = self.game.held_piece.color if self.game.can_swap else 5
        
        for row in range(4):
            for col in range(4):
                if self.game.held_piece.shape[row][col]:
                    px = x + (col - min_col) * 6 + offset_x
                    py = y + (row - min_row) * 6 + offset_y
                    pyxel.rect(px, py, 5, 5, color)
    
    def draw_particles(self):
        """Draw particle effects."""
        for p in self.game.particles:
            px = self.BOARD_OFFSET_X + int(p['x'] * self.BLOCK_SIZE) + self.BLOCK_SIZE // 2
            py = self.BOARD_OFFSET_Y + int(p['y'] * self.BLOCK_SIZE) + self.BLOCK_SIZE // 2
            alpha = min(1.0, p['life'] / 15.0)
            if alpha > 0:
                pyxel.pset(px, py, p['color'])
    
    def draw_line_clear_effect(self):
        """Simple elegant fade effect for clearing lines."""
        fade = self.game.clear_animation_timer / 8
        
        for line_y in self.game.clearing_lines:
            y = self.BOARD_OFFSET_Y + line_y * self.BLOCK_SIZE
            if fade > 0.6:
                pyxel.rect(self.BOARD_OFFSET_X, y, self.board_width_px, self.BLOCK_SIZE, 7)
    
    def draw_level_up(self):
        """Display level up notification."""
        if self.game.level_up_timer > 30:
            text = f"LEVEL {self.game.level}!"
            text_x = pyxel.width // 2 - len(text) * 2
            text_y = self.BOARD_OFFSET_Y + self.board_height_px // 3
            
            pulse = (self.game.level_up_timer // 5) % 2
            color = 10 if pulse else 9
            
            pyxel.text(text_x, text_y, text, color)
    
    def draw_score_popup(self):
        """Show score gained from line clear."""
        if self.game.score_popup_timer > 30:
            text = f"+{self.game.score_popup}"
            text_x = self.BOARD_OFFSET_X + self.board_width_px // 2 - len(text) * 2
            text_y = self.BOARD_OFFSET_Y + 20 - (60 - self.game.score_popup_timer)
            pyxel.text(text_x, text_y, text, 10)
    
    def draw_combo(self):
        """Show combo counter."""
        text = f"COMBO x{self.game.combo}"
        text_x = self.BOARD_OFFSET_X + self.board_width_px // 2 - len(text) * 2
        text_y = self.BOARD_OFFSET_Y + self.board_height_px - 15
        pyxel.text(text_x, text_y, text, 8)
    
    def draw_tetris(self):
        """Display TETRIS message for 4+ line clears."""
        if self.game.tetris_timer > 40:
            text = "TETRIS!"
            text_x = pyxel.width // 2 - len(text) * 2
            text_y = self.BOARD_OFFSET_Y + self.board_height_px // 2 - 10
            
            bounce = abs((self.game.tetris_timer % 10) - 5)
            text_y -= bounce
            
            colors = [8, 9, 10, 11, 12]
            color = colors[(self.game.tetris_timer // 5) % len(colors)]
            
            pyxel.text(text_x + 1, text_y + 1, text, 0)
            pyxel.text(text_x, text_y, text, color)
    
    def draw_spin_message(self):
        """Display spin message (T-SPIN, S-SPIN, Z-SPIN)."""
        if self.game.spin_message_timer > 40:
            text = self.game.spin_message
            text_x = pyxel.width // 2 - len(text) * 2
            text_y = self.BOARD_OFFSET_Y + self.board_height_px // 2 + 10
            
            bounce = abs((self.game.spin_message_timer % 8) - 4)
            text_y -= bounce // 2
            
            colors = [8, 9, 10]
            color = colors[(self.game.spin_message_timer // 5) % len(colors)]
            
            pyxel.text(text_x + 1, text_y + 1, text, 0)
            pyxel.text(text_x, text_y, text, color)
    
    def draw_pause_screen(self):
        """Draw pause overlay."""
        text = "PAUSED"
        text_x = pyxel.width // 2 - len(text) * 2
        text_y = pyxel.height // 2
        
        pyxel.rect(text_x - 4, text_y - 4, len(text) * 4 + 8, 12, 0)
        pyxel.text(text_x, text_y, text, 10)
    
    def draw_jump_scare(self):
        """Draw jump scare effect on line clear."""
        pyxel.cls(0)
        pyxel.blt(0, 0, self.jump_scare_image, 0, 0, pyxel.width, pyxel.height)
    
    def draw_game_over_screen(self):
        """Draw game over overlay with score."""
        text1 = "GAME OVER"
        text2 = f"Score: {self.game.score}"
        text3 = f"Lines: {self.game.lines_cleared}"
        text4 = "Press R to restart"
        
        text1_x = pyxel.width // 2 - len(text1) * 2
        text2_x = pyxel.width // 2 - len(text2) * 2
        text3_x = pyxel.width // 2 - len(text3) * 2
        text4_x = pyxel.width // 2 - len(text4) * 2
        text_y = pyxel.height // 2 - 15
        
        pyxel.rect(text1_x - 6, text_y - 4, max(len(text1), len(text4)) * 4 + 12, 44, 0)
        pyxel.rectb(text1_x - 6, text_y - 4, max(len(text1), len(text4)) * 4 + 12, 44, 7)
        
        pulse_color = 8 if (pyxel.frame_count // 15) % 2 == 0 else 9
        pyxel.text(text1_x, text_y, text1, pulse_color)
        pyxel.text(text2_x, text_y + 12, text2, 10)
        pyxel.text(text3_x, text_y + 20, text3, 10)
        pyxel.text(text4_x, text_y + 32, text4, 7)
