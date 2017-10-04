from geopy.distance import great_circle
from geopy.distance import vincenty
from geopy.distance import distance
from queue import PriorityQueue

class Vertex(object):

    def __init__(self, vertexName, latitude, longitude):
        self.name = vertexName
        self.latitude = latitude
        self.longitude = longitude
        self.adjacent_edges = []
        self.cose = 0
        self.visited = False
        self.prev_vertex = None

class Edge(object):
    def __init__(self, source, target, cost):
        self.source_vertex = source
        self.target_vertex = target
        self.cost = cost

class Graph(object):

    def compute_costs(self):
        for v in self.vertices.values():
            for e in v.adjacent_edges:
                source = (e.source_vertex.latitude, e.source_vertex.longitude)
                target = (e.target_vertex.latitude, e.target_vertex.longitude)
                e.cost = distance(source, target).miles
    
     # Use Prim's algorithm to get a minimum spanning tree.
    def get_min_spanning_tree(self, start_vertex):
        graph = Graph()

        # Add weights and perform Prim's algorithm.
        self.compute_costs()
        self.do_prim(start_vertex)

        # Add all the vertices to the new graph.
        for v in self.vertices.values():
            if v.name not in graph.vertices:
                new_vertex = Vertex(v.name, v.latitude, v.longitude)
                graph.vertices[new_vertex.name] = new_vertex

        # Go through each vertex and add the edge connecting
        # the previous node to the current one.
        for v in self.vertices.values():
            c = 0
            if v.prev_vertex:
                for e in v.adjacent_edges:
                    #Find weight of edge then stop searching.
                    if e.target_vertex == v.prev_vertex:
                        c = e.cost
                        break
                graph.add_edge(v.prev_vertex.name, v.name, c)

        return graph

    # Prim's algorithm to find a minimum spanning tree.
    def do_prim(self, start_vertex):
        queue = PriorityQueue()

        # Set each vertex to infinite cost and not visited.
        for v in self.vertices.values():
            v.cost = float("inf")
            v.visited = False
        # Add the starting point to the queue.
        self.vertices[start_vertex].visited = True
        self.vertices[start_vertex].cost = 0
        queue.put((self.vertices[start_vertex].cost, self.vertices[start_vertex]))
        while not queue.empty():

            # Visit the minimum value.
            cur_vertex = queue.get()[1]
            cur_vertex.visited = True

            #For every edge of every vertex.
            for e in cur_vertex.adjacent_edges:
                e.target_vertex.name
                # If the edge is adjacent and the vertex has not already
                # been visited.
                if not e.target_vertex.visited:

                    # Remove the temporary infinite value of v and
                    # replace it with its actual cost.
                    if e.cost < e.target_vertex.cost:
                        e.target_vertex.cost = e.cost
                        e.target_vertex.prev_vertex = cur_vertex
                    queue.put((e.target_vertex.cost, e.target_vertex))

    #  Add a new edge from u to v. Create new nodes if these nodes don't exist
    #  yet. This method permits adding multiple edges between the same nodes.
    def add_edge(self, nameU, nameV, cost):
        if not self.vertices[nameU]:
            self.vertices[nameU.name] = nameU
        if not self.vertices[nameV]:
            self.vertices[nameV.name] = nameV
        source_vertex = self.vertices[nameU]
        target_vertex = self.vertices[nameV]
        new_edge = Edge(source_vertex, target_vertex, cost)
        source_vertex.adjacent_edges.append(new_edge)

    def _run(self):
        v1 = Vertex('New York City', 40.730610, -73.935242)
        v2 = Vertex('Paris',48.864716, 2.349014)
        v3 = Vertex('Beijing',39.913818 ,116.363625)
        v4 = Vertex('London',51.508530  ,-0.076132)
        self.vertices['New York City'] = v1
        self.vertices['Paris'] = v2
        self.vertices['Beijing'] = v3
        self.vertices['London'] = v4
  
        for source in self.vertices:
            for target in self.vertices:
                if source != target:
                    self.add_edge(source,target,1)
 
        new_graph = self.get_min_spanning_tree(v1.name)
        new_graph.preorder('New York City')

    def print_adj_list(self):
        for u in self.vertices:
            s = u
            s += " -> [ "
            for e in self.vertices[u].adjacent_edges:
                s += e.target_vertex.name
                s += "("
                s += str(e.cost)
                s += ") "
            s += "]"
            print s

    def preorder(self, node):
        self.route.append(node)
        if node.adjacent_edges:
            for e in node.adjacent_edges:
                self.preorder(e.target_vertex)
        

    def __init__(self):
        self.vertices = {}
        self.route = []
    
if __name__ == '__main__':
    Graph()._run()
