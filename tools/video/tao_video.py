"""Dựng video 2D cho mọi bài của góc "Bài học cuộc sống" theo khung Bài 1.

  python3 tao_video.py lensau 2 --kich-ban     # in lời Trâu Con để duyệt
  python3 tao_video.py lensau 2 --tts          # in các dòng gửi giọng Elio
  python3 tao_video.py lensau 2 --khung 40 95  # chụp thử vài khung hình (giây)
  python3 tao_video.py lensau 2 --xuat         # xuất video vào kho trang

Giọng Trâu Con: video2d/elio/<bai><NN>/01.wav … (mỗi câu một tệp, đúng thứ tự LOI).
Chưa có thì thời lượng được ước tính và video chỉ có phụ đề (chỉ để xem thử).
"""
import json, os, re, subprocess, sys, asyncio, wave, contextlib, unicodedata, shutil, functools, threading, http.server

GOC = os.path.dirname(os.path.abspath(__file__))
TRANG = "/home/claude/baihoccuocsong"
FPS = 30
TEN_THO = {"lensau": "Lên Sáu", "lentam": "Lên Tám"}
TEP = {"lensau": "kho", "lentam": "bai"}

SO = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười"]


def so_chu(n):
    if n <= 10: return SO[n]
    ch, dv = divmod(n, 10)
    dau = "mười" if ch == 1 else SO[ch] + " mươi"
    if dv == 0: return dau
    if dv == 1: return dau + (" một" if ch == 1 else " mốt")
    if dv == 4 and ch > 1: return dau + " tư"
    if dv == 5: return dau + " lăm"
    return dau + " " + SO[dv]


def thu_tu(n):
    return "thứ nhất" if n == 1 else ("thứ tư" if n == 4 else "thứ " + so_chu(n))


def nfc(s): return unicodedata.normalize("NFC", s)


def doc_bai(bai, so):
    s = open(f"{TRANG}/data/{bai}/{TEP[bai]}{so:02d}.js", encoding="utf-8").read()
    return json.loads(s[s.index("{"):s.rindex("}") + 1])


def chia_cau(van):
    """Tách đoạn thành câu; câu quá dài thì tách tiếp ở dấu hai chấm / chấm phẩy / dấu phẩy giữa câu."""
    ra = []
    for c in re.split(r"(?<=[.!?])\s+", van.strip()):
        hang = [c]
        while any(len(h) > 112 for h in hang):
            moi = []
            for h in hang:
                if len(h) <= 112: moi.append(h); continue
                cho = [m.end() for m in re.finditer(r"[:;]\s", h)] or [m.end() for m in re.finditer(r",\s", h)]
                if not cho: moi.append(h); continue
                k = min(cho, key=lambda x: abs(x - len(h) / 2))
                a, b = h[:k].rstrip(), h[k:].strip()
                a = re.sub(r"[,;:]$", ".", a)
                moi += [a, b[0].upper() + b[1:]]
            if moi == hang: break
            hang = moi
        ra += hang
    return [x for x in ra if x]


def chuan(s): return re.sub(r"[^\w\s]", "", nfc(s).lower()).split()


TU_DUNG = set("thì là và của mà cho có không con các bạn mình chúng ta một những được đã để như nên với này ấy rồi lại đi ra vào".split())


def cau_tho_khop(cau, dong):
    """Các câu thơ (chỉ số) mà câu dịch xuôi nhắc lại: so âm tiết và cặp âm tiết."""
    a = chuan(cau); a2 = set(zip(a, a[1:])); a1 = set(a) - TU_DUNG
    diem = []
    for d in dong:
        b = chuan(d); diem.append(len(set(b) & a1) + 2 * len(set(zip(b, b[1:])) & a2))
    tot = max(diem) if diem else 0
    if tot < 1: return []
    return [i for i, x in enumerate(diem) if x >= max(1, tot * 0.5)]


