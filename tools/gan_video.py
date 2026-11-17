"""Gắn video đã xuất vào dữ liệu bài: thêm "video": {src, poster} cho bài nào đã có tệp mp4."""
import json, os, re, sys
TRANG = "/home/claude/baihoccuocsong"
TEP = {"lensau": "kho", "lentam": "bai"}
n = 0
for bai, tep in TEP.items():
    for f in sorted(os.listdir(f"{TRANG}/data/{bai}")):
        m = re.match(rf"{tep}(\d\d)\.js$", f)
        if not m: continue
        mp4 = f"video/{bai}/{tep}{m.group(1)}.mp4"
        if not os.path.exists(f"{TRANG}/{mp4}"): continue
        p = f"{TRANG}/data/{bai}/{f}"; s = open(p, encoding="utf-8").read()
        i = s.index("window.BAI_HOC = "); dau = s[:i]
        B = json.loads(s[i + len("window.BAI_HOC = "):].rstrip().rstrip(";"))
        moi = {"src": mp4, "poster": mp4[:-4] + ".jpg"}
        if B.get("video") != moi:
            B["video"] = moi
            open(p, "w", encoding="utf-8").write(dau + "window.BAI_HOC = " + json.dumps(B, ensure_ascii=False, indent=1) + ";\n")
            n += 1
print("đã gắn video cho", n, "bài")
