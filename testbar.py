from progress.bar import Bar
import time

# Simulate a task with a progress bar
bar = Bar('Processing', max=100)
for i in range(100):
    time.sleep(0.1)  # Simulate work
    bar.next()
bar.finish()

print("Progress bar test completed.")
