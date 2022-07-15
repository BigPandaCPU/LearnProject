import nlopt
from numpy import *
count = 0
def myfunc(x, grad):
    global count
    if grad.size > 0:
        grad[0] = 0.0
        grad[1] = 0.5 / sqrt(x[1])
    count += 1
    return sqrt(x[1])

def myconstraint(x, grad, a, b):
    if grad.size > 0:
        grad[0] = 3*a*(a*x[0]+b)**2
        grad[1] = -1.0
    return (a*x[0]+b)**3 - x[1]

opt = nlopt.opt(nlopt.LD_MMA, 2)
opt.set_lower_bounds([-float('inf'), 0])
opt.set_min_objective(myfunc)
opt.add_inequality_constraint(lambda x, grad:myconstraint(x, grad, 2, 0), 1e-8)  #添加不等式约束，要求不等式<0
opt.add_inequality_constraint(lambda x, grad:myconstraint(x, grad, -1, 1), 1e-8)
opt.set_xtol_rel(1e-4)  #设置x的绝对容差
x = opt.optimize([1.234, 5.678]) #设置x的初始值

print("count:", count)
minf = opt.last_optimum_value()
print("optimum at", x[0], x[1])
print("minmum value = ", minf)
print("result code = ", opt.last_optimize_result())