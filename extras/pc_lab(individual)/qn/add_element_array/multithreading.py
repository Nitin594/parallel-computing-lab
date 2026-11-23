import time
import threading


def array_sum(part, result, index):
    result[index] = sum(part)


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

        result = [0] * len(parts)
        threads = []

        for i, part in enumerate(parts):
            t = threading.Thread(
                target=array_sum,
                args=(part, result, i)
            )

            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total = sum(result)

        end_time = time.perf_counter()

        print("Array:", arr)
        print("Sum of Array Elements:", total)
        print("Execution Time:", end_time - start_time, "seconds")