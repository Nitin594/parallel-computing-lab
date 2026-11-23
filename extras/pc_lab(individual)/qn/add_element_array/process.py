import time
from multiprocessing import Process, Queue


def array_sum(part, q):
    total = sum(part)
    q.put(total)


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

        for part in parts:
            p = Process(target=array_sum, args=(part, q))
            processes.append(p)
            p.start()

        results = []

        for i in range(len(parts)):
            results.append(q.get())

        for p in processes:
            p.join()

        total = sum(results)

        end_time = time.perf_counter()

        print("Array:", arr)
        print("Sum of Array Elements:", total)
        print("Execution Time:", end_time - start_time, "seconds")