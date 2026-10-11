import os
import shutil

os.makedirs("source", exist_ok=True)
os.makedirs("destination", exist_ok=True)

with open("source/test.txt", "w") as file:
    file.write("Hello")

shutil.copy("source/test.txt", "destination/test_copy.txt")

shutil.move("source/test.txt", "destination/test.txt")

print("Done")
