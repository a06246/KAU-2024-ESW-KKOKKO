import digitalio
import board
import time
from config import *
from .game_state import GameState

class InputHandler:
    def __init__(self):
        self.buttons = {
            'L': digitalio.DigitalInOut(getattr(board, f'D{PIN_BTN_L}')),
            'R': digitalio.DigitalInOut(getattr(board, f'D{PIN_BTN_R}')),
            'U': digitalio.DigitalInOut(getattr(board, f'D{PIN_BTN_U}')),
            'D': digitalio.DigitalInOut(getattr(board, f'D{PIN_BTN_D}')),
            '5': digitalio.DigitalInOut(getattr(board, f'D{PIN_BTN_5}')),
            '6': digitalio.DigitalInOut(getattr(board, f'D{PIN_BTN_6}'))
        }
        
        for button in self.buttons.values():
            button.direction = digitalio.Direction.INPUT
            button.pull = digitalio.Pull.UP

    def handle_input(self, game, game_map, chick, chick_pos):
        if game.state in [GameState.MENU, GameState.GAME_OVER]:
            if not self.buttons['6'].value:
                self._handle_game_start(game, chick, chick_pos, game_map)
                return
        
        if game.state == GameState.PLAYING:
            self._handle_game_input(game, game_map, chick, chick_pos)

    def _handle_game_start(self, game, chick, chick_pos, game_map):
        game.start()
        chick.reset_position(3, 6)
        chick_pos[0] = chick.x * CELL_WIDTH + CELL_WIDTH//2
        chick_pos[1] = chick.y * CELL_HEIGHT + CELL_HEIGHT//2
        game_map.reset()
        time.sleep(0.2)

    def _handle_game_input(self, game, game_map, chick, chick_pos):
        if not self.buttons['L'].value:
            chick.direction = "left"
        elif not self.buttons['R'].value:
            chick.direction = "right"
        elif not self.buttons['U'].value:
            chick.direction = "back"
        elif not self.buttons['D'].value:
            chick.direction = "front"
        elif not self.buttons['5'].value:
            self._handle_movement(game, game_map, chick, chick_pos)
            time.sleep(0.2)  # 디바운싱

    def _handle_movement(self, game, game_map, chick, chick_pos):
        moved = False
        
        if chick.direction == "front":
            if chick.y == 5:
                chick.y = 6
                moved = True
        elif chick.direction == "back":
            if game_map.current_view_start == 0:  # 최상단 영역에 도달했을 때
                if chick.y > 1:  # 최상단 2번째 줄까지만 이동 가능
                    chick.y -= 1
                    moved = True
            else:  # 일반 영역
                if chick.y == 6:
                    chick.y = 5
                    moved = True
                elif chick.y == 5:
                    if game_map.scroll_up():
                        chick.y = 5
                        moved = True
        elif chick.direction == "left" and chick.x > 0:
            chick.x -= 1
            moved = True
        elif chick.direction == "right" and chick.x < GRID_COLS - 1:
            chick.x += 1
            moved = True
        
        if moved:
            game.reset_timer()  # 이동할 때마다 타이머 리셋
        
        chick_pos[0] = chick.x * CELL_WIDTH + CELL_WIDTH//2
        chick_pos[1] = chick.y * CELL_HEIGHT + CELL_HEIGHT//2