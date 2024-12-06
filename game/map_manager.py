import random
from config import *
from .game_objects import Vehicle

class MapManager:
    def __init__(self, total_rows=50):
        self.total_rows = total_rows
        self.current_view_start = self.total_rows - GRID_ROWS
        self.map_sections = []
        self.vehicles = []
        self.visible_vehicles = []
        
        self._initialize_map()
        self._initialize_vehicles()
    
    def _initialize_map(self):
        # 맨 아래 두 줄(0,1)은 2_line_road로 고정
        self.map_sections = []
        self.map_sections.append(('2_line_road', self.total_rows - 2))  # 맨 아래 2줄을 2_line_road로
        
        # 최상단 4줄은 4_line_background로 고정
        self.map_sections.append(('4_line_background', 0))
        current_row = 4  # 4_line_background 다음부터 시작
        
        # 나머지 줄은 패턴을 고려하여 생성
        last_type = 'road'
        while current_row < self.total_rows - 2:  # 마지막 2줄을 제외하고 생성
            if 'road' in last_type:
                map_type = random.choice(['2_line_driveway', '3_line_driveway', 
                                       '1_line_river', '2_line_river'])
            elif 'driveway' in last_type or 'river' in last_type:
                map_type = random.choice(['1_line_road', '2_line_road'])
            
            height = self._get_map_height(map_type)
            if current_row + height <= self.total_rows - 2:  # 마지막 2줄 전까지만
                self.map_sections.append((map_type, current_row))
                current_row += height
                last_type = map_type
            else:
                self.map_sections.append(('1_line_road', current_row))
                current_row += 1

    def _initialize_vehicles(self):
        """모든 driveway 줄에 초기 차량 배치"""
        for map_type, start_row in self.map_sections:
            if map_type in ['2_line_driveway', '3_line_driveway']:
                height = self._get_map_height(map_type)
                for row in range(start_row, start_row + height):
                    direction = random.choice(["left", "right"])
                    base_speed = random.randint(2, 3)
                    if row >= 60:
                        base_speed = random.randint(3, 5)
                    
                    # 각 줄마다 3-4대의 차량을 화면 내에 균등하게 배치
                    num_vehicles = random.randint(3, 4)
                    spacing = DISPLAY_WIDTH // num_vehicles
                    positions = []
                    
                    for i in range(num_vehicles):
                        vehicle_type = random.choice(["car1", "car2", "motorcycle1", "motorcycle2"])
                        vehicle_width = CELL_WIDTH * 2 if vehicle_type in ["car1", "car2"] else int(CELL_WIDTH * 1.5)
                        
                        # 최대 10번 시도하여 겹치지 않는 위치 찾기
                        max_attempts = 10
                        found_valid_position = False
                        
                        for _ in range(max_attempts):
                            base_x = i * spacing
                            random_offset = random.randint(-spacing//4, spacing//4)
                            actual_x = base_x + random_offset
                            
                            # 다른 차량과의 겹침 체크
                            valid_position = True
                            for pos in positions:
                                if abs(actual_x - pos['x']) < (vehicle_width + CELL_WIDTH):  # 최소 1칸의 간격
                                    valid_position = False
                                    break
                            
                            if valid_position:
                                found_valid_position = True
                                positions.append({
                                    'x': actual_x,
                                    'width': vehicle_width,
                                    'type': vehicle_type
                                })
                                break
                        
                        if found_valid_position:
                            y = (row - self.current_view_start) * CELL_HEIGHT
                            if vehicle_type in ["motorcycle1", "motorcycle2"]:
                                y += (CELL_HEIGHT - int(CELL_HEIGHT * 0.8)) // 2
                            
                            new_vehicle = Vehicle(actual_x, y, vehicle_type, direction, row, base_speed)
                            self.vehicles.append(new_vehicle)

    def update(self):
        """모든 차량 업데이트"""
        visible_roads = []
        for map_type, start_row in self.map_sections:
            if map_type in ['2_line_driveway', '3_line_driveway']:
                height = self._get_map_height(map_type)
                if (start_row + height > self.current_view_start and 
                    start_row < self.current_view_start + GRID_ROWS):
                    for i in range(height):
                        visible_roads.append(start_row + i)

        for vehicle in self.vehicles:
            vehicle.move()
            
            # 화면을 벗어난 차량 재배치
            if vehicle.direction == "right":
                if vehicle.x > DISPLAY_WIDTH + CELL_WIDTH:
                    same_row_vehicles = [v for v in self.vehicles 
                                       if v.row == vehicle.row and v != vehicle]
                    if same_row_vehicles:
                        leftmost_x = min(v.x for v in same_row_vehicles)
                        vehicle.x = leftmost_x - random.randint(CELL_WIDTH * 4, CELL_WIDTH * 6)
                    else:
                        vehicle.x = -vehicle.width
            else:
                if vehicle.x < -vehicle.width - CELL_WIDTH:
                    same_row_vehicles = [v for v in self.vehicles 
                                       if v.row == vehicle.row and v != vehicle]
                    if same_row_vehicles:
                        rightmost_x = max(v.x for v in same_row_vehicles)
                        vehicle.x = rightmost_x + random.randint(CELL_WIDTH * 4, CELL_WIDTH * 6)
                    else:
                        vehicle.x = DISPLAY_WIDTH + vehicle.width
            
            # y좌표 업데이트
            vehicle.y = (vehicle.row - self.current_view_start) * CELL_HEIGHT
            if vehicle.type in ["motorcycle1", "motorcycle2"]:
                vehicle.y += (CELL_HEIGHT - int(CELL_HEIGHT * 0.8)) // 2

        self.visible_vehicles = [v for v in self.vehicles if v.row in visible_roads]

    def get_visible_map(self):
        visible = []
        for map_type, start_row in self.map_sections:
            if (start_row + self._get_map_height(map_type) > self.current_view_start and 
                start_row < self.current_view_start + GRID_ROWS):
                visible.append((map_type, start_row - self.current_view_start))
        return visible

    def scroll_up(self):
        if self.current_view_start > 0:
            self.current_view_start -= 1
            return True
        return False

    def reset(self):
        self.__init__(self.total_rows)

    def check_collision(self, chick_pos):
        """꼬꼬와 차량의 충돌 체크"""
        chick_rect = {
            'x': chick_pos[0] - CELL_WIDTH//2,
            'y': chick_pos[1] - CELL_HEIGHT//2,
            'width': CELL_WIDTH,
            'height': CELL_HEIGHT
        }
        
        for vehicle in self.visible_vehicles:
            vehicle_rect = {
                'x': vehicle.x,
                'y': vehicle.y,
                'width': vehicle.width,
                'height': vehicle.height
            }
            
            if (chick_rect['x'] < vehicle_rect['x'] + vehicle_rect['width'] and
                chick_rect['x'] + chick_rect['width'] > vehicle_rect['x'] and
                chick_rect['y'] < vehicle_rect['y'] + vehicle_rect['height'] and
                chick_rect['y'] + chick_rect['height'] > vehicle_rect['y']):
                return True
        return False

    def check_ending(self, chick_pos):
        """꼬꼬가 ending 구역에 도달했는지 체크"""
        chick_row = self.current_view_start + chick_pos[1] // CELL_HEIGHT
        return chick_row < 4  # 최상단 4줄 안에 있는지 체크

    @staticmethod
    def _get_map_height(map_type):
        return MAP_LINE_HEIGHTS.get(map_type, 1) 