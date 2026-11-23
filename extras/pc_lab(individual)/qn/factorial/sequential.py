import time

# Take input from user
n = int(input("Enter a number: "))

# Start timer
start_time = time.perf_counter()

# Initialize factorial
fact = 1

# Calculate factorial
for i in range(1, n + 1):
    fact = fact * i

# End timer
end_time = time.perf_counter()

# Display result
print("Factorial of", n, "is:", fact)

print("Execution Time:",
      end_time - start_time, "seconds")