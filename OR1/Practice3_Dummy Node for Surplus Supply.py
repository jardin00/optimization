import gurobipy as gp
from gurobipy import GRB

node_name = [1,2,3,4,5]

arcs = [(1,2),(1,4),(1,5),(2,4),(3,1),(3,5),(4,3)]

cost = {(1,2):9,(1,4):4,(1,5):0,(2,4):7,(3,1):3,(3,5):0,(4,3):-2}

# 1. Create new model
model = gp.Model('Dummy Node for Surplus Supply')

# 2. Create Decision variable
x = model.addVars(arcs, vtype=GRB.CONTINUOUS, name='x')

# 3. Set Objective
model.setObjective(gp.quicksum(cost[(i,j)]*x[i,j] for i,j in arcs), GRB.MINIMIZE)

# 4. Add Constraints
model.addConstr(x[3,1]-(x[1,2]+x[1,4]+x[1,5]) == -50)
model.addConstr(x[1,2]-x[2,4] == 28)
model.addConstr(x[4,3]-(x[3,1]+x[3,5]) == -90)
model.addConstr((x[1,4]+x[2,4])-x[4,3] == 52)
model.addConstr(x[1,5]+x[3,5] == 60)

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
    1: (0, 3),
    2: (3, 5),
    3: (3, 2),
    4: (6, 3),
    5: (0, 0)}

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
plt.savefig('practice3_dummy.png', bbox_inches='tight', dpi=300)
