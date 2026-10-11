import os
import shutil

shutil.copy("sample.txt", "backup.txt")

path = "backup.txt"

if os.path.exists(path):
    os.remove(path)
    print("File deleted")
else:
    print("File does not exist")
