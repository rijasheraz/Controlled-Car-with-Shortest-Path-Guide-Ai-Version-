# Controlled-Car-with-Shortest-Path-Guide-Ai-Version-
This project has 2 versions. The first is to simply give the shortest path, and the second has an AI version. 

Controlled Car with Shortest Path Guide
This is a Pygame-based interactive car navigation game. The player controls a car on a grid with obstacles, using arrow keys to move toward a goal. The game includes a dynamic shortest-path guide (calculated using Dijkstra's algorithm), and a loading screen with a progress bar for better user experience.

Features:
Dynamic Shortest Path Guidance: Highlights the optimal path to the goal dynamically.
Interactive Gameplay: Move the car using arrow keys while avoiding obstacles.
Randomized Grid: Each game generates a new grid with random obstacles, ensuring a unique experience.
Loading Screen: Includes a title, image, and animated progress bar.
Goal Feedback: Displays a message and move count upon reaching the goal.
Key Technologies:
Pygame: For rendering graphics and handling user input.
Dijkstra's Algorithm: For real-time shortest-path calculations.
Randomized Grid Generation: Ensures solvable paths between car and goal.
Setup:
Install Pygame:
bash
Copy code
pip install pygame
Place required images (car and loading image) in the specified paths in the code or update the paths.
Run the script to start the game.
Controls:
Arrow Keys: Move the car up, down, left, or right.
Customization:
Modify ROWS and COLS to change the grid size.
Adjust obstacle density by tweaking num_obstacles in generate_random_grid().
This repository serves as a foundational project for learning Pygame, pathfinding algorithms, and grid-based game mechanics. 
