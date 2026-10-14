def merge(A, B):
    C = list()
    i = j = 0
    print(f"\nMerging arrays {A} and {B} into", end="")
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            C.append(A[i])
            i += 1
        else:
            C.append(B[j])
            j += 1
    while i < len(A):
        C.append(A[i])
        i += 1
    while j < len(B):
        C.append(B[j])
        j += 1
    print(f" array {C}")
    return C

def merge_sort(arr):
    result = arr
    print(f"Preparing to sort {arr=}")
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        print(f"\tSplitting it into {left_half} and {right_half}")
        sorted_left = merge_sort(left_half)
        sorted_right = merge_sort(right_half)
        print(f"About to merge {sorted_left} and {sorted_right}")
        result = merge(sorted_left, sorted_right)
    return result

# test
test = [7,6,5,4,3,2,1,0]
print(merge_sort(test))