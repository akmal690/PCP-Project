import time

start_time = time.time()  # Start tracking time
input("Press Enter when you finish playing...")  # Wait for user to signal end
end_time = time.time()  # Stop tracking

total_time = round((end_time - start_time) / 60, 2)  # Convert to minutes
print(f"You played for {total_time} minutes.")
