"""Căn giờ Lên Tám: mỗi bài giảng = lời mở + 2 khổ thơ (4 câu × 5 chữ) + giảng; cắt câu 'Nào giờ thì ... hôm nay.'"""
import sys, json, re
import numpy as np
sys.path.insert(0, '/home/claude/tools')
import can_gio
from can_gio import am_tiet, tach_cau, nang_luong

CAT = re.compile(r'\s*(Nào giờ thì chúng ta hãy bắt đầu bài học tiếng [Vv]iệt của ngày hôm nay\.?)\s*$')


SUA = [("Đua bạn,m học", "Đua bạn, học"), ("Tư ich có", "Tư ích có"), ("Vào ra phảiu", "Vào ra phải"),
       ("cô,cậu", "cô, cậu"), ("bao nhieu người", "bao nhiêu người"), ("Bé đại như", "Bé dại như"), ("THẢO THƠN", "THẢO THƠM"),
       ("Khôn dầu bởi", "Khôn dần bởi"), ("khôn dầu bởi", "khôn dần bởi"), ("phảiu", "phải"), ("Bố mẻ đẻ", "Bố mẹ đẻ")]


def sua(p):
    for a, b in SUA: p = p.replace(a, b)
    return p


def dong_tho(p):
    q = p.replace('“', '').replace('”', '').replace('"', '').strip()
    ds = [x.strip().rstrip() for x in q.split('\n') if x.strip()]
    if len(ds) == 4 and all(am_tiet(x) == 5 for x in ds):
        return ds
    return None


def chuan_bi(b):
    doan, dv = [], []
    for i, p in enumerate(b['doan']):
        p = sua(p)
        ds = dong_tho(p)
        if ds:
            doan.append({'tho': ds})
            for c in ds:
                dv.append({'doan': len(doan) - 1, 'tho': True, 'chu': c, 'at': am_tiet(c)})
            continue
        if i == len(b['doan']) - 1:
            m = CAT.search(p)
            if m:   # bản ghi không có câu này (đã kiểm bằng đối chiếu âm thanh giữa 32 bài)
                p = p[:m.start()].strip()
        doan.append({'vi': p})
        dv.append({'doan': len(doan) - 1, 'tho': False, 'chu': p, 'at': am_tiet(p)})
    return doan, dv


def can5(path, don_vi):
    """Như can_gio.can nhưng thời lượng câu thơ 5 chữ."""
    src = open('/home/claude/tools/can_gio.py').read()
    return can_gio.can(path, don_vi)


def lam_lai_nhom_tho(wav, dv):
    """Chia lại ranh giới các câu trong một nhóm thơ nếu có câu quá ngắn/dài: chọn ranh giới ở khoảng lặng
    (>= 0.05 s) sao cho các câu dài đều nhau."""
    s, _ = nang_luong(wav)
    nhom = {}
    for u in dv:
        if u['tho']: nhom.setdefault(u['doan'], []).append(u)
    sua_doi = []
    for g, ds in nhom.items():
        if all(1.0 <= u['kt'] - u['bd'] <= 2.6 for u in ds): continue
        a, b = int(ds[0]['bd'] * 100), int(ds[-1]['kt'] * 100)
        cand = []
        i = a
        while i < b:
            if not s[i]:
                j = i
                while j < b and not s[j]: j += 1
                if j - i >= 5: cand.append((i, j))
                i = j
            else: i += 1
        K = len(ds); m = (b - a) / K
        best = None
        from itertools import combinations
        for comb in combinations(range(len(cand)), K - 1):
            bien = [a] + [x for c in comb for x in cand[c]] + [b]
            seg = [(bien[2 * q], bien[2 * q + 1]) for q in range(K)]
            cost = sum(((y - x) - m * 0.9) ** 2 for x, y in seg) - 400 * sum(cand[c][1] - cand[c][0] for c in comb) / 100
            if best is None or cost < best[0]: best = (cost, seg)
        if best:
            for u, (x, y) in zip(ds, best[1]):
                u['bd'], u['kt'] = round(x / 100, 2), round(y / 100, 2)
            sua_doi.append(g)
    return sua_doi


if __name__ == '__main__':
    goc = '/home/claude/moi/lentam'
    kb = json.load(open(f'{goc}/kich_ban.json'))
    ds = [int(x) for x in sys.argv[1:]] or list(range(1, 33))
    for b in kb:
        n = b['so']
        if n not in ds: continue
        doan, dv = chuan_bi(b)
        so_tho = sum(1 for u in dv if u['tho'])
        wav = f'{goc}/wav/bai{n:02d}.wav'
        dv, r = can_gio.can(wav, dv)
        lam = lam_lai_nhom_tho(wav, dv)
        if lam: print('  chia lại nhóm thơ', lam)
        bd = {}
        for u in dv:
            if u['doan'] >= 0: bd.setdefault(u['doan'], u['bd'])
        for q, d in enumerate(doan): d['t'] = round(bd.get(q, 0), 2)
        cat = [u for u in dv if u.get('cat')]
        if cat:
            truoc = [u for u in dv if not u.get('cat')][-1]
            het = round(min(cat[0]['bd'], truoc['kt'] + 0.6) , 2)
            het = round(truoc['kt'] + 0.12, 2)
        else:
            s, _ = nang_luong(wav); het = round((len(s) - int(np.argmax(s[::-1]))) / 100 + 0.12, 2)
        tho = [u for u in dv if u['tho']]
        canh = [f"{u['chu']} ({u['kt'] - u['bd']:.2f}s)" for u in tho if not (1.0 <= u['kt'] - u['bd'] <= 3.0)]
        json.dump({'so': n, 'tieu_de': b['tieu_de'], 'kho': b['kho'], 'doan': doan, 'dv': dv, 'het': het, 'co_cat': bool(cat)},
                  open(f'{goc}/can_bai{n:02d}.json', 'w'), ensure_ascii=False, indent=1)
        ends = [d['t'] for d in doan[1:]] + [het]
        rate = ' '.join(('T' if 'tho' in d else '') + f"{(e - d['t']) / am_tiet(d.get('vi') or ' '.join(d['tho'])):.2f}" for d, e in zip(doan, ends))
        cu = f"cắt@{cat[0]['bd']:.1f}–{cat[0]['kt']:.1f} ({cat[0]['kt'] - cat[0]['bd']:.1f}s)" if cat else 'không có câu cắt'
        print(n, f'thơ {so_tho} câu', rate, '|', cu, '| hết', het, canh, flush=True)
