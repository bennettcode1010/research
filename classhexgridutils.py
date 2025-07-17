from hexalattice.hexalattice import create_hex_grid
from math import sqrt
import random
from newcorridordata import start, end, k

random.seed(42)

# === Hub class ===
class Hub:
    def __init__(self, hub_id, land_type, coords, amount):
        self.id = hub_id
        self.land_type = land_type
        self.coords = coords  # (x, y)
        self.amount_remaining = amount

    def get_distance(self, other_coords):
        x1, y1 = self.coords
        x2, y2 = other_coords
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def is_available(self):
        return self.amount_remaining > 0


# === Setup ===
def get_hex_centers(k):
    hex_centers, _ = create_hex_grid(nx=k, ny=k, min_diam=0.2, do_plot=False)
    return hex_centers

centers = get_hex_centers(k)
cell_coords = {
    i: (float(coord[0]), float(coord[1]))
    for i, coord in enumerate(centers, start=1)
}

# === Type hub definitions ===
type_hubs_raw = {
    10: ("forest", 20),
    15: ("grassland", 20),
    47: ("farmland", 15),
    28: ("city", 9),
    61: ("forest", 40),
    103: ("city", 11)
}

type_hubs = [
    Hub(hub_id, land_type, cell_coords[hub_id], amount)
    for hub_id, (land_type, amount) in type_hubs_raw.items()
]


# === Assign land types to cells based on closest hub ===
def assign_type_by_closest(cell_coords, type_hubs):
    type_assignments = {}

    # Assign habitat types to start and end cells
    for i in start + end:
        type_assignments[i] = "habitat"

    # Assign each hub its type and reduce available amount
    for hub in type_hubs:
        type_assignments[hub.id] = hub.land_type
        hub.amount_remaining -= 1

    # Assign remaining cells based on closest available hub
    for cell, coords in cell_coords.items():
        if cell in type_assignments:
            continue

        min_distance = 1000
        closest_hub = None

        for hub in type_hubs:
            if hub.is_available():
                dist = hub.get_distance(coords)
                if dist < min_distance:
                    min_distance = dist
                    closest_hub = hub

        if closest_hub:
            type_assignments[cell] = closest_hub.land_type
            closest_hub.amount_remaining -= 1
        else:
            type_assignments[cell] = "unassigned"

    return dict(sorted(type_assignments.items()))


# === Generate utility scores ===
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


# === Main execution ===
types = assign_type_by_closest(cell_coords, type_hubs)
utilities = generate_utilities(types)