import os
from PIL import Image
from config import *

class ImageLoader:
    def __init__(self, base_dir):
        self.image_dir = os.path.join(base_dir, "images")
        self.images = {}
        self._load_images()
    
    def _load_images(self):
        required_images = [
            "start_screen.png",
            "game_over_screen.png",
            "ending_screen.png",
            "kkokko_front.png",
            "kkokko_back.png",
            "kkokko_left.png",
            "kkokko_right.png",
            "car1.png",
            "car2.png",
            "motorcycle1.png",
            "motorcycle2.png",
            "eagle.png"
        ]
        
        for img_name in required_images:
            path = os.path.join(self.image_dir, img_name)
            if not os.path.exists(path):
                print(f"Warning: {img_name} not found")
                continue
            
            name = img_name.split('.')[0]
            is_rgba = name not in ['start_screen', 'game_over_screen']
            self.images[name] = self._load_and_resize_image(path, is_rgba, name)
        
        self.images['tiles'] = {}
        for map_type in MAP_TYPES:
            path = os.path.join(self.image_dir, f"{map_type}.png")
            if os.path.exists(path):
                height = MAP_LINE_HEIGHTS[map_type] * CELL_HEIGHT
                self.images['tiles'][map_type] = self._load_and_resize_tile(path, height)
            else:
                print(f"Warning: {map_type}.png not found")
    
    def _load_and_resize_image(self, path, is_rgba, name):
        img = Image.open(path).convert('RGBA' if is_rgba else 'RGB')
        
        if name in ['car1', 'car2']:
            return img.resize((CELL_WIDTH * 2, CELL_HEIGHT))
        elif name.startswith('motorcycle'):
            width = int(CELL_WIDTH * 1.5)
            height = int(CELL_HEIGHT * 0.8)
            return img.resize((width, height))
        elif name.startswith('kkokko'):
            return img.resize((CELL_WIDTH, CELL_HEIGHT))
        elif name == 'eagle':
            return img.resize((CELL_WIDTH * 2, CELL_HEIGHT * 2))
        else:
            return img.resize((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    
    def _load_and_resize_tile(self, path, height):
        img = Image.open(path).convert('RGBA')
        return img.resize((DISPLAY_WIDTH, height))