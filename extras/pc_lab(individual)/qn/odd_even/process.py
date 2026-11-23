import time
from multiprocessing import Process, Queue


def check_even_odd(num, q):
    if num % 2 == 0:
        q.put((num, "Even"))
    else:
        q.put((num, "Odd"))


if __name__ == "__main__":
    n = int(input("Enter how many numbers: "))

    numbers = []

    for i in range(n):
        num = int(input("Enter number: "))
        numbers.append(num)

    start_time = time.perf_counter()

    q = Queue()
    processes = []

    for num in numbers:
        p = Process(target=check_even_odd, args=(num, q))
        processes.append(p)
        p.start()

    result = []

    for i in range(n):
        result.append(q.get())

    for p in processes:
        p.join()

    end_time = time.perf_counter()

    result.sort(key=lambda x: numbers.index(x[0]))

    print("\nResults:")
    for num, value in result:
        print(num, "is", value)

    print("Execution Time:", end_time - start_time, "seconds")