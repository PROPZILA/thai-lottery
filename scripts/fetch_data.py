"""สร้าง data/draws.json (เฉพาะรางวัลที่ 1 เลข 6 หลัก) จากชุดข้อมูล WimPalaLab/thai-lottery-data
ซึ่งดึงผลจาก API ของสำนักงานสลากฯ (GLO) อัปเดตทุกวัน
ต้นทาง: https://github.com/WimPalaLab/thai-lottery-data
"""
import csv, io, json, os, urllib.request

URL = "https://raw.githubusercontent.com/WimPalaLab/thai-lottery-data/main/data/thai_lottery.csv"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "draws.json")
FROM_DATE = "1995-01-01"   # ใช้ทุกงวดที่มีในชุดข้อมูล

def numbers(cell):
    return [n.strip() for n in (cell or "").split("|") if n.strip().isdigit()]

def parse(text):
    """เก็บเฉพาะรางวัลที่ 1 (เลข 6 หลัก) ของทุกงวด"""
    draws = []
    for row in csv.DictReader(io.StringIO(text)):
        if row["draw_date"] < FROM_DATE:
            continue
        first = numbers(row.get("first"))
        if first and len(first[0]) == 6:
            draws.append({"date": row["draw_date"], "first": first[0]})
    return sorted(draws, key=lambda d: d["date"])

def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "lottery-stats/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        text = r.read().decode("utf-8-sig")    # ไฟล์ต้นทางมี BOM
    draws = parse(text)
    if not draws:
        raise SystemExit("ไม่พบข้อมูล: รูปแบบไฟล์ต้นทางอาจเปลี่ยน")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(draws, f, ensure_ascii=False, separators=(",", ":"))
    print(f"บันทึก {len(draws)} งวด ({draws[0]['date']} ถึง {draws[-1]['date']})")

if __name__ == "__main__":
    main()
