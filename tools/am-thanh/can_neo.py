"""Căn giờ bản ghi mới bằng 'neo' câu thơ chuyển từ bản căn cũ (câu thơ đã kiểm cao độ),
rồi căn văn xuôi giữa các neo bằng quy hoạch động trên từng đoạn âm thanh con."""
import sys, json, os, subprocess, tempfile
import numpy as np
sys.path.insert(0, '/home/claude/tools')
from can_gio import can, nang_luong, am_tiet
from can_moi import chuan_bi_moi
from doi_chieu import mel
from scipy.io import wavfile


def tim_neo(A, B, bd, kt, du_doan, R=25.0):
    """Tìm đoạn [bd,kt] của bản cũ (đặc trưng A) trong bản mới (B) quanh vị trí dự đoán."""
    i0, i1 = int((bd - 0.3) / 0.02), int((kt + 0.3) / 0.02)
    a = A[i0:i1]; an = (a - a.mean()) / (a.std() + 1e-9); W = len(a)
    tot = (-9, 0)
    lo = max(0, int((du_doan - R) / 0.02)); hi = min(len(B) - W, int((du_doan + R) / 0.02))
    for j in range(lo, hi):
        b = B[j:j + W]; bn = (b - b.mean()) / (b.std() + 1e-9)
        r = (an * bn).mean()
        if r > tot[0]: tot = (r, j)
    return tot[0], (tot[1] - i0) * 0.02   # độ lệch mới - cũ


def can_doan_con(wav, a, b, don_vi):
    sr, x = wavfile.read(wav)
    seg = x[int(a * sr):int(b * sr)]
    fd, p = tempfile.mkstemp(suffix='.wav'); os.close(fd)
    wavfile.write(p, sr, seg)
    dv, r = can(p, [dict(u) for u in don_vi])
    os.remove(p)
    for u in dv:
        u['bd'] = round(u['bd'] + a, 2); u['kt'] = round(u['kt'] + a, 2)
    return dv


def chay(goc_moi, goc_cu, n, kich_ban):
    k = [x for x in kich_ban if x['so'] == n][0]
    doan, dv, cau_hoi = chuan_bi_moi(k['doan'])
    cu = json.load(open(f'{goc_cu}/can_kho{n:02d}.json'))
    tho_cu = [u for u in cu['dv'] if u['tho'] and not u.get('duoi')]
    wav_moi, wav_cu = f'{goc_moi}/wav/kho{n:02d}.wav', f'{goc_cu}/wav/kho{n:02d}.wav'
    A, B = mel(wav_cu), mel(wav_moi)
    tho_moi = [u for u in dv if u['tho']]
    assert [u['chu'] for u in tho_moi] == [u['chu'] for u in tho_cu], 'thơ khác nhau'
    lech = -0.04; canh = []
    for um, uc in zip(tho_moi, tho_cu):
        r, d = tim_neo(A, B, uc['bd'], uc['kt'], uc['bd'] + lech)
        if r < 0.7: canh.append(f"neo yếu {uc['chu']} r={r:.2f}")
        um['bd'] = round(uc['bd'] + d, 2); um['kt'] = round(uc['kt'] + d, 2); lech = d
    # trọng tài từng nhóm thơ: neo cũ hay căn DP mới, chọn bên có độ dài câu hợp lý
    dp = json.load(open(f'{goc_moi}/can_dp/can_kho{n:02d}.json'))
    tho_dp = [u for u in dp['dv'] if u['tho']]
    def phat(ds):
        p = 0
        for u in ds:
            d = u['kt'] - u['bd']
            p += max(0, 0.65 - d) * 4 + max(0, d - 1.6) * 2
        for x, y in zip(ds, ds[1:]):
            g = y['bd'] - x['kt']
            p += max(0, g - 1.2)
        return p
    nhom = {}
    for i, u in enumerate(tho_moi): nhom.setdefault(u['doan'], []).append(i)
    for g, idx in nhom.items():
        a = [tho_moi[i] for i in idx]; b = [tho_dp[i] for i in idx]
        pa, pb = phat(a), phat(b)
        if pb + 0.3 < pa:
            canh.append(f"nhóm thơ '{a[0]['chu']}': dùng căn mới (phạt {pa:.1f} → {pb:.1f})")
            for i in idx: tho_moi[i]['bd'], tho_moi[i]['kt'] = tho_dp[i]['bd'], tho_dp[i]['kt']
    s, _ = nang_luong(wav_moi)
    het = (len(s) - int(np.argmax(s[::-1]))) / 100
    bat = int(np.argmax(s)) / 100
    # chia đơn vị văn xuôi thành các cụm giữa neo thơ
    cum, cur, mo = [], [], bat
    for u in dv:
        if u['tho']:
            if cur: cum.append((mo, u['bd'], cur)); cur = []
            mo = u['kt']
        else:
            cur.append(u)
    if cur: cum.append((mo, het + 0.05, cur))
    for a, b, ds in cum:
        a2 = max(0, a - 0.05); b2 = b + 0.05
        if len(ds) == 1:
            ds[0]['bd'], ds[0]['kt'] = round(a + 0.0, 2), round(b, 2)
            # bỏ khoảng lặng đầu
            i = int(a * 100)
            while i < len(s) and not s[i] and i < b * 100: i += 1
            ds[0]['bd'] = round(i / 100, 2)
        else:
            ra = can_doan_con(wav_moi, a2, b2, ds)
            for u, v in zip(ds, ra): u['bd'], u['kt'] = v['bd'], v['kt']
    bd = {}
    for u in dv: bd.setdefault(u['doan'], u['bd'])
    for q, d in enumerate(doan): d['t'] = round(bd.get(q, 0), 2)
    out = {'so': n, 'tieu_de': k['tieu_de'], 'doan': doan, 'dv': dv, 'cau_hoi': cau_hoi, 'het': round(het + 0.12, 2)}
    json.dump(out, open(f'{goc_moi}/can_kho{n:02d}.json', 'w'), ensure_ascii=False, indent=1)
    return out, canh


if __name__ == '__main__':
    goc_moi, goc_cu = sys.argv[1], sys.argv[2]
    kb = json.load(open(f'{goc_moi}/kich_ban_moi.json'))
    for n in [int(x) for x in sys.argv[3:]] or range(1, 19):
        out, canh = chay(goc_moi, goc_cu, n, kb)
        ds = out['doan']; ends = [d['t'] for d in ds[1:]] + [out['het']]
        rate = []
        for d, e in zip(ds, ends):
            t = d.get('vi') or ' '.join(d['tho']); rate.append(('T' if 'tho' in d else '') + f"{(e - d['t']) / am_tiet(t):.2f}")
        print(n, ' '.join(rate), canh, flush=True)
