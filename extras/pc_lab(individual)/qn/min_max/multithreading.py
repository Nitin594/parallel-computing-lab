import time
import threading


def find_min_max(part, result, index):
    minimum = min(part)
    maximum = max(part)

    result[index] = (minimum, maximum)


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

        result = [None] * len(parts)
        threads = []

        for i, part in enumerate(parts):
            t = threading.Thread(
                target=find_min_max,
                args=(part, result, i)
            )

            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        minimum = min(item[0] for item in result)
        maximum = max(item[1] for item in result)

        end_time = time.perf_counter()

        print("Array:", arr)
        print("Minimum Element:", minimum)
        print("Maximum Element:", maximum)
        print("Execution Time:", end_time - start_time, "seconds")