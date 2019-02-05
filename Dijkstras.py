from collections import defaultdict, deque, OrderedDict
import sys
import pprint

# Creating a class for adding nodes, vertices, and edge weights for a graph
class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.costs = {}
# Function to add nodes to graph
    def add_node(self, value):
        self.nodes.add(value)

# Function to add edges to graph
    def add_edge(self, from_node, to_node, cost):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.costs[(from_node, to_node)] = cost  # value of node from one node to another
        self.costs[(to_node, from_node)] = cost  # to make the graph undirected


# Function for dijkstra's algorithm
def djk(graph, initial):
    visited = {initial: 0}  # Initialize visited
    path = {}  # Initialize path

    nodes = set(graph.nodes) # taking nodes from graph

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:  # no nodes are visited
                    min_node = node  # set 1st node traversed as min node with 
                elif visited[node] < visited[min_node]:  # if iterated node is less than node in visited list
                    min_node = node  # set iterated node to min_node
        if min_node is None:  # break loop is no nodes present
            break

        nodes.remove(min_node)  # Remove min node from list
        present_weight = visited[min_node]  # use of weight of first node in min node

        for edge in graph.edges[min_node]:  # use of exception handling while dealing with weights
            try:
                weight = present_weight + graph.costs[(min_node, edge)]  # add weights to already existing path
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight  # weights of edges in path
                path[edge] = min_node  # nodes of edges path

    return visited, path


# defining a shortest path function
def shrt_pth(orgn, dstn, graph):
    visited, paths = djk(graph, orgn)
    fl_pth = deque()  # initializing deque as a double ended list

    _dstn = paths[dstn]

    while _dstn != orgn:  # checking nodes other than source node itself
        fl_pth.appendleft(_dstn)  # adding other shortest nodes to path till we 
        _dstn = paths[_dstn]  # adding distances

    fl_pth.appendleft(orgn)
    fl_pth.append(dstn)

    return list(fl_pth), visited[dstn]  # Returns the full shortest path as well as the distance of that particular path


# Creating the adjacency matrix
def adj_mat(graph):
    nodes = set(graph.nodes)
    lis = []
    edges = {}
    mat = [[0 for x in range(len(nodes))] for y in range(len(nodes))] # Defining matrix for nodes
    edges = graph.edges

    nodes = sorted(nodes)  # sorting nodes in a order (A-Z)
    i = 0
    edges = OrderedDict(sorted(edges.items())) # using dictionary to store edge values between nodes
    for p, lis in edges.items():
        j = 0
        lis = sorted(lis)
        for n in nodes:
            for x in lis:  # Adding edge values to respective matrix cells
                if x == n:
                    mat[i][j] = graph.costs[(p, x)]
            j = j+1  # incrementing to next cell
        i = i+1  # incrementing to next cell

    pprint.pprint(mat)  # printing adjacency matrix as sparse matrix

# Main function
if __name__ == '__main__':
    graph = Graph() # initializing graph Graph class
    g = {}
    with open('input.txt', 'r') as f: # taking input from text file
        la = []
        lb = []
        for ll in f:
            n1, n2, d = ll.rstrip('\n',).split(',')  # splitting input bases on comma
            g.setdefault(n1, []).append((n2, d))  # assigning 1 character as 1st node of edge, 2nd character as 2nd node
            la.append(n1)  # creating a list of all first nodes
            lb.append(n2)   # creating a list of all second nodes

ml = sorted(la + lb)
myset = sorted(set(ml))
# Adding nodes to our graph
for i in range(len(myset)):
    graph.add_node(myset[i])

with open('input.txt', 'r') as ff:
    for l in ff:
        n11, n21, d1 = l.rstrip('\n', ).split(',')
        g.setdefault(n11, []).append((n21, d1))
        graph.add_edge(n11, n21, int(d1))  # Adding edges to our graph with edge weights

print(" Adjacency Matrix ")
adj_mat(graph)  # printing adjacency matrix

print('The shortest path from source node A to other nodes in graph:')  # printing shortest path from A as source
for i in range(len(myset)):
    ds = myset[i]
    if ds != 'A':
        print('A', "->", ds, shrt_pth('A', ds, graph))  # using shortest path functions

print("Please enter the Source node in CAPS")  # Asking for user input
s = input()

# printing shortest path source node to other nodes in graph
print('The shortest path from source to other nodes in graph:')
for i in range(len(myset)):
    ds = myset[i]
    if s[0] != ds:
        print(s[0], "->", ds, shrt_pth(s[0], ds, graph))  # using shortest path function
