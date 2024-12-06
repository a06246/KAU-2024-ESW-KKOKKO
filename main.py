import os
import time
from PIL import Image
from game import (
    Game, GameState, Chick, 
    DisplayManager, InputHandler, 
    MapManager, ImageLoader
)
from config import *

def main():
    try:
        # 초기화
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # 게임 객체 초기화
        game = Game()
        display = DisplayManager()
        input_handler = InputHandler()
        image_loader = ImageLoader(BASE_DIR)
        
        # 게임 오브젝트 초기화
        chick = Chick(3, 6)
        chick_pos = [chick.x * CELL_WIDTH + CELL_WIDTH//2, 
                    chick.y * CELL_HEIGHT + CELL_HEIGHT//2]
        game_map = MapManager()

        print("Starting game... Press CTRL+C to exit.")
        print("Press Button 6 to start the game!")
        display.disp.fill(0)
        
        # 게임 루프
        while True:
            # 입력 처리
            input_handler.handle_input(game, game_map, chick, chick_pos)
            
            # 게임 상태 업데이트
            if game.state == GameState.PLAYING:
                game_map.update()
                game.update()
                
                # 충돌 체크
                if game_map.check_collision(chick_pos):
                    game.game_over()
                # 엔딩 체크
                elif game_map.check_ending(chick_pos):
                    game.show_ending()
            
            # 화면 그리기
            display.draw_screen(game, game_map, chick, chick_pos, image_loader.images)
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        raise e
    finally:
        print("Cleaning up...")
        display.cleanup()

if __name__ == "__main__":
    main() 