import os

def get_directory_size(directory, max_depth=3, current_depth=0):
    total_size = 0
    if current_depth > max_depth:
        return total_size
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
        for d in dirnames:
            total_size += get_directory_size(os.path.join(dirpath, d), max_depth, current_depth + 1)
        break  # Prevent os.walk from going deeper
    return total_size

def find_large_directories(root_directory, size_threshold_mb=100, max_depth=3):
    large_directories = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        dir_size = get_directory_size(dirpath, max_depth) / (1024 * 1024)  # Convert size to MB
        if dir_size > size_threshold_mb:
            large_directories.append((dirpath, dir_size))
    return large_directories

# Set the root directory to the current working directory
root_directory = "."

# Find directories larger than 100 MB
large_directories = find_large_directories(root_directory)

# Print the results
if large_directories:
    print("Large directories found:")
    for dirpath, dir_size in large_directories:
        print(f"{dirpath}: {dir_size:.2f} MB")
else:
    print("No large directories found.")
