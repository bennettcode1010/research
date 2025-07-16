from corridordata import ARCS_SET
from pyomocorridor import optimal_nodes






class Arc:
    def __init__(self,i,j):
        self.i = i
        self.j = j


class Node:
    def __init__(self, id):
        self.id = id
        self.neighbors = []


class Graph:
    def __init__(self):
        self.nodes = {}
        self.optimal_nodes = optimal_nodes

    def add_node(self,node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id)

    def add_arc(self,i,j):
        if i in self.nodes and j in self.nodes:
            self.nodes[i].neighbors.append(self.nodes[j])
        


    def make_graph_from_selected(self,arcs,selected_nodes):
        for node_id in selected_nodes:
            self.add_node(node_id)
        for arc in arcs:
            if arc.i in selected_nodes and arc.j in selected_nodes:
                self.add_arc(arc.i,arc.j)

    def print_graph(self):
        for node_id, node in self.nodes.items():
            neighbor_ids = [neighbor.id for neighbor in node.neighbors]
            print(f"Node {node_id}: Neighbors are {neighbor_ids}")

    def check_corridor_validity(self, selected_nodes, start, end):
        visited = {}
        for i in selected_nodes:
            visited[i] = False
        self._dfs_(start, visited)

        path_exists = visited[end]
        fully_connected = all(visited.values())

        if path_exists and fully_connected:
            print(f" Corridor is valid: node {start} connects to node {end} and all selected nodes are connected.")
            if set(selected_nodes) == set(self.optimal_nodes):
                print("User's solution matches the optimal solution.")
                return True
            else:
                print("User's solution is valid but not optimal.")
                return False
        elif not path_exists:
            print(f" Node {end} is not reachable from node {start}.")
        elif not fully_connected:
            print(" Corridor has disconnected parts — not all selected nodes are reachable.")

        return False

    def _dfs_(self, current_id, visited):
        visited[current_id] = True
        for neighbor in self.nodes[current_id].neighbors:
            if neighbor.id in visited and not visited[neighbor.id]:
                self._dfs_(neighbor.id, visited)
        
        

arcs = [Arc(i, j) for i, j in ARCS_SET]

selected_nodes = [1, 8, 9,10,11,12,21,18,24,30]

  
graph = Graph()

graph.make_graph_from_selected(arcs,selected_nodes)

graph.check_corridor_validity(selected_nodes,1,30)





    

