import time
import math

def check_prime(n):
    if n <= 1:
        return False

    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False

    return True


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