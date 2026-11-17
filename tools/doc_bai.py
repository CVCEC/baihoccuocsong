import json, sys
bai, n = sys.argv[1], int(sys.argv[2])
tep = f"/home/claude/baihoccuocsong/data/{bai}/{'kho' if bai=='lensau' else 'bai'}{n:02d}.js"
s = open(tep, encoding='utf-8').read(); j = json.loads(s[s.index('{'):s.rindex('}') + 1])
print(f"== {bai} {n}: {j['tieuDe']} | {j['chuDe']} | khổ {j.get('khoTho')}")
for g in j['tho']: print('  THƠ: ' + ' / '.join(c[0] for c in g))
for i, d in enumerate(j['loiGiang']):
    print(f"[{i}] " + (d.get('vi') or 'THƠ: ' + ' / '.join(d['tho'])))
print('KỂ BỐ MẸ:', j.get('keBoMe'))
