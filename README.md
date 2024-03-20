# UAV-S-R
Aero 470 Team Project, search and rescue Biomimetic Algorithm (BA) implementation.
By: Riley Krueger and Joan Brooke

create an agent based Search and Rescue mission to be carried out by multiple drones. Targets are stationary objects to be found.

create a 2D search area that is split into a large grid of cells

drones travel from cell to cell based on a sum coverage metrics. They travel directly to the center of the cell and begin searching, when they are finished, the cell is considered 100% searched.

drones communicate their coverage to eachother so they know not to look in the same cell twice.

Cells that have not been visited contain several coverage metrics: Terrain features (LOS obstructions/obstacles), proximity to targets already found, and distance from the last visited cell.

Cells that have more terrain features take longer to search.

The drone will travel to the cell with the best probability, which is the sum of the coverage metrics. 

When the cell has finished being searched, the drone will update if there were any targets found, which updates the neighboring cells 'proximity to other targets' metric.

Once all targets have been found the simulation is ended.

targets are loosely grouped together across the map.
