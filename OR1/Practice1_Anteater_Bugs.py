import gurobipy as gp
from gurobipy import GRB

# 1. Create new model
model = gp.Model('Anteater Bugs')

# 2. Create Decision variable - Integer
W = model.addVar(vtype=GRB.INTEGER, name='W')
L = model.addVar(vtype=GRB.INTEGER, name='L')

# 3. Set Objective
model.setObjective(W+2*L, GRB.MAXIMIZE)

# 4. Add Constraints

# Malt capacity
model.addConstr(10*W+3*L <= 1000, name='Malt_capa')

# Hops capacity
model.addConstr(20*W+12*L <= 2000, name='Hops_capa')

# Labor capacity
model.addConstr(3*W+3*L <= 1500, name='Labor_capa')

# Nonnegativity
model.addConstr(W >= 0, name='Nonnegativity1')
model.addConstr(L >= 0, name='Nonnegativity2')

# 5.Optimize model
model.optimize()


# Print result
print('==========================================================================')
print(f'Objective: {model.ObjVal}')
print(f'W: {W.X}')
print(f'L: {L.X}')