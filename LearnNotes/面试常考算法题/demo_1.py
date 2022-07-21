#cost = [10, 15, 20]
cost = [1,100,1,1,1,100,1,1,100,1]
p0 = 0
p1 = 0
for i in range(2, len(cost)+1):
    tmp = p0
    p0 = p1
    p1 = min(p1+cost[i-1], tmp+cost[i-2])
print(p1)

# p1,p2 = 0, 0
# for i in range(2, len(cost)+1):
#             p1,p2 =p2, min(p2 + cost[i-1], p1 + cost[i-2])
# print(p2)