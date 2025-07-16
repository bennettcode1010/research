import pyomo.environ as pyo
from newcorridordata import ARCS, NODES, B, N_s,N_e,start,end
from hexgridutils import utilities


#ARCS_SET = [(arc['i'], arc['j']) for arc in ARCS.values()]
ARCS_SET = ARCS

model = pyo.ConcreteModel()

#Sets---
model.ARCS = pyo.Set(dimen=2,initialize=ARCS_SET)

model.NODES = pyo.Set(initialize=NODES)

#Params---

model.B = pyo.Param(mutable = True,initialize = B + 2)

model.u = pyo.Param(model.NODES, initialize = utilities)

model.N_s = pyo.Set(initialize=N_s)
model.N_e = pyo.Set(initialize=N_e)

#Vars---

model.x = pyo.Var(model.ARCS, within=pyo.NonNegativeReals)
model.y = pyo.Var(model.NODES, within=pyo.Binary)

#Obj

model.obj = pyo.Objective(expr = sum(model.u[n] * model.y[n] for n in model.NODES), sense='maximize')

#Constraints

def budget_limit_rule(model):
    return sum(model.x[i,j] for (i,j) in model.ARCS if i == 0) <= model.B

model.BudgetLimit = pyo.Constraint(rule = budget_limit_rule)

# ASKABOUTTHIS def inject_only_to_start_rule(model):
    #expr = sum(model.x[i, j] for (i, j) in model.ARCS if i == 0 and j not in model.start)
    #return expr == 0

#model.InjectOnlyToStart = pyo.Constraint(rule = inject_only_to_start_rule)

def flow_balance_rule(model,n):
    inflow = sum(model.x[i,j] for (i,j) in model.ARCS if j == n)
    outflow = sum(model.x[i,j] for (i,j) in model.ARCS if i == n)
    return inflow - outflow == model.y[n]

model.FlowBalance = pyo.Constraint(model.NODES, rule = flow_balance_rule)

def flow_if_selected_rule(model,i,j):
    return model.x[i,j] <= model.B * model.y[j]

model.FlowIfSelected = pyo.Constraint(model.ARCS, rule = flow_if_selected_rule)
'''
def no_outflow_from_end_rule(model,n):
    return sum(model.x[i,j] for (i,j) in model.ARCS if i == n) == 0

model.NoOutflowFromEnd = pyo.Constraint(model.end, rule = no_outflow_from_end_rule)
'''

def must_select_one_start(model):
    return sum(model.y[n] for n in model.N_s) == 1

model.MustSelectOneStart= pyo.Constraint(rule = must_select_one_start)


def must_select_one_end(model):
    return sum(model.y[n] for n in model.N_e) == 1

model.MustSelectOneEnd= pyo.Constraint(rule = must_select_one_end)


# Solve the model using GLPK
solver = pyo.SolverFactory('glpk')
results = solver.solve(model)

# Print objective value
print("\nObjective Value:", pyo.value(model.obj))



selected = {n: 0 for n in model.NODES}

# Mark node j as selected if any y[n] == 1
for n in model.NODES:
    if pyo.value(model.y[n]) > 0:
        selected[n] = 1
    if n in start + end:
        selected[n] = 1

optimal_nodes = []

for node, sel in selected.items():
    if sel == 1:
        optimal_nodes.append(node)


print("Optimal Corridor =", optimal_nodes)


    
