import time
import threading


def check_even_odd(num, result, index):
    if num % 2 == 0:
        result[index] = (num, "Even")
    else:
        result[index] = (num, "Odd")


if __name__ == "__main__":
    n = int(input("Enter how many numbers: "))

    numbers = []

    for i in range(n):
        num = int(input("Enter number: "))
        numbers.append(num)

    start_time = time.perf_counter()

    result = [None] * n
    threads = []

    for i in range(n):
        t = threading.Thread(
            target=check_even_odd,
            args=(numbers[i], result, i)
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.perf_counter()

    print("\nResults:")
    for num, value in result:
        print(num, "is", value)

    print("Execution Time:", end_time - start_time, "seconds")