# Display settings
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240

# Grid settings
GRID_ROWS = 7
GRID_COLS = 7
CELL_WIDTH = DISPLAY_WIDTH // GRID_COLS
CELL_HEIGHT = DISPLAY_HEIGHT // GRID_ROWS

# Map settings
MAP_TYPES = [
    '1_line_road', '2_line_road',
    '2_line_driveway', '3_line_driveway',
    '1_line_river', '2_line_river',
    '4_line_background'
]

MAP_LINE_HEIGHTS = {
    '1_line_road': 1,
    '2_line_road': 2,
    '2_line_driveway': 2,
    '3_line_driveway': 3,
    '1_line_river': 1,
    '2_line_river': 2,
    '4_line_background': 4
}

# GPIO Pin settings
PIN_DC = 25      # Data/Command
PIN_CS = 0       # Chip Select (CE0)
PIN_RST = 24     # Reset
PIN_BACKLIGHT = 26

# Button GPIO pins
PIN_BTN_L = 27
PIN_BTN_R = 23
PIN_BTN_U = 17
PIN_BTN_D = 22
PIN_BTN_5 = 5
PIN_BTN_6 = 6 