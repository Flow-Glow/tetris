import pyxel
from game import TetrisGame
from renderer import Renderer


class App:
    
    def __init__(self):
        pyxel.init(200, 180, title="Tetris")
        
        jump_scare_image = pyxel.Image.from_image("./assets/img.png")
        pyxel.sounds[0].pcm("./assets/bgm.ogg")
        pyxel.sounds[1].pcm("./assets/horror-scream_D_minor.ogg")
        pyxel.play(0, 0, loop=True)
        
        self.game = TetrisGame(board_width=10, board_height=20)
        self.renderer = Renderer(self.game, jump_scare_image)
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        """Update game state (called every frame)."""
        if pyxel.btnp(pyxel.KEY_R):
            self.game.reset()
        
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        self.game.update()
    
    def draw(self):
        self.renderer.draw()


def main():
    """Entry point for the game."""
    App()


if __name__ == "__main__":
    main()