def nhom_cua_cau_hoi(q, tho):
    """Câu hỏi trích câu thơ nhóm nào (dựa vào lời giải có ngoặc kép)."""
    trich = " ".join(re.findall(r"“([^”]+)”", q.get("giai", "")))
    if not trich: return None
    t = set(chuan(trich)); tot, chon = 0, None
    for g, nhom in enumerate(tho):
        diem = len(t & set(chuan(" ".join(c[0] for c in nhom))))
        if diem > tot: tot, chon = diem, g
    return chon if tot >= 2 else None


def tao_loi(bai, so, B):
    ten = TEN_THO[bai]; tho = B["tho"]; a, b = B["khoTho"]
    loi = []
    def them(sub, tt, say=None, **k): loi.append(dict(sub=sub, say=say, tt=tt, **k))
    them("Xin chào các bạn! Mình là Trâu Con.", "wave")
    them(f"Hôm nay, mình cùng các bạn học bài {so} của bài thơ {ten}.", "wave",
         f"Hôm nay, mình cùng các bạn học bài {thu_tu(so)} của bài thơ {ten}.")
    td = B["tieuDe"].rstrip(".")
    ten_bai = td if "“" in td else f"“{td}”"
    them(f"Bài hôm nay có tên: {ten_bai}" + ("" if td[-1] in "?!" else "."), "wave")
    them("Các bạn cùng nghe cô Hà đọc thơ nhé!", "listening")
    # dịch xuôi – mỗi nhóm thơ một lượt
    hinh_nhom = {g: [] for g in range(len(tho))}; con = []
    for q in B["cauHoi"]:
        h = q["chon"][q["dung"]][1]
        g = nhom_cua_cau_hoi(q, tho)
        (hinh_nhom[g] if g is not None else con).append(h)
    them("Bây giờ, mình kể lại bằng lời dễ hiểu nhé.", "reading", hinh=None, nhom=0, mo_dau=True)
    dung = set()
    for d in B["dichXuoi"]:
        g = d["nhom"]; cau = chia_cau(d["vi"]); L = len(tho[g]); goc = sum(len(x) for x in tho[:g])
        kho = hinh_nhom[g] + [h for h in con if h not in dung] + [h for gg in hinh_nhom for h in hinh_nhom[gg] if gg != g]
        kho = [h for h in dict.fromkeys(kho)]
        dong = [c_[0] for c_ in tho[g]]
        for i, c in enumerate(cau):
            tu, den = (i * L) // len(cau), max((i * L) // len(cau) + 1, ((i + 1) * L) // len(cau))
            khop = cau_tho_khop(c, dong)
            if khop: tu, den = min(khop), max(khop) + 1
            h = next((x for x in kho if x not in dung), kho[0] if kho else None)
            if h: dung.add(h)
            them(c, "reading", cau=list(range(goc + tu, goc + den)), hinh=h, nhom=g)
    if bai == "lensau" and so == 1:  # Bài 1: giữ tranh riêng đã duyệt
        rieng = ["chu-quoc-ngu", "hoc-cham", "doc-nghe", "day-dung-gio", "voi-vang", "vo-long", "hieu-bai"]
        cx = [x for x in loi if "cau" in x]
        for x, h in zip(cx, rieng): x["hinh"] = h
    md = next(i for i, x in enumerate(loi) if x.get("mo_dau"))
    loi[md]["hinh"] = loi[md + 1].get("hinh")  # câu mở đầu hiện sẵn tranh đầu tiên như Bài 1
    # từ khó: tối đa 4 từ ngắn
    hop = [t for t in B["tuKho"] if len(t["tu"].split()) <= 3 and not re.search(r"[,()]", t["tu"])]
    tu = ([t for t in hop if len(t["tu"].split()) >= 2] + [t for t in hop if len(t["tu"].split()) == 1])[:4]
    tu = [t for t in B["tuKho"] if t in tu]  # giữ thứ tự như trong bài
    them("Các bạn đọc theo mình nhé:", "thinking", tu_mo_dau=True)
    for t in tu:
        w = t["tu"]; h = None
        for q in B["cauHoi"]:
            if nfc(w.lower()) in nfc((q["hoi"] + " " + q["giai"] + " " + q["chon"][q["dung"]][0]).lower()):
                h = q["chon"][q["dung"]][1]; break
        them(w, "thinking", say=w + ".", tu=w, hinh_tu=h)
    # tranh cho thẻ từ: có đủ cho mọi từ thì dùng, thiếu thì bỏ hết cho đều
    the_tu = [x for x in loi if x.get("tu")]
    if bai == "lensau" and so == 1:
        for x, h in zip(the_tu, ["chu-quoc-ngu", "vo-long", "khoc-nhe", "voi-vang"]): x["hinh_tu"] = h
    if not all(x.get("hinh_tu") for x in the_tu) or len({x["hinh_tu"] for x in the_tu}) < len(the_tu):
        for x in the_tu: x["hinh_tu"] = None
    them("Các bạn hãy nhớ nhé:", "thumbs-up", nho_mo_dau=True)
    for x in B["baiHoc"]:
        them(x, "thumbs-up", nho=True)
    them("Bây giờ, các bạn nghe cô Hà giảng, trả lời câu hỏi, rồi viết vài câu thật hay nhé!", "cheer", ket=True)
    them("Hẹn gặp lại các bạn!", "wave", ket=True)
    return loi


