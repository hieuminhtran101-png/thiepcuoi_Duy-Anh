#!/usr/bin/env python3
"""Nhúng nhạc nền vào thiệp cưới HTML.

Cách dùng:
    python them_nhac.py Duy_Anh.html nhac_cuoi.mp3
    -> tạo ra file Duy_Anh_co_nhac.html (1 file duy nhất, gửi đi là có nhạc)

Hoặc dùng link nhạc có sẵn trên mạng (file sẽ nhẹ hơn):
    python them_nhac.py Duy_Anh.html https://ten-mien-cua-ban/nhac.mp3
"""
import base64, mimetypes, os, re, sys

if len(sys.argv) != 3:
    sys.exit(__doc__)

html_path, music = sys.argv[1], sys.argv[2]

if music.lower().startswith(("http://", "https://")):
    src = music
else:
    if not os.path.isfile(music):
        sys.exit(f"Không tìm thấy file nhạc: {music}")
    mime = mimetypes.guess_type(music)[0] or "audio/mpeg"
    with open(music, "rb") as f:
        src = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    print(f"Dung lượng nhạc: {os.path.getsize(music)/1024/1024:.1f} MB")

with open(html_path, encoding="utf-8") as f:
    html = f.read()

pattern = re.compile(r'music:\s*"(?:[^"\\]|\\.)*"')
if not pattern.search(html):
    sys.exit('Không tìm thấy dòng music:"" trong file HTML.')
html = pattern.sub(lambda m: f'music:"{src}"', html, count=1)

out = os.path.splitext(html_path)[0] + "_co_nhac.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("Xong! File mới:", out)