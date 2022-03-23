import numpy as np
import copy
def backpack_solover(weights, values, backpack_volume):
    assert len(weights) == len(values)

    used = [False]*len(weights)
    max_value = 0
    path = used
    def back_tracking(used, max_value):
        global path
        print(path)
        num = len(used)
        if sum(weights*used) > backpack_volume:
            return max_value

        for i in range(num):
            if (used[i]):
                continue
            elif sum(weights*used) > backpack_volume:
                break
            else:
                if max_value < sum(values*used):
                    path = copy.deepcopy(used)
                    print(used)
                max_value = max(max_value, sum(values*used))

                used[i] = True
                max_value = back_tracking(used, max_value)
            used[i] = False
        return max_value

    max_value = back_tracking(used, max_value)
    print("path=",path)
    return max_value


if __name__=="__main__":
    weight = np.array([2, 3, 4, 4, 1, 5, 6])
    value = np.array([2, 6, 4, 5, 3, 8, 9])
    weight_most = 15
    max_value = backpack_solover(weight, value, weight_most)
    print(max_value)
