"""Xuất âm thanh + dữ liệu cho trang Bài học cuộc sống từ bản ghi mới (16/11/2026).
- Lên Sáu: 18 bài (mỗi bài 2 khổ), lời giảng = cả bản ghi mới (đã kết bằng lời cảm ơn).
- Lên Tám: 32 bài có ghi âm (khổ 1–64).
"""
import json, os, re, subprocess, sys, unicodedata
sys.path.insert(0, '/home/claude/tools')
from can_lentam import sua as sua_lentam
_src = open('/home/claude/tools/xuat_kho.py', encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('TIEU_DE = {'):_src.index('def hoa_dau')], _ns)
TIEU_DE, CHU_DE = _ns['TIEU_DE'], _ns['CHU_DE']

GOC = '/home/claude/cuocsong-site'
LS, LT = '/home/claude/moi/lensau', '/home/claude/moi/lentam'


def nfc(s): return unicodedata.normalize('NFC', s)


def dep(s):
    """Ngoặc kép cong, gạch nối dài, bỏ khoảng trắng thừa."""
    s = nfc(s).replace('\xa0', ' ')
    s = re.sub(r'"([^"\n]*)"', '“\\1”', s)
    s = s.replace(' - ', ' – ')
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def hoa_dau(c): return c[:1].upper() + c[1:]


def ffmpeg(*a): subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *a], check=True)


