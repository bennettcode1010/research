from hexalattice.hexalattice import create_hex_grid
from math import sqrt
import random
from newcorridordata import start, end

random.seed(42)

k=12


# Define type hubs
type_hubs = {
    10: "forest",
    15: "grassland",
    47: "farmland",
    28: "city",
    61: "forest"
}
amounts_types = {
    "forest":  20,
    "grassland": 20,
    "farmland": 15,
    "city": 9
}


def get_hex_centers(k):
    hex_centers, _ = create_hex_grid(nx=k, ny=k, min_diam=0.2, do_plot=False)
    return hex_centers

centers = get_hex_centers(12)
cell_coords = {
    i: (float(coord[0]), float(coord[1]))
    for i, coord in enumerate(centers, start=1)}

def get_distances(cell_coords, type_hubs):
    all_distances = {}

    for num, coord in cell_coords.items():
        distances = []
        for index, t in type_hubs.items():
            x1, y1 = coord
            x2, y2 = cell_coords[index]
            distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
            distances.append((t, distance))
        
        all_distances[num] = distances  # store distances for this cell

    return all_distances



def get_probabilities_by_cells(cell_coords,type_hubs):

    random_type_assignments = {}

    for hub_id, t in type_hubs.items():
        random_type_assignments[hub_id] = t

    random_type_assignments[1] = "habitat"
    random_type_assignments[64] = "habitat"
    all_distances = get_distances(cell_coords, type_hubs)

    for cell, dist_list in all_distances.items():
        if cell in type_hubs or cell in [1, 64]:
            continue

        # Step 1: Separate types and numeric distances
        types = [t for t, _ in dist_list]
        distances = [d for _, d in dist_list]

        # Normalize distances and invert (closer = higher weight)
        normed = [d / sum(distances) for d in distances]
        inv_probs = [1 / d for d in normed]
        sum_inv = sum(inv_probs)
        probabilities = [ip / sum_inv for ip in inv_probs]

        
        chosen_type = random.choices(types, weights=probabilities, k=1)[0]
        random_type_assignments[cell] = chosen_type
    sorted_assignments = dict(sorted(random_type_assignments.items()))
    return sorted_assignments
'''
amounts_types = {
    "forest":  20,
    "grassland": 20,
    "farmland": 15,
    "city": 9
}
'''


amounts_types = {
    "forest":  60,
    "grassland": 40,
    "farmland": 30,
    "city": 15
}
def assign_type_by_closest(cell_coords, type_hubs, amounts_types):
    type_assignments = {}
    # Assign known types
    for i in start + end:
        type_assignments[i] = "habitat"

    for hub_id, t in type_hubs.items():
        type_assignments[hub_id] = t
        amounts_types[t] -= 1

    all_distances = get_distances(cell_coords, type_hubs)

    for cell, dist_list in all_distances.items():
        if cell in type_assignments:
            continue
        closest_type = None
        smallest_distance = 1000
        for t, d in dist_list:
            if amounts_types[t] > 0:
                if d < smallest_distance:
                    smallest_distance = d
                    closest_type = t
        if closest_type is not None:
            type_assignments[cell] = closest_type
            amounts_types[closest_type] -= 1
        else:
            type_assignments[cell] = "unassigned"

    cell_types = dict(sorted(type_assignments.items()))
    return cell_types
            


def generate_utilities(cell_types):
    utilities = {}
    for i, t in cell_types.items():
        if t == "forest":
            utilities[i] = random.randint(80, 100)
        elif t == "grassland":
            utilities[i] = random.randint(60, 80)
        elif t == "farmland":
            utilities[i] = random.randint(40, 60)
        elif t == "city":
            utilities[i] = random.randint(0, 20)
        else:
            utilities[i] = 0
    return utilities


# Generate type and utility assignments
#types = get_probabilities_by_cells(cell_coords, type_hubs)
types = assign_type_by_closest(cell_coords, type_hubs, amounts_types)
utilities = generate_utilities(types)








    
