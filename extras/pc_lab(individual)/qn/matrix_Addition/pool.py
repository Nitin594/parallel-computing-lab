import time
from multiprocessing import Pool

# Function to add two rows
def add_rows(data):
    row_a, row_b = data
    return [row_a[i] + row_b[i]
            for i in range(len(row_a))]

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

    # Start execution time
    start_time = time.perf_counter()

    # Create process pool
    with Pool() as pool:

        # Distribute rows among processes
        C = pool.map(add_rows, zip(A, B))

    # End execution time
    end_time = time.perf_counter()

    # Display result
    print("Resultant Matrix:")
    for row in C:
        print(row)

    print("\nExecution Time:",
          end_time - start_time, "seconds")