class Solution(object):
    def  integerBreak(self, n):
        dp = [1]*(n+1)
        for i in range(2, n+1):
            max_num = dp[i]
            for j in range(1, i):
                max_num= max(max_num, dp[i-j]*dp[j], dp[i-j]*j, (i-j)*j)
            dp[i] = max_num
        return dp[-1]

if __name__=="__main__":
    a = Solution().integerBreak(20)
    print(a)
