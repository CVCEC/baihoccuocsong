"""Ghép nội dung đã soạn (noidung/<bai>/NN.json) vào data/<bai>/...NN.js; kiểm tra đủ phần theo chuẩn Bài 1."""
import json, sys, re, unicodedata
GOC = '/home/claude/baihoccuocsong'
CAN = ['tieuDeEn', 'dichXuoi', 'tuKho', 'cauHoi', 'viet', 'baiHoc', 'baiHocEn', 'viecTot', 'en']

def nfc(x):
    if isinstance(x, str): return unicodedata.normalize('NFC', x)
    if isinstance(x, list): return [nfc(i) for i in x]
    if isinstance(x, dict): return {k: nfc(v) for k, v in x.items()}
    return x

def ghep(bai, n, kiem_hinh=None):
    tep = f"{GOC}/data/{bai}/{'kho' if bai == 'lensau' else 'bai'}{n:02d}.js"
    s = open(tep, encoding='utf-8').read(); dau = s[:s.index('window.BAI_HOC')]
    B = json.loads(s[s.index('{'):s.rindex('}') + 1])
    N = nfc(json.load(open(f'/home/claude/noidung/{bai}/{n:02d}.json', encoding='utf-8')))
    thieu = [k for k in CAN if k not in N]
    assert not thieu, f'{bai} {n} thiếu {thieu}'
    assert len(N['en']) == len(B['loiGiang']), f"{bai} {n}: en {len(N['en'])} ≠ lời giảng {len(B['loiGiang'])}"
    assert len(N['dichXuoi']) == len(B['tho']), f"{bai} {n}: dịch xuôi {len(N['dichXuoi'])} ≠ nhóm thơ {len(B['tho'])}"
    for q in N['cauHoi']:
        assert 0 <= q['dung'] < len(q['chon']) and len(q['chon']) == 3, q
    for d, e in zip(B['loiGiang'], N['en']): d['en'] = e
    for k in ['tieuDeEn', 'dichXuoi', 'tuKho', 'cauHoi', 'viet', 'baiHoc', 'baiHocEn', 'viecTot']: B[k] = N[k]
    if 'keBoMe' in N: B['keBoMe'] = N['keBoMe']
    B['du'] = True
    dau = re.sub(r'Khung: thơ, cô Hà đọc thơ, lời giảng\. Các phần khác đang soạn\.', 'Đủ bài.', dau)
    open(tep, 'w', encoding='utf-8').write(dau + 'window.BAI_HOC = ' + json.dumps(B, ensure_ascii=False, indent=1) + ';\n')
    # cập nhật danh sách trang chủ
    ds_tep = f'{GOC}/data/{bai}/danh-sach.js'; d = open(ds_tep, encoding='utf-8').read()
    ds = json.loads(d[d.index('['):d.rindex(']') + 1])
    for k in ds:
        if k['kho'] == n: k['du'] = True
    open(ds_tep, 'w', encoding='utf-8').write(d[:d.index('[')] + json.dumps(ds, ensure_ascii=False, indent=1) + ';\n')
    return [c[1] for q in N['cauHoi'] for c in q['chon']]

if __name__ == '__main__':
    bai = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        h = ghep(bai, n); print(bai, n, 'xong;', len(h), 'tranh')
