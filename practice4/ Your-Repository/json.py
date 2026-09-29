import json
with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print("DN".ljust(55), "Description".ljust(15), "Speed".ljust(10), "MTU")
print("-" * 80)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    dn = attributes["dn"]
    description = attributes["descr"]
    speed = attributes["speed"]
    mtu = attributes["mtu"]

    print(dn.ljust(55), description.ljust(15), speed.ljust(10), mtu)
