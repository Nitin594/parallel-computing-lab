import time
from multiprocessing import Pool


def array_sum(part):
    return sum(part)


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

        with Pool() as pool:
            results = pool.map(array_sum, parts)

        total = sum(results)

        end_time = time.perf_counter()

        print("Array:", arr)
        print("Sum of Array Elements:", total)
        print("Execution Time:", end_time - start_time, "seconds")