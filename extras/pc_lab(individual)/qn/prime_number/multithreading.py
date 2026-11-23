import time
import math
import threading


def check_divisor(i, n, result, index):
    result[index] = (n % i == 0)


def check_prime(n):
    if n <= 1:
        return False

    divisors = list(range(2, math.isqrt(n) + 1))

    if not divisors:
        return True

    result = [False] * len(divisors)
    threads = []

    for index, i in enumerate(divisors):
        t = threading.Thread(
            target=check_divisor,
            args=(i, n, result, index)
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return not any(result)


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