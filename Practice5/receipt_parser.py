import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

prices = re.findall(r"Стоимость\s*\n([\d ]+,\d{2})", text)

products = re.findall(
    r"\d+\.\s*\n(.+?)\n[\d,]+\s*x\s*[\d ]+,\d{2}",
    text
)

date_time = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
    text
)

payment = re.search(
    r"(Банковская карта|Наличные)",
    text
)

total = re.search(
    r"ИТОГО:\s*\n([\d ]+,\d{2})",
    text
)

prices = [
    float(price.replace(" ", "").replace(",", "."))
    for price in prices
]

result = {
    "products": products,
    "prices": prices,
    "calculated_total": sum(prices),
    "receipt_total": total.group(1) if total else None,
    "date": date_time.group(1) if date_time else None,
    "time": date_time.group(2) if date_time else None,
    "payment_method": payment.group(1) if payment else None
}

print(json.dumps(result, ensure_ascii=False, indent=4))