def am_tiet(s): return len(re.findall(r"[^\s,.!?:;–\-“”]+", s))


def do_dai_wav(p):
    with contextlib.closing(wave.open(p)) as w: return w.getnframes() / w.getframerate()


def kich_ban(bai, so):
    B = doc_bai(bai, so); loi = tao_loi(bai, so, B)
    thu_muc = os.path.join(GOC, "elio", f"{bai}{so:02d}")
    tho = B["tho"]; tho_dai = tho[-1][-1][2] + 0.25
    cues, tu_the, canh, tu_moi, nho, nho_t = [], [], [], [], [], []
    t = 4.5; THE_DAU = 4.0

    def noi(i, gap=0.5):
        nonlocal t
        x = loi[i]; f = os.path.join(thu_muc, f"{i + 1:02d}.wav")
        if os.path.exists(f): d = do_dai_wav(f)
        else: d, f = am_tiet(x["say"] or x["sub"]) / 2.9 + 0.3, None
        c = {"t": round(t, 2), "d": round(d, 2), "sub": x["sub"], "ai": "trau", "tep": f}
        if x.get("cau") is not None: c["cau"] = x["cau"]
        if x.get("hinh"): c["hinh"] = x["hinh"]
        cues.append(c)
        if not tu_the or tu_the[-1]["ten"] != x["tt"]: tu_the.append({"t": round(t - 0.2, 2), "ten": x["tt"]})
        t += d + gap
        return c

    i = 0
    bd = t - 0.5
    for i in range(4): noi(i)
    canh.append({"id": "c-gioi-thieu", "bd": round(bd, 2), "kt": round(t, 2)})
    t += 0.3; tho_bd = t
    tu_the.append({"t": round(t - 0.2, 2), "ten": "listening"})
    for nhom in tho:
        for (c, a, b) in nhom: cues.append({"t": round(tho_bd + a, 2), "d": round(b - a, 2), "sub": c, "ai": "coha"})
    canh.append({"id": "c-tho", "bd": round(tho_bd - 0.3, 2), "kt": round(tho_bd + tho_dai + 0.4, 2)})
    t = tho_bd + tho_dai + 0.8
    # dịch xuôi
    k = 4; nhom_dang = None; bd = t - 0.4
    while k < len(loi) and "nhom" in loi[k]:
        g = loi[k]["nhom"]
        if nhom_dang is not None and g != nhom_dang:
            canh.append({"id": "c-xuoi", "bd": round(bd, 2), "kt": round(t, 2), "nhom": nhom_dang}); t += 0.2; bd = t - 0.4
        nhom_dang = g
        noi(k, gap=0.6); k += 1
    canh.append({"id": "c-xuoi", "bd": round(bd, 2), "kt": round(t, 2), "nhom": nhom_dang})
    # từ mới
    bd = t - 0.4; noi(k); k += 1
    while k < len(loi) and loi[k].get("tu"):
        tu_moi.append({"tu": loi[k]["tu"], "hinh": loi[k].get("hinh_tu"), "t": round(t, 2)}); noi(k, gap=1.6); k += 1
    canh.append({"id": "c-tu", "bd": round(bd, 2), "kt": round(t, 2)})
    # nhớ nhé
    bd = t - 0.4; noi(k); k += 1
    while k < len(loi) and loi[k].get("nho"):
        nho.append(loi[k]["sub"]); nho_t.append(round(t, 2)); noi(k); k += 1
    canh.append({"id": "c-nho", "bd": round(bd, 2), "kt": round(t + 0.2, 2)})
    t += 0.2; bd = t - 0.4
    buoc_t = [round(t + 1.2, 2), round(t + 3.0, 2), round(t + 4.6, 2)]
    while k < len(loi): noi(k); k += 1
    canh.append({"id": "c-ket", "bd": round(bd, 2), "kt": round(t, 2)})
    a, b = B["khoTho"]
    kb = {
        "bai": bai, "so": so, "tenTho": TEN_THO[bai], "nhan": f"Bài {so} · Khổ {a}–{b}", "tieuDe": B["tieuDe"].rstrip("."),
        "tho": tho, "thoBatDau": round(tho_bd, 2), "theDau": THE_DAU, "theCuoi": round(t, 2), "tong": round(t + 3.6, 2),
        "cues": cues, "tuThe": tu_the, "canh": canh,
        "hinhCan": sorted({c["hinh"] for c in cues if c.get("hinh")}),
        "tuMoi": tu_moi, "nho": nho, "nhoT": nho_t,
        "buoc": [{"chu": "Nghe cô Hà giảng", "hinh": "doc-nghe"}, {"chu": "Trả lời câu hỏi", "hinh": "hieu-bai"},
                 {"chu": "Viết vài câu", "hinh": "hoc-cham"}],
        "buocT": buoc_t,
        "thoAm": os.path.join(TRANG, B["amThanh"]["tho"]),
    }
    return kb, loi


