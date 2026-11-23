import time
from multiprocessing import Pool


def check_even_odd(num):
    if num % 2 == 0:
        return (num, "Even")
    else:
        return (num, "Odd")


if __name__ == "__main__":
    n = int(input("Enter how many numbers: "))

    numbers = []

    for i in range(n):
        num = int(input("Enter number: "))
        numbers.append(num)

    start_time = time.perf_counter()

    with Pool() as pool:
        result = pool.map(check_even_odd, numbers)

    end_time = time.perf_counter()

    print("\nResults:")
    for num, value in result:
        print(num, "is", value)

    print("Execution Time:", end_time - start_time, "seconds")