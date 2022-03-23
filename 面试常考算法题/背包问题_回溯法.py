import numpy as np
def backpack_solover(weights, values, backpack_volume):
    assert len(weights) == len(values)

    used = [False]*len(weights)
    max_value = 0

    def back_tracking(used):
        num = len(used)
        if sum(weights*used) > backpack_volume:
            return

        for i in range(num):
            if (used[i]):
                continue
            elif sum(weights*used) > backpack_volume:
                break
            else:
                print("max_value:", max_value)

                tmp = sum(values*used)
                if(max_value < tmp):
                    max_value = tmp

                #max_value = max(max_value, sum(values*used))
                used[i] = True
                #back_tracking(used)
            used[i] = False
        return

    back_tracking(used)
    return


if __name__=="__main__":
    weight = np.array([2, 3, 4, 4, 1, 5, 6])
    value = np.array([2, 6, 4, 5, 3, 8, 9])
    weight_most = 15
    max_value = backpack_solover(weight, value, weight_most)
    print(max_value)
