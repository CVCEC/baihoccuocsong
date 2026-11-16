"""Sinh js/canh-tap-the.js: banner khu tập thể Việt Nam cho góc Bài học cuộc sống.
Vẽ phẳng kiểu sách tranh, màu lấy từ lớp CSS (biến --ttv-*). viewBox 1200×260, neo đáy, giữa thấp để chừa chỗ cho tên trang."""

W, H = 1200, 200
NEN = 188  # mặt sân (đáy banner nằm ngay trên mép thẻ nội dung)


def r(x, y, w, h, c, extra=''):
    return f'<rect class="{c}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{extra}/>'


def khu_nha(x, w, tang, cao_tang, lop_tuong, lat=False, mau_phoi=('mai', 'vang', 'troi')):
    """Một dãy nhà tập thể: tầng, cửa sổ, ban công 'chuồng cọp', chậu cây, dây phơi."""
    cao = tang * cao_tang + 14
    y0 = NEN - cao
    s = r(x, y0, w, cao, lop_tuong)
    s += r(x - 6, y0 - 8, w + 12, 10, 'mai-nha')                     # mái bằng, gờ mái
    s += r(x + w * .18, y0 - 30, 34, 22, 'bon-nuoc', ' rx="4"')      # bồn nước trên mái
    s += f'<path class="day-dien" d="M{x + w * .72:.1f} {y0 - 8} v-34 M{x + w * .72 - 16:.1f} {y0 - 36} h32 M{x + w * .72 - 10:.1f} {y0 - 28} h20"/>'  # ăng-ten TV
    cot = max(2, int(w // 62))
    buoc = w / cot
    for t in range(tang):
        yt = y0 + 10 + t * cao_tang
        s += r(x, yt + cao_tang - 4, w, 3, 'vien-tang')
        for c in range(cot):
            cx = x + c * buoc + buoc / 2
            if (t + c + (1 if lat else 0)) % 3 == 0 and t < tang - 1:
                # ban công chuồng cọp nhô ra
                bx, bw, bh = cx - 24, 48, cao_tang * .62
                by = yt + cao_tang - 4 - bh
                s += r(bx, by, bw, bh, 'cua-toi')
                s += f'<path class="chuong-cop" d="M{bx:.1f} {by:.1f} h{bw} v{bh:.1f} h-{bw} Z ' + ' '.join(f'M{bx + k * 8:.1f} {by:.1f} v{bh:.1f}' for k in range(1, 6)) + f' M{bx:.1f} {by + bh / 2:.1f} h{bw}"/>'
                s += f'<path class="la-cay" d="M{bx + 6:.1f} {by + bh:.1f} q4 -14 10 -2 q6 -14 10 2 Z"/>'
                s += r(bx + 8, by + bh - 6, 14, 6, 'chau')
            else:
                s += r(cx - 13, yt + 6, 26, cao_tang * .55, 'cua-so', ' rx="2"')
                s += f'<path class="khung-cua" d="M{cx:.1f} {yt + 6:.1f} v{cao_tang * .55:.1f}"/>'
        if t == 1 or (t == 3 and tang > 4):
            # dây phơi quần áo giữa hai ô
            yy = yt + cao_tang * .62
            x1, x2 = x + 8, x + w - 8
            s += f'<path class="day-phoi" d="M{x1:.1f} {yy:.1f} Q{(x1 + x2) / 2:.1f} {yy + 6:.1f} {x2:.1f} {yy:.1f}"/>'
            for k, m in enumerate(mau_phoi * 2):
                ax = x1 + 18 + k * (x2 - x1 - 40) / 5
                if k % 2 == 0:
                    s += f'<path class="{m}" d="M{ax - 7:.1f} {yy + 3:.1f} h14 l3 7 h-4 v10 h-12 v-10 h-4 Z"/>'   # áo
                else:
                    s += r(ax - 6, yy + 3, 12, 14, m, ' rx="2"')                                                  # khăn
    s += r(x + w / 2 - 16, NEN - 34, 32, 34, 'cua-toi')               # lối cầu thang
    return s, y0


def meo(x, y, k=1.0):
    """Mèo ngồi (nhìn nghiêng ba phần tư)."""
    return (f'<g transform="translate({x} {y}) scale({k})">'
            '<path class="long-meo" d="M-11 0 Q-14 -18 0 -20 Q14 -18 11 0 Z"/>'
            '<path class="duoi" d="M10 -2 Q24 -2 22 -16" />'
            '<circle class="long-meo" cx="0" cy="-26" r="9"/>'
            '<path class="long-meo" d="M-8 -31 l2 -9 l6 6 Z M8 -31 l-2 -9 l-6 6 Z"/>'
            '<circle class="mat" cx="-3.5" cy="-27" r="1.4"/><circle class="mat" cx="3.5" cy="-27" r="1.4"/>'
            '<path class="mui" d="M-1.5 -23.5 h3 l-1.5 1.8 Z"/>'
            '</g>')


def cho(x, y, k=1.0):
    """Chó nằm/ngồi vẫy đuôi."""
    return (f'<g transform="translate({x} {y}) scale({k})">'
            '<rect class="long-cho" x="-26" y="-20" width="44" height="20" rx="10"/>'
            '<rect class="long-cho" x="-22" y="-6" width="7" height="8" rx="3"/><rect class="long-cho" x="6" y="-6" width="7" height="8" rx="3"/>'
            '<path class="duoi-cho" d="M-25 -14 Q-36 -22 -32 -32"/>'
            '<circle class="long-cho" cx="20" cy="-26" r="12"/>'
            '<path class="tai-cho" d="M12 -34 Q8 -22 14 -18 Q18 -26 16 -34 Z"/>'
            '<ellipse class="mom-cho" cx="29" cy="-22" rx="6" ry="4.5"/>'
            '<circle class="mat" cx="22" cy="-29" r="1.6"/><circle class="mat" cx="34" cy="-23" r="1.8"/>'
            '</g>')


def ga_mai(x, y, k=1.0):
    return (f'<g transform="translate({x} {y}) scale({k})">'
            '<path class="long-ga" d="M-14 -10 Q-16 -26 0 -24 Q8 -24 12 -16 L14 -20 Q20 -24 18 -14 Q16 -2 2 0 Q-12 0 -14 -10 Z"/>'
            '<path class="duoi-ga" d="M-13 -14 Q-24 -24 -20 -32 Q-14 -22 -10 -20 Z"/>'
            '<path class="mao-ga" d="M13 -24 q2 -6 5 -2 q3 -4 4 2 Z"/>'
            '<path class="mo-ga" d="M20 -18 l6 2 l-6 2 Z"/>'
            '<circle class="mat" cx="17" cy="-19" r="1.3"/>'
            '<path class="chan" d="M-2 0 v6 M4 0 v6"/>'
            '</g>')


def ga_con(x, y):
    return (f'<g transform="translate({x} {y})"><circle class="ga-con" cx="0" cy="-6" r="6"/><circle class="ga-con" cx="5" cy="-12" r="4"/>'
            '<path class="mo-ga" d="M8.5 -12.5 l3 1 l-3 1 Z"/><circle class="mat" cx="6" cy="-13" r=".9"/></g>')


def chim_se(x, y, quay=1):
    return (f'<g transform="translate({x} {y}) scale({quay} 1)"><ellipse class="long-chim" cx="0" cy="-5" rx="6" ry="4.5"/>'
            '<circle class="long-chim" cx="5" cy="-9" r="3.2"/><path class="duoi-chim" d="M-5 -5 l-6 -3 l1 5 Z"/>'
            '<path class="mo-ga" d="M7.8 -9.5 l2.6 1 l-2.6 1 Z"/><circle class="mat" cx="6" cy="-9.6" r=".8"/></g>')


def bo_cau(x, y):
    return (f'<g transform="translate({x} {y})"><ellipse class="long-bo-cau" cx="0" cy="-7" rx="10" ry="6.5"/>'
            '<circle class="long-bo-cau" cx="8" cy="-14" r="4.5"/><path class="co-bo-cau" d="M5 -11 q3 3 6 0 v3 q-3 2 -6 0 Z"/>'
            '<path class="duoi-chim" d="M-9 -8 l-7 -2 l2 6 Z"/><path class="mo-ga" d="M12 -14.5 l3 1 l-3 1 Z"/>'
            '<circle class="mat" cx="9" cy="-15" r=".9"/><path class="chan" d="M-1 -1 v2 M3 -1 v2"/></g>')


def cay_bang(x, y, cao):
    s = f'<path class="than-cay" d="M{x - 7} {y} q3 -{cao * .5} 0 -{cao} h12 q-4 {cao * .5} 2 {cao} Z"/>'
    for dx, dy, rr in [(-34, -cao - 8, 30), (0, -cao - 26, 36), (34, -cao - 6, 30), (-14, -cao + 8, 24), (18, -cao + 10, 24)]:
        s += f'<circle class="tan-cay" cx="{x + dx}" cy="{y + dy}" r="{rr}"/>'
    for dx, dy in [(-30, -cao - 16), (10, -cao - 40), (30, -cao - 2), (-6, -cao)]:
        s += f'<circle class="tan-cay-sang" cx="{x + dx}" cy="{y + dy}" r="8"/>'
    return s


def cot_dien(x, cao):
    y = NEN - cao
    s = r(x - 4, y, 8, cao, 'cot-dien')
    s += r(x - 22, y + 10, 44, 5, 'cot-dien')
    s += f'<circle class="su" cx="{x - 18}" cy="{y + 8}" r="3"/><circle class="su" cx="{x + 18}" cy="{y + 8}" r="3"/>'
    return s, y + 8


BO_CUC = {
    'rong': dict(W=1200, lop='bh-tap-the-svg rong', nha_a=(40, 270), nha_b=(900, 260), xa=[(330, 150, 56), (470, 130, 44), (600, 160, 50), (750, 130, 60)],
                 cot=(352, 852), cay=400, ghe=436, cho=540, ga=680, chim=[(392, 0, 1), (412, 3, -1), (800, 0, -1), (780, 4, 1)], bo_cau=1010, meo=128),
    'hep': dict(W=600, lop='bh-tap-the-svg hep', nha_a=(-30, 190), nha_b=(440, 190), xa=[(150, 110, 50), (250, 100, 40), (340, 110, 56)],
                cot=(176, 424), cay=214, ghe=246, cho=320, ga=372, chim=[(200, 0, 1), (214, 3, -1), (402, 0, -1), (388, 4, 1)], bo_cau=520, meo=30),
}


def tao_svg(ten):
    b = BO_CUC[ten]; W = b['W']
    s = f'<svg class="{b["lop"]}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
    for bx, bw, bc in b['xa']:
        s += r(bx, NEN - bc, bw, bc, 'nha-xa')
        for t in range(int(bc // 22)):
            for c in range(int(bw // 34)):
                s += r(bx + 12 + c * 34, NEN - bc + 10 + t * 22, 14, 10, 'cua-xa')
    s += r(0, NEN - 4, W, H - NEN + 4, 'san')
    a, ya = khu_nha(b['nha_a'][0], b['nha_a'][1], 5, 31, 'tuong-a')
    bb, yb = khu_nha(b['nha_b'][0], b['nha_b'][1], 5, 30, 'tuong-b', lat=True, mau_phoi=('troi', 'mai', 'vang'))
    s += a + bb
    x1, x2 = b['cot']
    c1, d1 = cot_dien(x1, 118)
    c2, d2 = cot_dien(x2, 118)
    s += c1 + c2
    ra = b['nha_a'][0] + b['nha_a'][1]; lb = b['nha_b'][0]
    s += f'<path class="day-dien" d="M{ra} {ya + 40} Q{ra + 20} {d1 + 10} {x1 - 18} {d1} M{ra} {ya + 60} Q{ra + 20} {d1 + 20} {x1 + 18} {d1}"/>'
    s += f'<path class="day-dien" d="M{lb} {yb + 40} Q{lb - 20} {d2 + 10} {x2 + 18} {d2} M{lb} {yb + 62} Q{lb - 20} {d2 + 22} {x2 - 18} {d2}"/>'
    s += f'<path class="day-dien" d="M{x1 - 18} {d1} Q{x1 + 68} {d1 + 26} {x1 + 118} {d1 + 30} M{x1 + 18} {d1} Q{x1 + 68} {d1 + 18} {x1 + 108} {d1 + 22}"/>'
    s += f'<path class="day-dien" d="M{x2 + 18} {d2} Q{x2 - 62} {d2 + 26} {x2 - 112} {d2 + 30} M{x2 - 18} {d2} Q{x2 - 62} {d2 + 18} {x2 - 102} {d2 + 22}"/>'
    for cx, dy, q in b['chim']:
        s += chim_se(cx, (d1 if cx < W / 2 else d2) + 15 + dy, q)
    s += cay_bang(b['cay'], NEN, 46)
    g = b['ghe']
    s += r(g, NEN - 14, 52, 6, 'ghe-da', ' rx="3"') + r(g + 6, NEN - 9, 6, 9, 'ghe-da') + r(g + 40, NEN - 9, 6, 9, 'ghe-da')
    s += meo(b['meo'] + (128 - 40 if ten == 'rong' else 70), ya + 10 + 31 * 2 - 4 - 31 * .62 + 0.5, .8)
    s += bo_cau(b['bo_cau'], yb - 8)
    s += cho(b['cho'], NEN, .85)
    x = b['ga']
    s += ga_mai(x, NEN) + ga_con(x + 26, NEN) + ga_con(x + 40, NEN) + ga_con(x + 14, NEN)
    s += '</svg>'
    return s


CSS_GHI_CHU = 'màu trong css/bai.css (.bh-tap-the …)'

if __name__ == '__main__':
    svg = tao_svg('rong') + tao_svg('hep')
    js = ('/* Banner "khu tập thể" của góc Bài học cuộc sống – vẽ phẳng kiểu sách tranh, sinh từ tools/ve_tap_the.py.\n'
          '   Màu lấy từ biến --ttv-* qua lớp CSS trong css/bai.css. Trâu Con vẫn là ảnh chính thức trong trang. */\n'
          '(function () {\n'
          '  var SVG = ' + repr(svg).replace("\\'", "'") + ';\n'
          '  function ve() {\n'
          '    var ds = document.querySelectorAll(".bh-dau");\n'
          '    for (var i = 0; i < ds.length; i++) {\n'
          '      if (ds[i].querySelector(".bh-tap-the")) continue;\n'
          '      var d = document.createElement("div"); d.className = "bh-tap-the"; d.setAttribute("aria-hidden", "true"); d.innerHTML = SVG;\n'
          '      ds[i].appendChild(d);\n'
          '      var san = document.createElement("div"); san.className = "bh-tap-the-san"; san.setAttribute("aria-hidden", "true"); ds[i].appendChild(san);\n'
          '      var nhan = document.createElement("p"); nhan.className = "bh-tap-the-ten"; nhan.textContent = "Khu tập thể"; ds[i].appendChild(nhan);\n'
          '    }\n'
          '  }\n'
          '  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ve); else ve();\n'
          '})();\n')
    open('/home/claude/baihoccuocsong/js/canh-tap-the.js', 'w', encoding='utf-8').write(js)
    open('/home/claude/scratch/tap_the.svg', 'w').write(svg)
    print(len(js))
