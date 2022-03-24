#背包的最大价值
weight = [0, 2, 3, 4, 4, 1, 5, 6]
value =  [0, 2, 6, 4, 5, 3, 8, 9]
weight_most = 15
wuping =[]
bag = [[0 for i in range(weight_most+1)] for j in range(len(weight))]
for i in range(1, len(weight)):
    for j in range(1, weight_most+1):
        if j >= weight[i]:
            bag[i][j] = max(bag[i-1][j-weight[i]]+value[i], bag[i-1][j])
        else:
            bag[i][j] = bag[i-1][j]
for j in range(len(weight)):
    print(bag[j])


wuping.clear()

j = weight_most
i = len(weight)-1
while(j>0):
    if bag[i][j] != bag[i-1][j]: #判断第i见物品，被装进背包
        wuping.append(weight[i])
        j = j-weight[i]
        i -=1
    else: #没有被装进背包
        i-= 1
print(wuping)



#print(wuping)

#背包里的物品
weight = [2, 3, 4, 4, 1]
value =  [2, 6, 4, 5, 3]

weight = [2, 3, 4, 4, 1, 5, 6]
value =  [2, 6, 4, 5, 3, 8, 9]
weight_most=15
dp = [0]*(weight_most+1)
#print(dp)

for i in range(len(weight)):
    for j in range(weight_most, weight[i]-1, -1):  #只有一个物品的时候，背包所装的最大价值就是该物品的价值
        dp[j] = max(dp[j-weight[i]]+value[i], dp[j])

    print(dp)