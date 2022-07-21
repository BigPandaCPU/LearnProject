
def max_subarray(A):
    max_ending_here = max_so_far =A[0]
    for x in A[1:]:
        max_ending_here = max(x, max_ending_here+x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

A = [1,2,3,-4, 5,6,-2, 7,2,-4,-3,5]
A_max_sub = max_subarray(A)
print(A_max_sub)