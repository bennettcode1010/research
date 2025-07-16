import pyomo.environ as pyo
from newcorridordata import ARCS, NODES, B
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

model.end = 64

#Vars---

model.x = pyo.Var(model.ARCS, within=pyo.NonNegativeReals)
model.y = pyo.Var(model.ARCS, within=pyo.Binary)

#Obj---

model.obj = pyo.Objective(expr= sum(model.y[i,j] * model.u[j] for (i,j) in model.ARCS),sense='maximize')

#Constraints---

model.BudgetLimit = pyo.Constraint(expr = model.x[0, 1] <= model.B)


def flow_balance_rule(model,n):
    inflow = sum(model.x[i,j] for (i,j) in model.ARCS if j == n)
    outflow = sum(model.x[i,j] for (i,j) in model.ARCS if i == n)
    incoming_y = sum(model.y[i,j] for (i,j) in model.ARCS if j ==n)
    return inflow - outflow == incoming_y

model.FlowBalance = pyo.Constraint(model.NODES, rule = flow_balance_rule)

def arc_if_flow_rule(model,i,j):
    return model.y[i,j] <= model.x[i,j]

model.ArcifFlow = pyo.Constraint(model.ARCS, rule = arc_if_flow_rule)

def flow_if_arc_rule(model,i,j):
    return model.x[i,j] <= model.B * model.y[i,j]

model.FlowifArc = pyo.Constraint(model.ARCS, rule = flow_if_arc_rule)

model.ForceStartArc = pyo.Constraint(expr=model.y[0, 1] == 1)

model.NoOutflowFromEnd = pyo.Constraint(
    expr=sum(model.x[i, j] for (i, j) in model.ARCS if i == model.end) == 0
)

model.MustSelectEnd = pyo.Constraint(
    expr=sum(model.y[i, j] for (i, j) in model.ARCS if j == model.end) == 1
)
#talk about this
def unique_selection_rule(model, n):
    return sum(model.y[i, j] for (i,j) in model.ARCS if j == n) <= 1

model.UniqueSelection = pyo.Constraint(model.NODES, rule=unique_selection_rule)

# Solve the model using GLPK
solver = pyo.SolverFactory('glpk')
results = solver.solve(model)

# Print objective value
print("\nObjective Value:", pyo.value(model.obj))



selected = {n: 0 for n in model.NODES}

# Mark node j as selected if any y[i,j] == 1
for (i, j) in model.ARCS:
    if pyo.value(model.y[i, j]) > 0:
        selected[j] = 1

optimal_nodes = []
for node, sel in selected.items():
    if sel == 1:
        optimal_nodes.append(node)

print("Optimal Corridor =", optimal_nodes)
