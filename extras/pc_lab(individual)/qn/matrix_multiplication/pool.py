import time
from multiprocessing import Pool


# Function to multiply one row
def multiply_row(args):

    i, A, B = args

    result = []

    for j in range(len(B[0])):

        total = 0

        for k in range(len(B)):
            total += A[i][k] * B[k][j]

        result.append(total)

    return result


if __name__ == "__main__":

    # Define matrices
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    B = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]

    rows = len(A)

    # Start timer
    start_time = time.perf_counter()

    # Create process pool
    with Pool(processes=3) as pool:

        tasks = [(i, A, B) for i in range(rows)]

        # Distribute tasks
        C = pool.map(multiply_row, tasks)

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Resultant Matrix:")

    for row in C:
        print(row)

    print("Execution Time:",
          end_time - start_time, "seconds")