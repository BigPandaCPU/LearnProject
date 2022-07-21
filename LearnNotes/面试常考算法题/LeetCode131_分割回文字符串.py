#回溯法分割回文字符串
#题目说明#
#给定一个字符串S， 将S分割成一些子串，使得每个子串都是回文字符串
#示例#
#输入S=“abc”
#输出["a", "a", "b"], ["aa", "b"]

#思路，与求集合的所有子集思路相同
import copy

def is_palindrome(str):
    if str == str[::-1]:
        return True
    else:
        return False


S = "aab"
print(len(S))
path = []
results = []
def back_tracing(S, start_index):
    if (start_index >= len(S)):
        print(path)
        results.append(copy.deepcopy(path))

    for i in range(start_index, len(S)):
        sub_str = S[start_index: i+1]
        if is_palindrome(sub_str):
            path.append(sub_str)
        else:
            continue
        back_tracing(S, i+1)
        path.pop()

back_tracing(S, 0)
print(results)