def xuat_giang(src, het, dst):
    ffmpeg("-i", src, "-af", f"atrim=0:{het:.2f},afade=t=out:st={het - 0.15:.2f}:d=0.15,apad=pad_dur=0.6,highpass=f=70,loudnorm=I=-18:TP=-2:LRA=11",
           "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "64k", dst)


def xuat_tho(src, dv, dst, sua=lambda x: x):
    nhom = {}
    for u in dv:
        if u['tho']: nhom.setdefault(u['doan'], []).append(u)
    loc, nhan, ket, t_ra = [], [], [], 0.0
    ds = sorted(nhom.items())
    for gi, (_, us) in enumerate(ds):
        a = max(0, us[0]['bd'] - 0.12); b = us[-1]['kt'] + 0.15
        loc.append(f"[0:a]atrim={a:.2f}:{b:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={b - a - 0.06:.2f}:d=0.06[g{gi}]")
        nhan.append(f"[g{gi}]")
        ket.append([[hoa_dau(dep(sua(u['chu']))), round(t_ra + u['bd'] - a, 2), round(t_ra + u['kt'] - a, 2)] for u in us])
        t_ra += b - a
        if gi < len(ds) - 1:
            loc.append(f"anullsrc=r=44100:cl=mono,atrim=0:0.7[s{gi}]"); nhan.append(f"[s{gi}]"); t_ra += 0.7
    loc.append("".join(nhan) + f"concat=n={len(nhan)}:v=0:a=1,highpass=f=70,loudnorm=I=-18:TP=-2:LRA=11[ra]")
    ffmpeg("-i", src, "-filter_complex", ";".join(loc), "-map", "[ra]", "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "96k", dst)
    return ket


def loi_giang(doan, sua=lambda x: x):
    out = []
    for d in doan:
        if 'tho' in d: out.append({"tho": [hoa_dau(dep(sua(c))) for c in d['tho']], "t": d['t']})
        else: out.append({"vi": dep(sua(d['vi'])), "t": d['t']})
    return out


def ghi_js(path, dau, obj, ten="window.BAI_HOC"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(dau + "\n" + ten + " = " + json.dumps(obj, ensure_ascii=False, indent=1) + ";\n")


def doc_js(path):
    s = open(path, encoding='utf-8').read(); return json.loads(s[s.index('{'):s.rindex('}') + 1])


# ---------------------------------------------------------------- Lên Sáu
def lensau(chon):
    os.makedirs(f'{GOC}/audio/lensau', exist_ok=True)
    ds = []
    for n in range(1, 19):
        c = json.load(open(f'{LS}/can_kho{n:02d}.json'))
        src = f'{LS}/src/{n:02d}.m4a'
        het = c['het']
        if n in chon:
            xuat_giang(src, het, f'{GOC}/audio/lensau/kho{n:02d}-giang.mp3')
        lg = loi_giang(c['doan'])
        if n == 1:
            B = doc_js(f'{GOC}/data/lensau/kho01.js')
            assert len(B['loiGiang']) == len(lg)
            for cu, moi in zip(B['loiGiang'], lg):
                assert ('tho' in cu) == ('tho' in moi)
                cu['t'] = moi['t']
            # hai đoạn cuối đổi chữ theo bản ghi mới
            B['loiGiang'][-2]['vi'] = lg[-2]['vi']
            B['loiGiang'][-2]['en'] = ("Turning six is a special milestone: “vỡ lòng” means your very first steps in learning, when everything is new. "
                                       "“Học cho thông” means understanding each lesson as you go – reading and writing well. "
                                       "Then your teacher won't scold you; you'll get smiles, praise and good marks instead!")
            B['loiGiang'][-1]['vi'] = lg[-1]['vi']
            B['loiGiang'][-1]['en'] = ("This verse is like a mirror to look into every day: love your language, study hard, read aloud and listen, "
                                       "don't cry in the morning, and don't rush. Cô Hà thanks you for learning the first two verses of “Lên Sáu” with her.")
            B['amThanh']['giangGiay'] = round(het + 0.6)
            B['khoTho'] = [1, 2]
            ghi_js(f'{GOC}/data/lensau/kho01.js', "/* Lên Sáu – Bài 1 (khổ 1–2). Đủ bài. */", B)
            tho = B['tho']
        else:
            if n in chon:
                tho = xuat_tho(src, c['dv'], f'{GOC}/audio/lensau/kho{n:02d}-tho.mp3')
            else:
                tho = doc_js(f'{GOC}/data/lensau/kho{n:02d}.js')['tho']
            B = {"bai": "lensau", "kho": n, "khoTho": [2 * n - 1, 2 * n], "tieuDe": TIEU_DE[n], "chuDe": CHU_DE[n], "tho": tho,
                 "amThanh": {"tho": f"audio/lensau/kho{n:02d}-tho.mp3", "giang": f"audio/lensau/kho{n:02d}-giang.mp3", "giangGiay": round(het + 0.6)},
                 "loiGiang": lg, "keBoMe": [dep(q) for q in c['cau_hoi']],
                 "nguon": "Thơ: Tản Đà, bài “Lên Sáu” · Giảng và đọc thơ: cô Hà"}
            ghi_js(f'{GOC}/data/lensau/kho{n:02d}.js', f"/* Lên Sáu – Bài {n} (khổ {2 * n - 1}–{2 * n}). Khung: thơ, cô Hà đọc thơ, lời giảng. Các phần khác đang soạn. */", B)
        ds.append({"kho": n, "khoTho": [2 * n - 1, 2 * n], "tieuDe": B['tieuDe'], "chuDe": B['chuDe'],
                   "cauDau": [tho[0][0][0], tho[0][1][0]], "du": n == 1})
        print('Lên Sáu', n, 'giảng', het, 's', flush=True)
    ghi_js(f'{GOC}/data/lensau/danh-sach.js', "/* Danh sách 18 bài Lên Sáu (mỗi bài 2 khổ) – dùng cho trang chủ góc học */", ds, "window.DANH_SACH_KHO")


# ---------------------------------------------------------------- Lên Tám
CHU_DE_LT = {}
for a, b, t in [(1, 4, "Con người và sự học"), (5, 6, "Biết ơn ông cha"), (7, 13, "Cha mẹ"), (14, 14, "Đạo làm người"),
                (15, 20, "Chữ Hiếu"), (21, 25, "Anh em, họ hàng"), (26, 26, "Đạo làm người"), (27, 32, "Học tập")]:
    for i in range(a, b + 1): CHU_DE_LT[i] = t


def tieu_de(s):
    s = nfc(sua_lentam(s)).strip().lower()
    return s[:1].upper() + s[1:]


def lentam(chon):
    os.makedirs(f'{GOC}/audio/lentam', exist_ok=True); os.makedirs(f'{GOC}/data/lentam', exist_ok=True)
    ds = []
    for n in range(1, 33):
        c = json.load(open(f'{LT}/can_bai{n:02d}.json'))
        src = f'{LT}/src/{n:02d}.m4a'
        het = c['het']
        if n in chon:
            xuat_giang(src, het, f'{GOC}/audio/lentam/bai{n:02d}-giang.mp3')
            tho = xuat_tho(src, c['dv'], f'{GOC}/audio/lentam/bai{n:02d}-tho.mp3', sua_lentam)
        else:
            tho = doc_js(f'{GOC}/data/lentam/bai{n:02d}.js')['tho']
        a, b = c['kho']
        B = {"bai": "lentam", "kho": n, "khoTho": [a, b], "tieuDe": tieu_de(c['tieu_de']), "chuDe": CHU_DE_LT[n], "tho": tho,
             "amThanh": {"tho": f"audio/lentam/bai{n:02d}-tho.mp3", "giang": f"audio/lentam/bai{n:02d}-giang.mp3", "giangGiay": round(het + 0.6)},
             "loiGiang": loi_giang(c['doan'], sua_lentam),
             "nguon": "Thơ: Tản Đà, bài “Lên Tám” · Giảng và đọc thơ: cô Hà"}
        ghi_js(f'{GOC}/data/lentam/bai{n:02d}.js', f"/* Lên Tám – Bài {n} (khổ {a}–{b}). Khung: thơ, cô Hà đọc thơ, lời giảng. Các phần khác đang soạn. */", B)
        ds.append({"kho": n, "khoTho": [a, b], "tieuDe": B['tieuDe'], "chuDe": B['chuDe'], "cauDau": [tho[0][0][0], tho[0][1][0]], "du": False})
        print('Lên Tám', n, 'giảng', het, 's', flush=True)
    ghi_js(f'{GOC}/data/lentam/danh-sach.js', "/* Danh sách các bài Lên Tám đã có ghi âm (mỗi bài 2 khổ) – dùng cho trang chủ góc học */", ds, "window.DANH_SACH_LENTAM")


if __name__ == '__main__':
    lam = sys.argv[1] if len(sys.argv) > 1 else 'ca-hai'
    chon = set(int(x) for x in sys.argv[2:]) or set(range(1, 33))
    if lam in ('lensau', 'ca-hai'): lensau(chon)
    if lam in ('lentam', 'ca-hai'): lentam(chon)
