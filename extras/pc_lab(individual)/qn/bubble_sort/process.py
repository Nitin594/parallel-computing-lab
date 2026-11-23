import time
from multiprocessing import Process, Queue


def bubble_sort(arr, q, index):
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        for j in range(n-i-1):

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    q.put((index, arr))


def merge_arrays(arrays):
    result = []

    while any(arrays):
        min_value = None
        min_index = -1

        for i in range(len(arrays)):
            if arrays[i]:
                if min_value is None or arrays[i][0] < min_value:
                    min_value = arrays[i][0]
                    min_index = i

        result.append(min_value)
        arrays[min_index].pop(0)

    return result


if __name__ == "__main__":
    n = int(input("Enter size of array: "))

    if n <= 0:
        print("Array size must be greater than zero.")
    else:
        arr = []

        for i in range(n):
            num = int(input("Enter element: "))
            arr.append(num)

        start_time = time.perf_counter()

        # Divide array into four parts
        parts = [arr[i::4] for i in range(4)]
        parts = [part for part in parts if part]

        q = Queue()
        processes = []

        for i, part in enumerate(parts):
            p = Process(target=bubble_sort, args=(part, q, i))
            processes.append(p)
            p.start()

        sorted_parts = [None] * len(parts)

        for i in range(len(parts)):
            index, sorted_arr = q.get()
            sorted_parts[index] = sorted_arr

        for p in processes:
            p.join()

        result = merge_arrays(sorted_parts)

        end_time = time.perf_counter()

        print("Original Array:", arr)
        print("Sorted Array:", result)
        print("Execution Time:", end_time-start_time, "seconds")