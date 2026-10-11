import os

with open("sample.txt", "r") as file:
    lines = file.readlines()

print(len(lines))

items = ["Apple", "Banana", "Orange"]

with open("list.txt", "w") as file:
    for item in items:
        file.write(item + "\n")

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    with open(letter + ".txt", "w") as file:
        file.write(letter)

with open("sample.txt", "r") as source:
    content = source.read()

with open("copy.txt", "w") as destination:
    destination.write(content)

path = "copy.txt"

if os.path.exists(path) and os.access(path, os.W_OK):
    os.remove(path)
    print("File deleted")
else:
    print("Cannot delete file")
