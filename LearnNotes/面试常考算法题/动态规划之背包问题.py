#0-1背包问题，二位数组解法
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


# 0-1背包问题，找到背包中的物品
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




#0-1背包里的一维数组解法
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

#完全背包问题
#物品是可以重复取的，问题关键的是更新的策略
weight = [2, 3, 4, 7]
value =  [1, 3, 5, 9]

bag_weight = 10

dp = [[0 for i in range(bag_weight+1)] for j in range(len(weight))]

for i in range(bag_weight+1):
    dp[0][i] = (i//weight[0]) * value[0]
print(dp[0])

for i in range(1, len(weight)):
    for j in range(1, bag_weight+1):
        if ( j >= weight[i] ):
            dp[i][j] = max(dp[i-1][j], dp[i][j-weight[i]]+value[i])
        else:
            dp[i][j] = dp[i-1][j]
print(dp[-1][-1])