"""Kiểm tra mọi mã tranh trong noidung/ dùng tên có trong thư viện (người, vật, dấu)."""
import json, glob, re
s = open('/home/claude/baihoccuocsong/js/hinh-ghep.js', encoding='utf-8').read()
vai = set(re.findall(r'^\s{4}(\w+):\s*\{ r:', s, re.M))
vat = set(re.findall(r'^\s{4}"([a-z-]+)": function', s, re.M))
dau = {'x', 'v', 'tim', 'hoi', 'zz', 'sao-nho'}
h = open('/home/claude/baihoccuocsong/js/hinh.js', encoding='utf-8').read()
co_san = set(re.findall(r'^\s{4}"([a-z-]+)": boc', h, re.M))
loi = 0
for f in sorted(glob.glob('/home/claude/noidung/*/*.json')):
    N = json.load(open(f, encoding='utf-8'))
    for q in N.get('cauHoi', []):
        for c in q['chon']:
            ma = c[1]
            if ma in co_san: continue
            for p in ma.split('|'):
                ten = p.split(':')[0]
                if ten not in vai and ten not in vat and ten not in dau:
                    print(f.split('/')[-2:], 'không có', ten, 'trong', ma); loi += 1
print('lỗi', loi, '| người', len(vai), 'vật', len(vat))
