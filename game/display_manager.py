import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw
from config import *
from .game_state import GameState
import time

class DisplayManager:
    def __init__(self):
        self.spi = board.SPI()
        
        self.dc = digitalio.DigitalInOut(getattr(board, f'D{PIN_DC}'))
        self.cs = digitalio.DigitalInOut(getattr(board, f'CE{PIN_CS}'))
        self.reset = digitalio.DigitalInOut(getattr(board, f'D{PIN_RST}'))
        
        self.dc.switch_to_output(value=False)
        self.cs.switch_to_output(value=True)
        self.reset.switch_to_output(value=True)
        
        self.disp = st7789.ST7789(
            self.spi,
            rotation=180,
            width=DISPLAY_WIDTH,
            height=DISPLAY_HEIGHT,
            x_offset=0,
            y_offset=80,
            baudrate=64000000,
            cs=self.cs,
            dc=self.dc,
            rst=self.reset,
        )
        
        self.backlight = digitalio.DigitalInOut(getattr(board, f'D{PIN_BACKLIGHT}'))
        self.backlight.switch_to_output()
        self.backlight.value = True
        
        self.disp.fill(0)

    def cleanup(self):
        self.disp.fill(0)
        self.backlight.value = False

    def draw_screen(self, game, game_map, chick, chick_pos, images):
        screen = Image.new('RGB', (DISPLAY_WIDTH, DISPLAY_HEIGHT), '#000000')
        draw = ImageDraw.Draw(screen)
        
        if game.state == GameState.MENU:
            screen.paste(images['start_screen'], (0, 0))
        elif game.state == GameState.GAME_OVER:
            screen.paste(images['game_over_screen'], (0, 0))
        elif game.state == GameState.ENDING:
            screen.paste(images['ending_screen'], (0, 0))
        elif game.state == GameState.PLAYING:
            self._draw_game_screen(screen, draw, game_map, chick, chick_pos, images, game)
        
        self.disp.image(screen)

    def _draw_game_screen(self, screen, draw, game_map, chick, chick_pos, images, game):
        # 맵 그리기
        for map_type, start_row in game_map.get_visible_map():
            if map_type in images['tiles']:
                y = start_row * CELL_HEIGHT
                screen.paste(images['tiles'][map_type], (0, y))
        
        # 차량 그리기
        for vehicle in game_map.visible_vehicles:
            self._draw_vehicle(screen, vehicle, images)
        
        # 독수리 애니메이션 중이면 독수리 그리기
        if game.eagle_animation and 'eagle' in images:
            eagle_image = images['eagle']
            if game.chick_visible:  # 꼬꼬가 아직 보이는 상태일 때만
                game.eagle_y = chick_pos[1] - CELL_HEIGHT  # 꼬꼬의 y 위치로 이동
                # 독수리와 병아리의 충돌 체크 (더 정확한 충돌 범위)
                if (abs(game.eagle_x - chick_pos[0]) < CELL_WIDTH * 1.5 and 
                    abs(game.eagle_y - chick_pos[1]) < CELL_HEIGHT * 1.5):
                    game.chick_visible = False  # 병아리 숨기기
            screen.paste(eagle_image, (int(game.eagle_x), int(game.eagle_y)), eagle_image)
        
        # 병아리가 보이는 상태일 때만 그리기
        if game.chick_visible:
            self._draw_chick(screen, chick, chick_pos, images)

    def _draw_vehicle(self, screen, vehicle, images):
        vehicle_image = images[vehicle.type]
        if vehicle.direction == "left":
            vehicle_image = vehicle_image.transpose(Image.FLIP_LEFT_RIGHT)
        screen.paste(vehicle_image, (int(vehicle.x), int(vehicle.y)), vehicle_image)

    def _draw_chick(self, screen, chick, chick_pos, images):
        chick_image = images[f'kkokko_{chick.direction}']
        x = chick_pos[0] - CELL_WIDTH//2
        y = chick_pos[1] - CELL_HEIGHT//2
        screen.paste(chick_image, (x, y), chick_image) 