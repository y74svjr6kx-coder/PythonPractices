import re

text = input()

result = re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()

print(result)
