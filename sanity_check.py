import json

with open("data/extracted_text.json", encoding="utf-8") as f:
    data = json.load(f)

print(type(data), len(data))

first = data[0] if isinstance(data, list) else next(iter(data.items()))
print(type(first))
if isinstance(first, dict):
    print(list(first.keys()))
print(str(first)[:500])

import re

heading = re.compile(r"^(\d+(\.\d+)*\.?\s+[A-Z][^\n]{2,80}|Abstract|References|Appendix.*)$", re.MULTILINE)

for paper_id, text in data.items():
    found = heading.findall(text)
    print(paper_id, len(text), "chars,", len(found), "heading-like lines")

# look at one paper's matches in detail
sample = next(iter(data.values()))
for m in heading.finditer(sample):
    print(repr(m.group(0)))