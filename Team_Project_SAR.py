## FinalProject

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from collections import deque
import time

class Cell:
    def __init__(self, terrain_features, proximity_to_targets, distance_from_last):
        self.terrain_features = terrain_features
        self.proximity_to_targets = proximity_to_targets
        self.distance_from_last = distance_from_last
        self.visited = False

class Drone:
    def __init__(self):
        self.current_cell = None
        self.stay_time = []


class SearchArea:
    def __init__(self, size, num_drones, num_targets):
        # Initialize all cells with a terrain value of -1
        self.grid = np.array([[Cell(-1, 0, 0) for _ in range(size)] for _ in range(size)])
        self.drones = [Drone() for _ in range(num_drones)]
        self.targets = [None for _ in range(num_targets)]
        self.visited_cells = []
        self.found_targets = []

        # Assign the maximum terrain value to a few cells
        max_value = 4
        max_cells = [(np.random.choice(range(size)), np.random.choice(range(size))) for _ in range(3)]
        for row, col in max_cells:
            self.grid[row][col].terrain_features = max_value

        # Assign terrain values to the rest of the cells
        self.assign_terrain_values(max_cells, max_value)

        # Randomly place drones on the grid
        for drone in self.drones:
            row_idx = np.random.choice(range(size))
            col_idx = np.random.choice(range(size))
            drone.current_cell = (row_idx, col_idx)
            self.visited_cells.append((row_idx, col_idx))

    def assign_terrain_values(self, max_cells, max_value):
        from collections import deque
        queue = deque(max_cells)

        while queue:
            cell = queue.popleft()
            row, col = cell
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]) and self.grid[new_row][new_col].terrain_features == -1:
                    self.grid[new_row][new_col].terrain_features = self.grid[row][col].terrain_features - 1
                    queue.append((new_row, new_col))

    def distribute_targets(self):
        # Implement logic to distribute targets across the grid
        num_targets = len(self.targets)
        grid = len(self.grid)
        
        # Randomly place the first target on the grid
        row_idx = np.random.choice(range(grid))
        col_idx = np.random.choice(range(grid))
        self.targets[0] = (row_idx, col_idx)

        # Place the remaining targets within a certain distance from the previous target
        for i in range(num_targets-1):
            i += 1
            prev_target = self.targets[i-1]
            row_idx = prev_target[0] + np.random.choice(range(-3, 3))
            col_idx = prev_target[1] + np.random.choice(range(-3, 3))

            # Ensure that the target is within the grid and not already occupied by another target
            row_idx = max(0, min(row_idx, grid - 2))
            col_idx = max(0, min(col_idx, grid - 2))
            while (row_idx, col_idx) in self.targets:
                row_idx = prev_target[0] + np.random.choice(range(-2, 2))
                col_idx = prev_target[1] + np.random.choice(range(-2, 2))
                row_idx = max(0, min(row_idx, grid - 2))
                col_idx = max(0, min(col_idx, grid - 2))
            self.targets[i] = (row_idx, col_idx)

    def start_search(self):
        start_time = time.time()
        while not self.all_targets_found():
            for drone in self.drones:
                # Calculate the next cell for each drone
                drone.current_cell = self.calculate_next_cell(self.grid, drone)
            # Update the search area
            self.visual()

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Time taken to find all targets: {elapsed_time} seconds")

    def all_targets_found(self):
        # Implement logic to check if all targets have been found
        for target in self.targets:
            if not any(target in self.visited_cells for drone in self.drones):
                return False
        return True

    def calculate_next_cell(self, grid, drone):
        # Implement logic to calculate next cell based on coverage metrics
        
        next_cell = []
        row_idx, col_idx = drone.current_cell
        self.visited_cells.append((row_idx, col_idx))
        #grid[row_idx][col_idx].visited = True        
        # Get the stay time for the current cell
        drone.stay_time = stay_time(self, grid, drone.current_cell)

        if drone.stay_time > 0:
            # If the stay time is greater than 0, the drone stays in the same cell
            next_cell = (row_idx, col_idx)

            # Update the terrain features of the current cell
            self.grid[row_idx][col_idx].terrain_features -= 1
            return next_cell
        else:
            # If the stay time is 0, the drone moves to the next cell
            # Implement logic to calculate the next cell based on coverage metrics            
            # Define the directions for the neighbors (up, down, left, right)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]            
            # Initialize the fitness scores dictionary
            fitness_scores = {}            
            # Iterate over the neighbors and their neighbors
            for i, (dx, dy) in enumerate(directions):
                for nx, ny in directions:
                    # Calculate the coordinates of the neighbor's neighbor
                    nnx, nny = row_idx + dx + nx, col_idx + dy + ny                    
                    # Check if the coordinates are within the grid
                    if 0 <= nnx < len(grid) and 0 <= nny < len(grid[0]):
                        # Calculate the fitness score
                        fitness_score = grid[nnx][nny].terrain_features*0.25  # Add the terrain features
                        fitness_score -= abs(nnx - row_idx) + abs(nny - col_idx)  # Subtract the distance                    
                        
                        # Check if there are any found targets
                        if self.found_targets:
                            # Calculate the distance to the nearest found target
                            nearest_target = min(self.found_targets, key=lambda target: abs(target[0] - row_idx) + abs(target[1] - col_idx))
                            distance_to_nearest_target = abs(nearest_target[0] - nnx) + abs(nearest_target[1] - nny)

                            # Subtract the distance to the nearest found target from the fitness score
                            fitness_score -= distance_to_nearest_target

                        # Store the fitness score in the dictionary
                        fitness_scores[(nnx, nny)] = fitness_score            
                        # Sort the fitness scores in descending order
            sorted_cells = sorted(fitness_scores.items(), key=lambda item: item[1], reverse=True)

            # Iterate through the sorted cells until we find one that hasn't been visited yet
            next_cell = None
            for cell, _ in sorted_cells:
                if cell not in self.visited_cells:
                    next_cell = cell
                    break

        # If no next cell was found in the sorted cells, select the nearest cell to average location of all drones to prevent the drone from getting stuck
        if next_cell is None:
            avg_row = sum(drone.current_cell[0] for drone in self.drones) / len(self.drones)
            avg_col = sum(drone.current_cell[1] for drone in self.drones) / len(self.drones)

            unvisited_cells = []
            for row in range(len(self.grid)):
                for col in range(len(self.grid[0])):
                    cell = (row, col)
                    if cell not in self.visited_cells:
                        unvisited_cells.append(cell)

            nearest_cell = min(unvisited_cells, key=lambda cell: ((cell[0] - avg_row) ** 2 + (cell[1] - avg_col) ** 2) ** 0.5)

            # Now nearest_cell is the nearest cell to the average location of found cells
            next_cell = nearest_cell    
            
        
        # Update the current cell for the drone
        if next_cell is not None:
            self.visited_cells.append(next_cell)
            return next_cell
    
    def visual(self):

        # Turn on interactive mode
        plt.ion()

        # Clear the previous visualization
        plt.clf()

        # Create a grid to visualize the search area
        grid_array = np.array([[cell.terrain_features for cell in row] for row in self.grid])

        # Create the initial visualization
        plt.imshow(grid_array, cmap='terrain')

        for target in self.targets:
            row_idx, col_idx = target
            plt.scatter(col_idx, row_idx, color='red', s=100)  # Use a red icon for the targets
        for drone in self.drones:
            row_idx, col_idx = drone.current_cell
            plt.scatter(col_idx, row_idx, color='magenta', marker='+', s=500)

            # If the current cell of the drone is a target, remove it from the list of targets
            if drone.current_cell in self.targets:
                self.targets.remove(drone.current_cell)
                self.found_targets.append(drone.current_cell)
        
        plt.title('Drone Search and Rescue Simulation')  # Add title

        # Add legend
        # You need to have some labeled plot elements to create a legend
        # Here's an example of creating a legend for three labeled plot elements
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='magenta', edgecolor='magenta', label='Drone'),
                           Patch(facecolor='red', edgecolor='red', label='Target')]
        plt.legend(handles=legend_elements, bbox_to_anchor=(1.05,1), loc='best')
        
        # Add colorbar
        #cbar = plt.colorbar()
        #cbar.set_label('Color Label', rotation=270, labelpad=15)
        
        # Draw the current figure and show it
        plt.draw()
        plt.show()

        # Pause for a short duration to observe the visualization
        plt.pause(0.75)



def stay_time(self, grid, current_cell):
    # Get the terrain feature of the current cell
    row_idx, col_idx = current_cell
    terrain_feature = grid[row_idx][col_idx].terrain_features

    # Calculate stay time based on terrain feature
    # This is just an example, adjust the formula as needed
    stay_time = terrain_feature

    return stay_time




# Usage
grid_size = int(input("Enter the size of the grid: "))
num_drones = int(input("Enter the number of drones: "))
num_targets = int(input("Enter the number of targets: "))

search_area = SearchArea(grid_size, num_drones, num_targets)
# Distribute targets across the search area
search_area.distribute_targets()
# Visualize the initial search area
search_area.visual()
# Start the search
search_area.start_search()
