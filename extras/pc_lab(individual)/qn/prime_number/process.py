import time
import math
from multiprocessing import Process, Queue


def check_divisor(i, n, q):
    if n % i == 0:
        q.put(True)
    else:
        q.put(False)


def check_prime(n):
    if n <= 1:
        return False

    divisors = list(range(2, math.isqrt(n) + 1))

    if not divisors:
        return True

    q = Queue()
    processes = []

    for i in divisors:
        p = Process(target=check_divisor, args=(i, n, q))
        processes.append(p)
        p.start()

    results = []

    for i in divisors:
        results.append(q.get())

    for p in processes:
        p.join()

    return not any(results)


if __name__ == "__main__":
    num = int(input("Enter a number: "))

    start_time = time.perf_counter()

    result = check_prime(num)

    end_time = time.perf_counter()

    if result:
        print(num, "is a Prime Number")
    else:
        print(num, "is Not a Prime Number")

    print("Execution Time:", end_time - start_time, "seconds")