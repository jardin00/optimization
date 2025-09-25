import gurobipy as gp
from gurobipy import GRB

node_name = ["DNN-1","DNN-2","DNN-3","S-1","S-2","London","Beijing"]

arcs = [("DNN-1", "S-1"), ("DNN-1", "London"),
("DNN-2", "S-1"),("DNN-2", "S-2"),
("DNN-3", "S-2"),("DNN-3", "Beijing"),
("S-1", "London"),("S-1", "Beijing"),
("S-2", "London"),("S-2", "Beijing")]

cost = {
    ("DNN-1", "S-1"): 1,
    ("DNN-1", "London"): 0.5,
    ("DNN-2", "S-1"): 2,
    ("DNN-2", "S-2"): 2,
    ("DNN-3", "S-2"): 1.5,
    ("DNN-3", "Beijing"): 0.5,
    ("S-1", "London"): 1,
    ("S-1", "Beijing"): 2,
    ("S-2", "London"): 1,
    ("S-2", "Beijing"): 1
}

capacities = {
    ("DNN-1", "S-1"): 175,
    ("DNN-1", "London"): 50,
    ("DNN-2", "S-1"): 200,
    ("DNN-2", "S-2"): 150,
    ("DNN-3", "S-2"): 100,
    ("DNN-3", "Beijing"): 75,
    ("S-1", "London"): 200,
    ("S-1", "Beijing"): 150,
    ("S-2", "London"): 200,
    ("S-2", "Beijing"): 175
}


# 1. Create new model
model = gp.Model('Network_Flow_management')

# 2. Create Decision variable
x = model.addVars(arcs, vtype=GRB.CONTINUOUS, name='x')

# 3. Set Objective
model.setObjective(gp.quicksum(cost[(i,j)]*x[i,j] for i,j in arcs), GRB.MINIMIZE)

# 4. Add Constraints

# Source (supply) node
model.addConstr(-(x["DNN-1", "London"]+x["DNN-1", "S-1"]) == -200)
model.addConstr(-(x["DNN-2", "S-1"]+x["DNN-2", "S-2"]) == -300)
model.addConstr(-(x["DNN-3", "S-2"]+x["DNN-3", "Beijing"]) == -100)

# Transhipment node
model.addConstr((x["DNN-1", "S-1"]+x["DNN-2", "S-1"])-(x["S-1", "London"]+x["S-1", "Beijing"]) == 0)
model.addConstr((x["DNN-2", "S-2"]+x["DNN-3", "S-2"])-(x["S-2", "London"]+x["S-2", "Beijing"]) == 0)

# Sink (demand) node
model.addConstr(x["DNN-1", "London"]+x["S-1", "London"]+x["S-2", "London"] == 400)
model.addConstr(x["S-1", "Beijing"]+x["S-2", "Beijing"]+x["DNN-3", "Beijing"] == 200)

# Flow capacity
for i,j in arcs:
    model.addConstr(x[i,j] <= capacities[(i,j)])

# Nonnegativity
for i,j in arcs:
    model.addConstr(x[i,j] >= 0)

# Optimize
model.optimize()

# Result
print('\n==========================================================================')
print(f'Objective: {model.ObjVal}')
for i,j in arcs:
    if x[i,j].X > 0:
        print(f'x[{i,j}]: {x[i,j].X}')

#=========================================================================
#PPT에 넣을거
import networkx as nx
import matplotlib.pyplot as plt

# 1. Create a directed graph
G = nx.DiGraph()

# 2. Add nodes and edges to the graph
for i, j in arcs:
    flow = x[i, j].X if x[i, j].X > 0 else 0
    G.add_edge(i, j, flow=flow)

# 3. Define node positions (adjust as necessary for better visualization)
pos = {
    "DNN-1": (0, 3),
    "DNN-2": (0, 2),
    "DNN-3": (0, 1),
    "S-1": (2, 2.5),
    "S-2": (2, 1.5),
    "London": (4, 3),
    "Beijing": (4, 1),
}

# 4. Draw nodes
plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="lightblue")

# 5. Draw edges with arrows
nx.draw_networkx_edges(
    G, 
    pos, 
    edge_color="gray", 
    arrows=True, 
    arrowstyle="-|>", 
    connectionstyle="arc3",  # Slightly curved edges for better visibility
    min_target_margin=15,  # Space between arrow and node
    arrowsize=20  # Arrow size
)

# 6. Add edge labels (flow values only)
edge_labels = {}
for i, j in G.edges:
    flow = G[i][j]["flow"]
    if flow > 0:  # Only display edges with flow
        edge_labels[(i, j)] = f"{flow:.1f}"
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

# 7. Add node labels
nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

# 8. Add title and show
#plt.title("Network Flow Optimization Result (Direction and Flow)", fontsize=14)
plt.axis("off")
#plt.show()
plt.savefig('practice3_network.png', bbox_inches='tight', dpi=300)
