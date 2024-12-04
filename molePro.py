import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = 600
GRID_SIZE = 6
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
BACKGROUND_COLOR = (185, 122, 87)  # Light brown
HOLE_COLOR = (139, 69, 19)         # Dark brown
HIT_COLOR = (0, 255, 0)            # Green for hit
MISS_COLOR = (255, 0, 0)           # Red for miss

# Load images
def load_image(image_path, size=None, default_color=None):
    try:
        img = pygame.image.load(image_path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error:
        if default_color:
            img = pygame.Surface((CELL_SIZE, CELL_SIZE))
            img.fill(default_color)
        return img

DIGLETT_IMAGE = load_image("red.png", (CELL_SIZE // 2, CELL_SIZE // 2), (255, 0, 0))  # Red placeholder
#HAMMER_IMAGE = load_image("hammer.png", (CELL_SIZE, CELL_SIZE), (0, 0, 255))  # Blue placeholder

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("AkiHiuKen")
screen.fill(BACKGROUND_COLOR)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.hole_center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        self.has_mole = False
        self.selected_color = None

    def draw(self):
        color = self.selected_color if self.selected_color else HOLE_COLOR
        pygame.draw.circle(screen, color, self.hole_center, CELL_SIZE // 3)
        if self.has_mole:
            mole_pos = (self.hole_center[0] - DIGLETT_IMAGE.get_width() // 2, self.hole_center[1] - DIGLETT_IMAGE.get_height() // 2)
            screen.blit(DIGLETT_IMAGE, mole_pos)

    def toggle_mole(self):
        self.has_mole = not self.has_mole

    def set_hit(self):
        self.selected_color = HIT_COLOR

    def set_miss(self):
        self.selected_color = MISS_COLOR

    def reset_color(self):
        self.selected_color = None


# Create grid of cells
cells = [[Cell(x * CELL_SIZE, y * CELL_SIZE) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

# Game loop variables
running = True
clock = pygame.time.Clock()
mole_timer = 0
#hammer_timer = 0
mole_interval = 1000  # Mole pops every second
#hammer_interval = 1000  # Hammer moves every second
current_hammer_cell = None

while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mole popping logic
    mole_timer += clock.tick(30)  # Get milliseconds passed
    if mole_timer > mole_interval:
        mole_timer = 0
        for row in cells:
            for cell in row:
                cell.has_mole = False
                cell.reset_color()  # Reset the color
        random.choice(random.choice(cells)).toggle_mole()

    # Hammer movement logic
   # hammer_timer += clock.get_time()
    #if hammer_timer > hammer_interval:
     #   hammer_timer = 0
      #  if current_hammer_cell:
       #     current_hammer_cell.reset_color()
        current_hammer_cell = random.choice(random.choice(cells))

        if current_hammer_cell.has_mole:
            current_hammer_cell.set_hit()
        else:
            current_hammer_cell.set_miss()

    # Draw all cells
    for row in cells:
        for cell in row:
            cell.draw()

  # Draw the hammer if it has a target
   # if current_hammer_cell:
    #    screen.blit(HAMMER_IMAGE, (current_hammer_cell.x, current_hammer_cell.y))

    pygame.display.flip()

pygame.quit()
