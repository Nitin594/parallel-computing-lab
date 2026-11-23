import time

# Define two matrices
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

# Get matrix dimensions
rows_A = len(A)
cols_A = len(A[0])
cols_B = len(B[0])

# Start timer
start_time = time.perf_counter()

# Create result matrix
C = [[0 for j in range(cols_B)]
     for i in range(rows_A)]

# Perform matrix multiplication
for i in range(rows_A):
    for j in range(cols_B):
        for k in range(cols_A):
            C[i][j] += A[i][k] * B[k][j]

# End timer
end_time = time.perf_counter()

# Display result
print("Resultant Matrix:")

for row in C:
    print(row)

print("Execution Time:",
      end_time - start_time, "seconds")