def ghi_kb(kb):
    # mang theo tranh và màu góc học từ trang thật
    os.makedirs(os.path.join(GOC, "trang"), exist_ok=True)
    import filecmp
    for a, b in [("js/hinh.js", "hinh.js"), ("js/hinh-ghep.js", "hinh-ghep.js"), ("css/hinh.css", "hinh.css")]:
        dst = os.path.join(GOC, "trang", b)
        if not os.path.exists(dst) or not filecmp.cmp(os.path.join(TRANG, a), dst, shallow=False):
            shutil.copy(os.path.join(TRANG, a), dst)
    s = open("/home/claude/mau-chung/v1/cvcec-chung.js", encoding="utf-8").read()
    m = re.search(r'id: "cuocsong".*?mau: "(#\w+)", mau_dam: "(#\w+)", mau_nhat: "(#\w+)"', s, re.S)
    kb["mau"] = {"goc": m.group(1), "dam": m.group(2), "nhat": m.group(3)}
    ten = f"{kb['bai']}{kb['so']:02d}"
    with open(os.path.join(GOC, f"kb_{ten}.js"), "w", encoding="utf-8") as f:
        f.write("window.KICH_BAN = " + json.dumps(kb, ensure_ascii=False) + ";\n")
    h = open(os.path.join(GOC, "bai.html"), encoding="utf-8").read().replace('src="kichban.js"', f'src="kb_{ten}.js"')
    open(os.path.join(GOC, f"bai_{ten}.html"), "w", encoding="utf-8").write(h)


