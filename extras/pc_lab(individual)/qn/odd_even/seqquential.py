import time

def check_even_odd(numbers):
    result = []

    for num in numbers:
        if num % 2 == 0:
            result.append((num, "Even"))
        else:
            result.append((num, "Odd"))

    return result


if __name__ == "__main__":
    n = int(input("Enter how many numbers: "))

    numbers = []

    for i in range(n):
        num = int(input("Enter number: "))
        numbers.append(num)

    start_time = time.perf_counter()

    result = check_even_odd(numbers)

    end_time = time.perf_counter()

    print("\nResults:")
    for num, value in result:
        print(num, "is", value)

    print("Execution Time:", end_time - start_time, "seconds")