import time

def fibonacci(n):
    a, b = 0, 1
    series = []

    for i in range(n):
        series.append(a)
        a, b = b, a + b

    return series


if __name__ == "__main__":
    n = int(input("Enter number of terms: "))

    if n < 0:
        print("Please enter a non-negative number.")
    else:
        start_time = time.perf_counter()

        result = fibonacci(n)

        end_time = time.perf_counter()

        print("Fibonacci Series:", result)
        print("Execution Time:", end_time - start_time, "seconds")