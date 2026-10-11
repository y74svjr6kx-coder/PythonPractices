import os

print(os.getcwd())

if not os.path.exists("test"):
    os.mkdir("test")

os.makedirs("parent/child", exist_ok=True)

for item in os.listdir("."):
    print(item)
