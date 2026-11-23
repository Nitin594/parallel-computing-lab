import time

def find_min_max(arr):
    minimum = arr[0]
    maximum = arr[0]

    for num in arr:
        if num < minimum:
            minimum = num

        if num > maximum:
            maximum = num

    return minimum, maximum


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

        minimum, maximum = find_min_max(arr)

        end_time = time.perf_counter()

        print("Array:", arr)
        print("Minimum Element:", minimum)
        print("Maximum Element:", maximum)
        print("Execution Time:", end_time - start_time, "seconds")