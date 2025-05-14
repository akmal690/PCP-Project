import time

# Prompt the user with a test sentence
test_sentence = "The quick brown fox jumps over the lazy dog."
print(f"Type the following: {test_sentence}")

# Start the timer
start_time = time.time()

# Capture user input
typed_input = input("Start typing: ")

# End the timer
end_time = time.time()

# Calculate typing speed
elapsed_time = end_time - start_time  # In seconds
word_count = len(typed_input.split())  # Count words in input
speed = word_count / (elapsed_time / 60)  # Words per minute

# Calculate accuracy
accuracy = len([char for char in typed_input if char in test_sentence]) / len(test_sentence) * 100

# Display the results
print(f"Typing Speed: {speed:.2f} words per minute")
print(f"Accuracy: {accuracy:.2f}%")

