import time
from multiprocessing import Pool


# Function to transpose one column
def transpose_column(args):

    j, A = args

    result = []

    for i in range(len(A)):
        result.append(A[i][j])

    return result


if __name__ == "__main__":

    # Define matrix
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    rows = len(A)
    cols = len(A[0])

    # Start timer
    start_time = time.perf_counter()

    # Create process pool
    with Pool(processes=3) as pool:

        tasks = [(j, A) for j in range(cols)]

        # Distribute tasks
        T = pool.map(transpose_column, tasks)

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Transpose Matrix:")

    for row in T:
        print(row)

    print("Execution Time:",
          end_time - start_time, "seconds")