import random
def qsort(a, lo, hi):
    """
    Sorts the given list in ascending order using QuickSort algorithm.

    Parameters:
    a (list): List of elements to be sorted.
    lo (int): The lower index of the sub-list to be sorted.
    hi (int): The higher index of the sub-list to be sorted.

    """
    if(lo >= hi):
        return
    p = a[(lo + hi) // 2]       # pivot, any a[] except a[hi]
    i = lo - 1
    j = hi + 1
    while(1):
        while(1):               # while(a[++i] < p)
            i += 1
            if(a[i] >= p):
                break
        while(1):               # while(a[--j] < p)
            j -= 1
            if(a[j] <= p):
                break
        if(i >= j):
            break
        a[i],a[j] = a[j],a[i]
    qsort(a, lo, j)
    qsort(a, j+1, hi)

list = [random.randint(0, 10000) for i in range(1000000)]

qsort(list,0,len(list)-1)
print(list)