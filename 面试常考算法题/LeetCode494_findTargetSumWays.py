import numpy as np
import copy
data = np.array([1, 1, 1, 1, 1])
used = [False]*len(data)

def back_tracing(data, used, S, start_index):
    if (sum(data[used]) == S):
        #path.append(copy.deepcopy(used))
        print( np.array( [ k+1 for k in range(0, len(data)) ] )[used] )

    for i in range(start_index, len(data)):
        used[i] = True
        back_tracing(data, used, S, i+1)
        used[i] = False

S = 3
s = (S+sum(data))/2
#back_tracing(data, used, s, 0 )


# #print(data.tolist())
# nums = data.tolist()
# ans= [0]
# def aux(cur_sum, cur_list):
#     if len(cur_list) == 0:
#         if cur_sum == S:
#             ans[0] += 1
#             #print(ans[0])
#     if len(cur_list) >0:
#         n = cur_list.pop(0)
#         aux(cur_sum+n, cur_list)
#         aux(cur_sum-n, cur_list)
# aux(0, nums)
# print(ans[0])
#
#
# class Solution:
#     def findTargetSumWays(self, nums, S):
#         ans = [0]
#
#         def aux(curSum, curList, ans):
#             if len(curList) == 0:
#                 if curSum == S:
#                     ans[0] += 1
#             if len(curList) > 0:
#                 n = curList.pop(0)
#                 aux(curSum + n, curList, ans)
#                 aux(curSum - n, curList, ans)
#
#         aux(0, nums, ans)
#         return ans[0]
# nums = [1, 1, 1, 1, 1]
# S = 3
# a = Solution().findTargetSumWays(nums, S)
# print(a)


def helper(nums, S, start, res):
    if start >= len(nums):
        if S==0:
            res[0] += 1
        return
    helper(nums, S-nums[start], start+1, res)
    helper(nums, S+nums[start], start+1, res)

nums=[1, 1, 1, 1, 1]
S = 3
res = [0]
helper(nums, S, 0, res)
print(res[0])
