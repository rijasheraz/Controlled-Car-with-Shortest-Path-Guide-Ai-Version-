import pygame
import heapq
import random
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Controlled Car with Shortest Path Guide")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Grid settings
GRID_SIZE = 20
ROWS, COLS = 30, 40  # Create a 30x40 grid

# Car and Goal positions
car_pos = [1, 1]
goal_pos = (28, 38)

# Define directions for movement
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Grid as 2D array filled with zeros (0 = empty, 1 = wall)
grid = [[0] * COLS for _ in range(ROWS)]

# Font for displaying messages
font = pygame.font.Font(None, 48)

# Move counter
move_count = 0

# Function to draw the grid, car, and goal
def draw(paths, goal_reached=False):
    screen.fill(WHITE)
    if not goal_reached:
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if grid[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

        # Draw the car
        car_image = pygame.image.load("D:\\ai\\car game\\images.png")
        car_image = pygame.transform.scale(car_image, (GRID_SIZE, GRID_SIZE))
        screen.blit(car_image, (car_pos[1] * GRID_SIZE, car_pos[0] * GRID_SIZE))

        # Draw the goal
        pygame.draw.rect(screen, GREEN, (goal_pos[1] * GRID_SIZE, goal_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the shortest path guides
        for path in paths:
            for pos in path:
                if pos != tuple(car_pos):  # Skip drawing at the car's starting position
                    pygame.draw.rect(screen, BLUE, (pos[1] * GRID_SIZE + 5, pos[0] * GRID_SIZE + 5, GRID_SIZE - 10, GRID_SIZE - 10))
    else:
        # Display message if goal is reached
        message = "You reached the goal!"
        text = font.render(message, True, BLACK)
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

        # Display total moves after goal is reached
        move_message = f"Moves: {move_count}"
        move_text = font.render(move_message, True, BLACK)
        screen.blit(move_text, (10, 10))  # Display at the top-left corner

# Modified Dijkstra's Algorithm to find all shortest paths
def dijkstra(start, goal):
    queue = [(0, start)]
    distances = {start: 0}
    previous_nodes = {start: []}  # Track multiple paths

    while queue:
        dist, current = heapq.heappop(queue)

        if current == goal:
            return reconstruct_paths(previous_nodes, goal)

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and grid[neighbor[0]][neighbor[1]] == 0:
                new_dist = dist + 1
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous_nodes[neighbor] = [current]
                    heapq.heappush(queue, (new_dist, neighbor))
                elif new_dist == distances[neighbor]:
                    previous_nodes[neighbor].append(current)

    return []

def reconstruct_paths(previous_nodes, goal):
    paths = []
    def build_path(node):
        path = []
        while node is not None:
            path.append(node)
            node = previous_nodes[node][0] if previous_nodes[node] else None
        return path[::-1]

    paths.append(build_path(goal))
    return paths

# Function to generate random grid with obstacles
def generate_random_grid():
    global grid, car_pos, goal_pos

    grid = [[0] * COLS for _ in range(ROWS)]  # Reset the grid

    # Randomly place obstacles
    num_obstacles = (ROWS * COLS) // 4  # 25% of the grid will be obstacles
    for _ in range(num_obstacles):
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if (row, col) != tuple(car_pos) and (row, col) != goal_pos:
            grid[row][col] = 1  # Mark as an obstacle

    # Ensure there is always a path
    while not is_path_exists(car_pos, goal_pos):
        # Re-generate if there's no path
        grid = [[0] * COLS for _ in range(ROWS)]
        for _ in range(num_obstacles):
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if (row, col) != tuple(car_pos) and (row, col) != goal_pos:
                grid[row][col] = 1

# Function to check if there is a path between car and goal
def is_path_exists(start, goal):
    visited = [[False] * COLS for _ in range(ROWS)]
    queue = [start]
    visited[start[0]][start[1]] = True

    while queue:
        current = queue.pop(0)
        if current == goal:
            return True
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS:
                if not visited[neighbor[0]][neighbor[1]] and grid[neighbor[0]][neighbor[1]] == 0:
                    visited[neighbor[0]][neighbor[1]] = True
                    queue.append(neighbor)

    return False

# Loading page function with image, title, and progress bar
def loading_page():
    screen.fill(WHITE)

    # Title Text
    font = pygame.font.SysFont("timesnewroman", 30,bold=True)  # Font size 48
    title_text = font.render("Controlled Car with Shortest Path Guide", True, BLACK)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

    # Loading Image (make it larger)
    loading_image = pygame.image.load("D:\\ai\\car game\\loading_image.png")  # Replace with your image path
    loading_image = pygame.transform.scale(loading_image, (600, 400))  # Make the image bigger
    screen.blit(loading_image, (screen.get_width() // 2 - 250, screen.get_height() // 2 - 150))  # Adjust position

    # Progress bar at the bottom
    bar_width = 800
    bar_height = 30
    progress_bar_rect = pygame.Rect((screen.get_width() // 2 - bar_width // 2), screen.get_height() - bar_height - 20, bar_width, bar_height)
    pygame.draw.rect(screen, BLACK, progress_bar_rect, 2)  # Outline of the progress bar
    pygame.draw.rect(screen, GREEN, (progress_bar_rect.x, progress_bar_rect.y, 0, bar_height))  # Fill the progress bar

    pygame.display.flip()
    total_steps = 100
    for i in range(total_steps):
        # Animate progress bar
        pygame.draw.rect(screen, BLUE, (progress_bar_rect.x, progress_bar_rect.y, (i * bar_width) // total_steps, bar_height))
        pygame.display.flip()
        pygame.time.delay(30)  # Delay to simulate loading process (adjust as needed)

    time.sleep(1)  # Wait 1 second after loading completes
    
# Main loop
running = True
goal_reached = False
generate_random_grid()  # Generate a new grid at the start

loading_page()  # Show loading page with image, title, and progress bar

while running:
    # Calculate the shortest path(s) from car position to goal if not reached
    paths = dijkstra(tuple(car_pos), goal_pos) if not goal_reached else []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not goal_reached:
            if event.key == pygame.K_UP and car_pos[0] > 0 and grid[car_pos[0] - 1][car_pos[1]] == 0:
                car_pos[0] -= 1
                move_count += 1  # Increment move count
            elif event.key == pygame.K_DOWN and car_pos[0] < ROWS - 1 and grid[car_pos[0] + 1][car_pos[1]] == 0:
                car_pos[0] += 1
                move_count += 1  # Increment move count
            elif event.key == pygame.K_LEFT and car_pos[1] > 0 and grid[car_pos[0]][car_pos[1] - 1] == 0:
                car_pos[1] -= 1
                move_count += 1  # Increment move count
            elif event.key == pygame.K_RIGHT and car_pos[1] < COLS - 1 and grid[car_pos[0]][car_pos[1] + 1] == 0:
                car_pos[1] += 1
                move_count += 1  # Increment move count

    # Check if the car has reached the goal
    if tuple(car_pos) == goal_pos:
        goal_reached = True

    # Draw everything
    draw(paths, goal_reached)
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
