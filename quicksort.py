import random
import sys
#print(sys.getrecursionlimit())

def partition(arr, low, high, pivot):
    """
    This function takes an array, a low index, and a high index as input, and partitions the array
    into two parts based on a pivot. The function moves all elements less than or equal to the pivot
    to the left side of the pivot, and all elements greater than the pivot to the right side of the pivot.

    Args:
        arr (list): the array to partition
        low (int): the starting index of the partition
        high (int): the ending index of the partition
        pivot (int): the index of the pivot

    Returns:
        the index of the pivot after partitioning (int)
    """
    arr[low], arr[pivot] = arr[pivot], arr[low]
    pindex = low
    pivot = arr[low]
    for j in range(low + 1, high + 1):
        if arr[j] <= pivot:
            pindex += 1
            arr[pindex], arr[j] = arr[j], arr[pindex]
    arr[pindex], arr[low] = arr[low], arr[pindex]
    return pindex

def quickSort(arr, low, high, pivot_choice):
    """
    This function takes an array, a low index, a high index, and a pivot_choice as input, and sorts the
    array in ascending order using the QuickSort algorithm. The function partitions the array using the
    partition() function, and then recursively calls itself on the left and right partitions until
    the entire array is sorted.

    Args:
        arr (list): the array to sort
        low (int): the starting index of the partition to sort
        high (int): the ending index of the partition to sort
        pivot_choice (str): the pivot choice. Can be "left" or "right".

    Returns:
        None
    """
    if low < high:
        if pivot_choice == "left":
            pi = partition(arr, low, high, low)
        elif pivot_choice == "right":
            pi = partition(arr, low, high, high)
        else:
            raise ValueError("Invalid pivot choice")
        quickSort(arr, low, pi - 1, pivot_choice)
        quickSort(arr, pi + 1, high, pivot_choice)

list = [random.randint(0, 100) for i in range(1000000)]
""" 
print("Unsorted array:")
#print(list)

pivot_choice = input("Choose pivot (left or right): ")
n = len(list)
quickSort(list, 0, n - 1, pivot_choice)

print("Sorted array:")
#print(list)
 """
list.sort()