class _Lang(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def may_chu(cong):
    h = functools.partial(_Lang, directory=GOC)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", cong), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


async def chup(kb, cac_giay, ra, cong):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1920, "height": 1080}); loi = []
        pg.on("pageerror", lambda e: loi.append(str(e)))
        await pg.goto(f"http://127.0.0.1:{cong}/bai_{kb['bai']}{kb['so']:02d}.html"); await pg.wait_for_function("window.SAN_SANG === true")
        await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        for g in cac_giay:
            await pg.evaluate(f"ve({g})"); await pg.screenshot(path=f"{ra}_{int(g * 10):05d}.jpg", type="jpeg", quality=80)
        await b.close()
        if loi: print("LỖI TRANG:", loi)


async def ve_khung(kb, ra_video, cong):
    from playwright.async_api import async_playwright
    n = int(round(kb["tong"] * FPS))
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", ra_video], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto(f"http://127.0.0.1:{cong}/bai_{kb['bai']}{kb['so']:02d}.html"); await pg.wait_for_function("window.SAN_SANG === true")
        await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        for k in range(n):
            await pg.evaluate(f"ve({k / FPS})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=90))
        await b.close()
    ff.stdin.close(); ff.wait()


def tieng(kb, ra_am):
    vao = ["-f", "lavfi", "-t", str(kb["tong"]), "-i", "anullsrc=r=44100:cl=mono", "-i", kb["thoAm"]]
    loc = [f"[1:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(kb['thoBatDau'] * 1000)}:all=1[a1]"]; nhan = ["[0:a]", "[a1]"]; k = 2
    for c in kb["cues"]:
        if c.get("tep"):
            vao += ["-i", c["tep"]]
            loc.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(c['t'] * 1000)}:all=1[a{k}]"); nhan.append(f"[a{k}]"); k += 1
    loc.append("".join(nhan) + f"amix=inputs={len(nhan)}:normalize=0,atrim=0:{kb['tong']}[ra]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + vao + ["-filter_complex", ";".join(loc), "-map", "[ra]", "-c:a", "pcm_s16le", ra_am], check=True)


if __name__ == "__main__":
    bai, so = sys.argv[1], int(sys.argv[2]); a = sys.argv[3:]
    kb, loi = kich_ban(bai, so)
    if "--kich-ban" in a:
        for i, x in enumerate(loi, 1):
            print(f"{i:2d}. {x['sub']}" + (f"   [đọc: {x['say']}]" if x["say"] and x["say"] != x["sub"] + "." else "") + (f"   «{x['hinh']}»" if x.get("hinh") else ""))
        print("tổng ≈", kb["tong"], "giây")
    if "--tts" in a:
        print("\n".join((x["say"] or x["sub"]) for x in loi))
    cong = 8800 + so + (40 if bai == "lentam" else 0)
    if "--khung" in a or "--xuat" in a:
        ghi_kb(kb); sv = may_chu(cong)
        if "--khung" in a:
            giay = [float(x) for x in a[a.index("--khung") + 1:] if re.match(r"^[\d.]+$", x)]
            asyncio.run(chup(kb, giay, f"/home/claude/scratch/v_{bai}{so:02d}", cong))
        if "--xuat" in a:
            ra = os.path.join(TRANG, "video", bai, f"{TEP[bai]}{so:02d}.mp4"); os.makedirs(os.path.dirname(ra), exist_ok=True)
            hinh = os.path.join(GOC, f"_hinh_{bai}{so}.mp4"); am = os.path.join(GOC, f"_tieng_{bai}{so}.wav")
            asyncio.run(ve_khung(kb, hinh, cong)); tieng(kb, am)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", hinh, "-i", am, "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                            "-movflags", "+faststart", "-shortest", ra], check=True)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(kb["thoBatDau"] + 2), "-i", ra, "-frames:v", "1", "-q:v", "4",
                            ra[:-4] + ".jpg"], check=True)
            os.remove(hinh); os.remove(am)
            print("xong:", ra, round(os.path.getsize(ra) / 1e6, 1), "MB")
        sv.shutdown()
