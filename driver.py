import subprocess

file_path = "main.py"
# num_times = 50  # Number of times to run the file

# for _ in range(num_times):
while True:
    subprocess.call(["python", file_path])