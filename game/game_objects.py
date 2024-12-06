from config import *

class GameObject:
    def __init__(self, x, y, width, height, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def collides_with(self, other):
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

class Chick(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, CELL_WIDTH, CELL_HEIGHT)
        self.direction = "front"
        self.lives = 3
        self.is_on_log = False
    
    def reset_position(self, x, y):
        self.x = x
        self.y = y
        self.direction = "front"

class Vehicle(GameObject):
    def __init__(self, x, y, vehicle_type, direction="right", row=0, speed=None):
        if vehicle_type in ["car1", "car2"]:
            width = CELL_WIDTH * 2
            height = CELL_HEIGHT
            self.base_speed = 2
        else:  # motorcycle1, motorcycle2
            width = int(CELL_WIDTH * 1.5)
            height = int(CELL_HEIGHT * 0.8)
            self.base_speed = 2
            
        super().__init__(x, y, width, height)
        self.type = vehicle_type
        self.direction = direction
        self.row = row
        self.speed = speed if speed is not None else self.base_speed
        
        if direction == "left":
            self.speed = -abs(self.speed)
        else:
            self.speed = abs(self.speed)

    def move(self):
        if self.row >= 60:
            speed_multiplier = 1 + ((self.row - 60) * 0.1)
            current_speed = self.speed * speed_multiplier
            self.x += current_speed
        else:
            self.x += self.speed
        