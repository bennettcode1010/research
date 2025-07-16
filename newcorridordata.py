
import random

k=12

NODES = list(range(1,k**2 +1))

B= 20

start = [1,2,13]
end = [132,143,144]
N_s= [2,13]
N_e= [132,143]
random.seed(42)

def make_square_hex_arcs(k):
    arc_list = []
    for j in range(0, k-1):
        if j % 2 == 0:
            for i in range(1+j*k,k+1+j*k):
                arc_list.append((i,i+k))
                if i != k+j*k:
                    arc_list.append((i,i+1))
                if i != k*j+1:
                    arc_list.append((i,i+k-1))
        else:
            for i in range(1+j*k,k+1+j*k):
                arc_list.append((i,i+k))
                if i != k+j*k:
                    arc_list.append((i,i+1))
                    arc_list.append((i,i+k+1))
                    
    for i in range((k-1)*k+1,k**2):
        arc_list.append((i,i+1))
       
    reversed_arcs = [(j, i) for (i, j) in arc_list if j not in end]
    arc_list.extend(reversed_arcs)
    for j in N_s:
        arc_list.append((0, j))

    return arc_list


ARCS = make_square_hex_arcs(k)


def make_neighbors():
    neighbors = {i: [] for i in range(1, 65)}  # Start each key with an empty list

    for i, j in ARCS:
        neighbors[i].append(j)
        neighbors[j].append(i)
    return neighbors

#need to figure out how to create clusters

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







