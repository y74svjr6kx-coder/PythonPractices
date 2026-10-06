import re

text = input()

result = re.sub(r"(?<!^)(?=[A-Z])", " ", text)

print(result)
