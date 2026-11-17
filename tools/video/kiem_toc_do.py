"""Tốc độ nói (âm tiết / giây tiếng nói, không tính quãng lặng) từng câu; báo câu lệch nhiều so với trung vị cả lô."""
import json, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chia_neo as cn, tao_video as tv
nk = json.load(open('elio/nhat_ky.json'))
tat = []
for x in nk:
    a = cn.doc16(x['tep']); fr = a[:len(a)//320*320].reshape(-1, 320)
    db = 20*np.log10(np.sqrt((fr**2).mean(1))+1e-9); no, sp = np.percentile(db, 5), np.percentile(db, 90); noi = db > no+0.3*(sp-no)
    for b, n in x['bai']:
        r = json.load(open(f'elio/{b}{n:02d}/ranh.json')); _, loi = tv.kich_ban(b, n)
        for i, l in enumerate(loi, 1):
            s = tv.am_tiet(l['say'] or l['sub']); t0, t1, neo = r[str(i)]
            sp_ = noi[int(t0/0.02):int(t1/0.02)].sum()*0.02
            if s >= 6: tat.append((f'{b}{n:02d}', i, s/max(sp_, 0.1), l['sub'][:55], neo))
m = np.median([t[2] for t in tat]); print('trung vị', round(m, 2), 'âm tiết/giây')
bao = {}
for t in tat:
    if not t[4] and not (0.72*m < t[2] < 1.38*m): bao.setdefault(t[0], []).append(t)
for k, v in bao.items():
    print(k, '; '.join(f"{t[1]}:{t[2]:.1f}{'N' if t[4] else ''}" for t in v))
print(len(bao), 'bài cần xem')
