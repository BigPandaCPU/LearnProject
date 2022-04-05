
path = []
#组合，不重复 从n（1-n）里面，取出k个数，有多少中取法
def backtracing(n, k, start_index):
    """

    :param n:
    :param k:
    :param startindex:
    :return:
    """
    if len(path) == k:
        print(path)
        return
    for i in range(start_index, n):
        path.append(i+1)
        backtracing(n, k, i+1)
        path.pop()

#组合2， 从（1-n）中按顺序依次取出k个数，每次取完后，在放回去，将取出来的数据按顺序进行排列，有多少中排列方式
def backtracing2(n, k):
    """

    :param n:
    :param k:
    :param startindex:
    :return:
    """
    if len(path) == k:
        print(path)
        return
    for i in range(0, n):
        path.append(i+1)
        backtracing2(n, k)
        path.pop()


#全排列 及 全排列有重复元素的情况
#对数据data,进行全排列，有多少中排列方式
def backtracing3(data, used):
    """

    :param n:
    :param k:
    :param startindex:
    :return:
    """
    if len(path) == len(data):
        print(path)
        return
    for i in range(len(data)):
        if used[i]:
            continue
        if (i > 0) and (data[i] == data[i-1]) and (used[i-1] is False):
            continue
        path.append(data[i])
        used[i] = True
        backtracing3(data, used)
        used[i] = False
        path.pop()

#所有子集，不含有重复的元素
def backtracing4(data, start_index):
    """

    :param n:
    :param k:
    :param startindex:
    :return:
    """
    # if len(path) == len(data):
    #     print(path)
    #     return
    print(path)
    for i in range(start_index, len(data)):
        # if used[i]:
        #     continue
        path.append(data[i])
        #used[i] = True
        backtracing4(data, i+1)
        #used[i] = False
        path.pop()

#找到数组data中的所有子集，其中有重复的元素情况
def backtracing5(data, used, start_index):
    """

    :param n:
    :param k:
    :param startindex:
    :return:
    """
    # if len(path) == len(data):
    #     print(path)
    #     return
    print(path)
    for i in range(start_index, len(data)):
        if (i > 0) and (data[i] == data[i - 1]) and (used[i - 1] is False):
            continue

        used[i] = True
        path.append(data[i])
        backtracing5(data, used, i+1)
        used[i] = False
        path.pop()

n = 3
k = 3
start_index = 0
data = [1, 1, 2]
used = [False] * len(data)
#backtracing5(data, used, 0)
backtracing2(3,2)

# data = [1,2,3,4,5]
# used = [False]*len(data)
# path = []
# def back_tracing(data, used):
#     if sum()