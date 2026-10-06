import re

text = input()

if re.fullmatch(r"a.*b", text):
    print("Match")
else:
    print("No match")
