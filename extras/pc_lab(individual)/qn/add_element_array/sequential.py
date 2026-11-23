import time

def array_sum(arr):
    total = 0

    for num in arr:
        total = total + num

    return total


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

        result = array_sum(arr)

        end_time = time.perf_counter()

        print("Array:", arr)
        print("Sum of Array Elements:", result)
        print("Execution Time:", end_time - start_time, "seconds")