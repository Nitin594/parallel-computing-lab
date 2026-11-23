import time
from multiprocessing import Pool


def find_min_max(part):
    return min(part), max(part)


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

        # Divide array into smaller parts
        parts = [arr[i::4] for i in range(4)]
        parts = [part for part in parts if part]

        with Pool() as pool:
            results = pool.map(find_min_max, parts)

        minimum = min(result[0] for result in results)
        maximum = max(result[1] for result in results)

        end_time = time.perf_counter()

        print("Array:", arr)
        print("Minimum Element:", minimum)
        print("Maximum Element:", maximum)
        print("Execution Time:", end_time - start_time, "seconds")