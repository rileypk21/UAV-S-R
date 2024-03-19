## Final Project

import numpy as np



class Cell:
    def __init__(self, terrain_features, proximity_to_targets, distance_from_last):
        self.terrain_features = terrain_features
        self.proximity_to_targets = proximity_to_targets
        self.distance_from_last = distance_from_last
        self.visited = False

class Drone:
    def __init__(self):
        self.current_cell = None
        self.visited_cells = []

    def calculate_next_cell(self, grid):
        # Implement logic to calculate next cell based on coverage metrics
        pass

    def stay_time(self, grid):
        # Get the terrain feature of the current cell
        row_idx, col_idx = self.current_cell
        terrain_feature = grid[row_idx][col_idx].terrain_features

        # Calculate stay time based on terrain feature
        # This is just an example, adjust the formula as needed
        stay_time = terrain_feature * 10

        return stay_time

class SearchArea:
    def __init__(self, size, num_drones, num_targets):
        self.grid = np.array([[Cell(np.random.choice(range(10)), 0, 0) for _ in range(size)] for _ in range(size)])
        self.drones = [Drone() for _ in range(num_drones)]
        self.targets = [None for _ in range(num_targets)]

        # Randomly place drones on the grid
        for drone in self.drones:
            row_idx = np.random.choice(range(size))
            col_idx = np.random.choice(range(size))
            drone.current_cell = (row_idx, col_idx)

    def distribute_targets(self):
        # Implement logic to distribute targets across the grid
        num_targets = len(self.targets)
        grid = len(self.grid)
        
        for i in range(num_targets):
            row_idx = np.random.choice(range(grid))
            col_idx = np.random.choice(range(grid))
            if (row_idx, col_idx) in self.targets:
                row_idx = np.random.choice(range(grid))
                col_idx = np.random.choice(range(grid))
            self.targets[i] = (row_idx, col_idx)

    def start_search(self):
        # Define the search time based on terrain features
        

        while not self.all_targets_found():
            for drone in self.drones:
                drone.calculate_next_cell(self.grid)

    def all_targets_found(self):
        # Implement logic to check if all targets have been found
        pass

#self.grid[row_idx][col_idx].terrain_features = np.random.randint(1,11)

grid_size = 5
num_drones = 1
num_targets = 25

search_area = SearchArea(grid_size, num_drones, num_targets)
search_area.distribute_targets()
search_area.start_search()


