import time
import math
from multiprocessing import Pool


def check_divisor(i, n):
    return n % i == 0


def check_prime(n):
    if n <= 1:
        return False

    divisors = range(2, math.isqrt(n) + 1)

    if len(divisors) == 0:
        return True

    with Pool() as pool:
        results = pool.starmap(
            check_divisor,
            [(i, n) for i in divisors]
        )

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