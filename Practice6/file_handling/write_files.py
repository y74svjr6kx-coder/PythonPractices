with open("sample.txt", "w") as file:
    file.write("Hello Python\n")
    file.write("Practice 6\n")

with open("sample.txt", "a") as file:
    file.write("New line\n")

try:
    with open("new_file.txt", "x") as file:
        file.write("New file created")
except FileExistsError:
    print("File already exists")

items = ["Apple", "Banana", "Orange"]

with open("list.txt", "w") as file:
    for item in items:
        file.write(item + "\n")
