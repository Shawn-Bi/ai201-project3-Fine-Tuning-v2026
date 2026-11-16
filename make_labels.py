import csv, re
raw = open("data/raw_posts.txt", encoding="utf-8", newline=None).read()
pat = re.compile(r"TITLE: (.*?)\nBODY: (.*?)\nURL: \S+\n===\n(?=TITLE: |\Z)", re.S)
posts = pat.findall(raw)
assert "".join(f"TITLE: {t}\nBODY: {b}\n" for t, b in posts) is not None
with open("labels.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\r\n")
    w.writerow(["text", "label", "note"])
    for t, b in posts:
        w.writerow([f"{t}\n{b}", "", ""])
with open("data/cold20.md", "w", encoding="utf-8", newline="\n") as f:
    for i, (t, b) in enumerate(posts[:20], 1):
        f.write(f"{i}.\n{t}\n{b}\n\nLABEL: \n\n")
print("rows:", len(posts))
