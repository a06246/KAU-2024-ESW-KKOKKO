from enum import Enum
import time
from config import *

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    ENDING = 3

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.score = 0
        self.last_move_time = time.time()
        self.eagle_timer = 5  # 5초 타이머
        self.eagle_x = -100  # 화면 밖 왼쪽에서 시작
        self.eagle_y = 0
        self.eagle_speed = 10
        self.eagle_animation = False
        self.chick_visible = True

    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        # 마지막 이동 후 5초가 지났는지 체크
        if time.time() - self.last_move_time > self.eagle_timer:
            self.eagle_animation = True
        
        # 독수리 애니메이션 업데이트
        if self.eagle_animation:
            self.eagle_x += self.eagle_speed
            if not self.chick_visible:  # 꼬꼬를 잡은 후에는 위로 올라감
                self.eagle_y -= 5
            if self.eagle_x > DISPLAY_WIDTH + 100:  # 화면을 완전히 벗어났을 때
                self.state = GameState.GAME_OVER
    
    def start(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.last_move_time = time.time()
        self.eagle_x = -100
        self.eagle_animation = False
        self.chick_visible = True
    
    def game_over(self):
        self.state = GameState.GAME_OVER
        self.chick_visible = False
    
    def show_ending(self):
        self.state = GameState.ENDING
    
    def reset_timer(self):
        self.last_move_time = time.time()