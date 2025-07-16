from hexalattice.hexalattice import create_hex_grid
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection
from math import sqrt
import random
#from pyomocorridor import selected
from pyomocorrNODE import selected
from hexgridutils import utilities,types,k
from newcorridordata import start,end

class Cell:
    def __init__(self, number, utility, cell_type="unknown"):
        self.number = number
        self.utility = utility
        self.cell_type = cell_type
        self.selected = False

    def __str__(self):
        return f"{self.number:3}" if self.selected else " 0 "


class Board:
    def __init__(self, rows, cols, utilities, types=None):
        self.rows = rows
        self.cols = cols
        self.board = []
        num = 1
        for r in range(rows):
            row = []
            for c in range(cols):
                utility = utilities.get(num, 0)
                cell_type = types.get(num, "unknown") if types else "unknown"
                row.append(Cell(num, utility, cell_type))
                num += 1
            self.board.append(row)

    def update_selection(self, selected_dict):
        for row in self.board:
            for cell in row:
                cell.selected = selected_dict.get(cell.number, 0) == 1
                

    def get_cells_flat(self):
        return [cell for row in self.board for cell in row]




def draw_optimal_corridor(selected, utilities, types):
    b = Board(rows=k, cols=k, utilities=utilities, types=types)
    b.update_selection(selected)
    cells = b.get_cells_flat()

    hex_centers, _ = create_hex_grid(nx=k, ny=k, min_diam=0.2, do_plot=False)
    fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
    patches = []
    facecolors = []
    edgecolors = []
    radius = .2 / sqrt(3)  # ≈ 0.577

    for (x, y), cell in zip(reversed(hex_centers), cells):
    # Determine face color
        if cell.cell_type == "forest":
            facecolor = "darkgreen"
        elif cell.cell_type == "grassland":
            facecolor = "yellowgreen"
        elif cell.cell_type == "farmland":
            facecolor = "sandybrown"
        elif cell.cell_type == "city":
            facecolor = "gray"
        elif cell.cell_type == "habitat":
            facecolor = "lightgreen"
        else:
            facecolor = "white"

        hex_patch = RegularPolygon((x, y), numVertices=6, radius=radius, orientation=0,
                               facecolor=facecolor, edgecolor="black", lw=1.0)
        ax.add_patch(hex_patch)

    # Add label
        ax.text(x, y, f"{cell.number}\n({cell.utility})", ha='center', va='center', fontsize=8)

# Step 2: Overlay selected borders in blue
    for (x, y), cell in zip(reversed(hex_centers), cells):
        if cell.selected:
            outline_patch = RegularPolygon((x, y), numVertices=6, radius=radius, orientation=0,
                                       facecolor='none', edgecolor='red', lw=2.0)
            ax.add_patch(outline_patch)

    ax.set_aspect('equal')
    ax.axis('off')

    x_coords = [x for x, y in hex_centers]
    y_coords = [y for x, y in hex_centers]
    buffer = 0.2
    ax.set_xlim(min(x_coords) - buffer, max(x_coords) + buffer)
    ax.set_ylim(min(y_coords) - buffer, max(y_coords) + buffer)

    plt.title("Optimal Corridor")
    plt.show()


#  Call the function
draw_optimal_corridor(selected, utilities, types)

