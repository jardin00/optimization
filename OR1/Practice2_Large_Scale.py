import random
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt

def create_data(data_size):
    random.seed(42) #Fix random seed
    
    #Create data
    p_j = [random.randint(1,100) for _ in range(data_size)]
    a_1_j= [random.randint(1,100) for _ in range(data_size)]
    a_2_j= [random.randint(1,100) for _ in range(data_size)]
    a_3_j= [random.randint(1,100) for _ in range(data_size)]

    return p_j, a_1_j, a_2_j, a_3_j

def gurobi_model(data_size, p_j, a_1_j, a_2_j, a_3_j, b1, b2, b3):
    # 1. Create new model
    model = gp.Model('Anteater Bugs')

    # 2. Create Decision variable - Integer
    x = model.addVars(data_size, vtype=GRB.INTEGER, name='x')

    # 3. Set Objective
    model.setObjective(gp.quicksum(p_j[j]*x[j] for j in range(data_size)), GRB.MAXIMIZE)

    # 4. Add Constraints

    # Malt capacity
    model.addConstr(gp.quicksum(a_1_j[j]*x[j] for j in range(data_size)) <= b1, name='Malt_capa')

    # Hops capacity
    model.addConstr(gp.quicksum(a_2_j[j]*x[j] for j in range(data_size)) <= b2, name='Hops_capa')

    # Labor capacity
    model.addConstr(gp.quicksum(a_3_j[j]*x[j] for j in range(data_size)) <= b3, name='Labor_capa')

    # Nonnegativity
    for j in range(data_size):
        model.addConstr(x[j] >= 0, name='Nonnegativity')

    # 5.Optimize model
    model.optimize()

    # Print result
    print('==========================================================================')
    print(f'Objective: {model.ObjVal}')

    return model.Runtime

def plot_runtime_graph(runtime_dict):
    data_sizes = list(runtime_dict.keys())
    runtimes = list(runtime_dict.values())

    #Plot the data
    plt.figure(figsize=(8,5))
    plt.plot(data_sizes,runtimes,marker='o')
    
    #Add title and label
    plt.title('Computation Time')
    plt.xlabel('Data Size')
    plt.ylabel('Runtime (seconds)')
    
    #Set xticks to match the data sizes
    plt.xticks(data_sizes)
    
    #display the graph
    plt.grid(True)
    plt.show()

def main():
    data_sizes = [100,500,1000,10000] #List of data sizes to test
    b1, b2, b3 = 1000, 2000, 1500
    runtime_dict ={} #Dictionary to store computation times for each data size

    for data_size in data_sizes:
        p_j, a_1_j, a_2_j, a_3_j = create_data(data_size)
        gurobi_runtime = gurobi_model(data_size, p_j, a_1_j, a_2_j, a_3_j, b1, b2, b3)
        runtime_dict[data_size] = gurobi_runtime

    plot_runtime_graph(runtime_dict)

    
if __name__=="__main__":
    main()