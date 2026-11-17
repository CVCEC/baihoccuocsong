"""Cắt giọng Elio theo mốc: tìm các câu cố định lặp lại trong mọi bài (chào, "Các bạn cùng
nghe cô Hà…", "Các bạn đọc theo mình nhé"…) bằng DTW trên phổ mel, rồi chia các câu còn lại
giữa hai mốc theo quãng lặng và số âm tiết.

  python3 chia_neo.py mau                     # lấy mẫu câu cố định từ bài sạch
  python3 chia_neo.py <số lần 1..18> …        # cắt lại các lần tạo giọng
"""
import os, sys, json, subprocess, re
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

GOC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GOC)
import tao_video as tv

CO_DINH = ["Xin chào các bạn! Mình là Trâu Con.", "Các bạn cùng nghe cô Hà đọc thơ nhé!",
           "Bây giờ, mình kể lại bằng lời dễ hiểu nhé.", "Các bạn đọc theo mình nhé:", "Các bạn hãy nhớ nhé:",
           "Bây giờ, các bạn nghe cô Hà giảng, trả lời câu hỏi, rồi viết vài câu thật hay nhé!", "Hẹn gặp lại các bạn!"]
HOP = 0.02


def doc16(p):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", "16000", "/tmp/_n16.wav"], check=True)
    sr, x = wavfile.read("/tmp/_n16.wav"); return x.astype(np.float32) / 32768


def mel(x, sr=16000):
    f, t, Z = stft(x, sr, nperseg=512, noverlap=512 - 320)
    S = np.abs(Z) ** 2
    ed = np.geomspace(80, 7000, 31)
    B = np.stack([S[(f >= ed[i]) & (f < ed[i + 1])].sum(0) for i in range(30)])
    return np.log(B + 1e-7).T  # (khung, 30)


def chuan_hoa(F, mu, sd):
    G = (F - mu) / sd
    return G / (np.linalg.norm(G, axis=1, keepdims=True) + 1e-9)


def sdtw(T, A):
    """DTW tìm đoạn con: trả về (chi phí trung bình, khung bắt đầu) cho mỗi khung kết thúc."""
    C = 1 - T @ A.T  # (M, N)
    M, N = C.shape; INF = 1e9
    D = np.full((M, N), INF, np.float32); S = np.zeros((M, N), np.int32)
    D[0] = C[0]; S[0] = np.arange(N)
    for i in range(1, M):
        c1 = np.full(N, INF, np.float32); s1 = np.zeros(N, np.int32)
        c1[1:] = D[i - 1, :-1]; s1[1:] = S[i - 1, :-1]                     # (1,1)
        c2 = np.full(N, INF, np.float32); s2 = np.zeros(N, np.int32)
        c2[2:] = D[i - 1, :-2] + C[i, 1:-1]; s2[2:] = S[i - 1, :-2]        # (1,2)
        c3 = np.full(N, INF, np.float32); s3 = np.zeros(N, np.int32)
        if i >= 2: c3[1:] = D[i - 2, :-1] + C[i - 1, 1:]; s3[1:] = S[i - 2, :-1]  # (2,1)
        st = np.stack([c1, c2, c3]); k = st.argmin(0)
        D[i] = st[k, np.arange(N)] + C[i]; S[i] = np.choose(k, [s1, s2, s3])
    return D[-1] / M, S[-1]


def ung_vien(T, A, toi_da=0.45):
    d, s = sdtw(T, A)
    out = []
    for j in range(2, len(d) - 2):
        if d[j] < toi_da and d[j] <= d[j - 2:j + 3].min():
            out.append((float(d[j]), int(s[j]), j + 1))
    out.sort(); kept = []
    for c in out:  # bỏ các ứng viên chồng nhau
        if all(c[2] <= k[1] or c[1] >= k[2] for k in kept): kept.append(c)
    return sorted(kept, key=lambda c: c[1])


def lay_mau():
    """Mẫu câu cố định lấy từ lentam05 (bài có độ dài các câu đều chuẩn)."""
    _, loi = tv.kich_ban("lentam", 5)
    mau = {}
    for i, x in enumerate(loi, 1):
        if x["sub"] in CO_DINH:
            mau[x["sub"]] = mel(doc16(os.path.join(GOC, "elio", "lentam05", f"{i:02d}.wav"))).tolist()
    json.dump(mau, open(os.path.join(GOC, "elio", "mau_co_dinh.json"), "w"))
    print("đã lấy", len(mau), "mẫu")


SPS = 0.30   # giây/âm tiết ước lượng (chỉ để chọn mốc)
NGHI = 0.55  # giây nghỉ ước lượng giữa hai câu


def chon_neo(cau, uv, w0):
    """Chọn mốc theo thứ tự trong một bài: phạt lệch khoảng cách giữa hai mốc so với ước lượng."""
    syl = [tv.am_tiet(c["doc"]) for c in cau]
    neo_i = [k for k, c in enumerate(cau) if uv.get(k)]
    best = {(-1, -1): (0.0, None, w0)}
    for k in neo_i:
        moi = {}
        for ci, c in enumerate(uv[k]):
            for key, (sc, _, het) in best.items():
                if c[1] < het: continue
                k0 = key[0]
                e = sum(syl[m] * SPS + (0.9 if syl[m] <= 3 else NGHI) for m in range(k0 + 1, k)) + (0.3 if k0 >= 0 else 0)
                g = (c[1] - het) * HOP
                v = sc + 6.0 * c[0] + 0.5 * ((g - e) / max(e, 2.0)) ** 2
                if (k, ci) not in moi or v < moi[(k, ci)][0]: moi[(k, ci)] = (v, key, c[2])
        if moi:
            best = {kk: (v, (key, best[key]), het) for kk, (v, key, het) in moi.items()}
            # cho phép bỏ qua mốc này: giữ lại các trạng thái cũ với phạt
    key = min(best, key=lambda kk: best[kk][0]); node = best[key]; neo = {}
    while key[0] >= 0:
        c = uv[key[0]][key[1]]; neo[key[0]] = (c[1], c[2], c[0])
        key, node = node[1][0], node[1][1]
    return neo


def _mfcc(x):
    from scipy.fft import dct
    C = dct(mel(x), type=2, axis=1, norm="ortho")[:, 1:14]
    return (C - C.mean(0)) / (C.std(0) + 1e-6)


def _dtw_path(A, B):
    D = np.sqrt(np.maximum(0, (A ** 2).sum(1)[:, None] + (B ** 2).sum(1)[None, :] - 2 * A @ B.T))
    n, m = D.shape; C = np.full((n + 1, m + 1), np.inf); C[0, 0] = 0
    for i in range(1, n + 1):
        base = D[i - 1] + np.minimum(C[i - 1, :-1], C[i - 1, 1:]); out = np.empty(m); out[0] = base[0]
        for j in range(1, m): out[j] = min(base[j], D[i - 1, j] + out[j - 1])
        C[i, 1:] = out
    i, j = n, m; path = []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1)); k = int(np.argmin([C[i - 1, j - 1], C[i - 1, j], C[i, j - 1]]))
        if k == 0: i, j = i - 1, j - 1
        elif k == 1: i -= 1
        else: j -= 1
    return np.array(path[::-1])


def du_doan(x16, cau, k0, k1, tu, den):
    """Dùng giọng máy espeak làm thước: DTW với đoạn giọng Elio để đoán ranh giới giữa các câu (khung)."""
    import espeak_vi as ev
    from scipy.signal import resample_poly
    phan = []; mo = []; n = 0
    for c in cau[k0:k1]:
        y = resample_poly(ev.noi(c["doc"]), 320, 441).astype(np.float32); phan += [y, np.zeros(4800, np.float32)]
        n += len(y); mo.append(n + 2400); n += 4800
    R = np.concatenate(phan); W = x16[tu * 320: den * 320]
    if len(W) < 3200: return None
    p = _dtw_path(_mfcc(R), _mfcc(W))
    out = []
    for b in mo[:-1]:
        fi = min(int(b / 320), p[:, 0].max()); js = p[p[:, 0] == fi, 1]
        out.append(tu + int(np.median(js)))
    return out


def chia_giua(cau, noi, tu, den, k0, k1, bien, x16=None):
    """Chia các câu k0..k1-1 trong khoảng khung [tu, den) theo quãng lặng và số âm tiết."""
    ss = [tv.am_tiet(c["doc"]) for c in cau[k0:k1]]; n = k1 - k0
    lang = []; i = tu
    while i < den:
        if not noi[i]:
            e = i
            while e < den and not noi[e]: e += 1
            if e - i >= 6: lang.append((i, e))
            i = e
        else: i += 1
    cand = [(tu, tu)] + lang + [(den, den)]; K = len(cand); INF = 1e18
    r = 0.5 * (max(1, noi[tu:den].sum()) * HOP / sum(ss)) + 0.5 / 3.67  # nửa theo cửa sổ, nửa theo tốc độ chung
    dd = du_doan(x16, cau, k0, k1, tu, den) if (x16 is not None and n >= 2) else None
    dai = sorted([(e - s_) * HOP for s_, e in lang], reverse=True)
    wref = max(0.3, float(np.median(dai[:max(1, n - 1)]))) if dai else 0.5
    dp = np.full((n + 1, K), INF); bk = np.zeros((n + 1, K), int); dp[0][0] = 0
    for l in range(1, n + 1):
        e = r * ss[l - 1]
        for b in range(1, K):
            for a in range(0, b):
                if dp[l - 1][a] >= INF: continue
                d = noi[cand[a][1]:cand[b][0]].sum() * HOP
                if d <= 0.15: continue
                w = (cand[b][1] - cand[b][0]) * HOP
                c = dp[l - 1][a] + 8.0 * np.log(d / e) ** 2 - (1.0 * min(w / wref, 1.2) if l < n else 0)
                if dd is not None and l < n:
                    c += ((((cand[b][0] + cand[b][1]) / 2 - dd[l - 1]) * HOP) / 0.6) ** 2
                if c < dp[l][b]: dp[l][b] = c; bk[l][b] = a
    b = K - 1; seg = []
    for l in range(n, 0, -1):
        a = bk[l][b]; seg.append((cand[a][1], cand[b][0])); b = a
    for l, sg in enumerate(seg[::-1]): bien[k0 + l] = sg


def cat(lan, khoi=None, het_khoi=None):
    nk = json.load(open(os.path.join(GOC, "elio", "nhat_ky.json")))[lan - 1]
    p = os.path.join(GOC, nk["tep"]); ds = [tuple(b) for b in nk["bai"]]
    x = doc16(p); F = mel(x); mu, sd = F.mean(0), F.std(0) + 1e-6
    A = chuan_hoa(F, mu, sd); N = len(A)
    mau = {k: chuan_hoa(np.array(v), mu, sd) for k, v in json.load(open(os.path.join(GOC, "elio", "mau_co_dinh.json"))).items()}
    fr = x[: len(x) // 320 * 320].reshape(-1, 320)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    noise, spk = np.percentile(db, 5), np.percentile(db, 90); noi = db > noise + 0.3 * (spk - noise)
    # khung từng bài: bắt đầu ở câu chào
    chao = ung_vien(mau[CO_DINH[0]], A, 0.22)
    if len(chao) < len(ds): chao = ung_vien(mau[CO_DINH[0]], A, 0.32)
    if khoi is None:
        # chọn n câu chào: câu đầu sớm nhất, các câu sau gần độ dài ước lượng của bài trước
        bd = [min(chao, key=lambda c: c[1])]
        for b, n in ds[1:]:
            _, loi = tv.kich_ban(*ds[len(bd) - 1])
            e = sum(tv.am_tiet(l["say"] or l["sub"]) * SPS + NGHI for l in loi) * 1.0
            sau = [c for c in chao if c[1] > bd[-1][2] + 20 / HOP]
            bd.append(min(sau, key=lambda c: abs((c[1] - bd[-1][1]) * HOP - e) / e + c[0]))
        khoi = [c[1] * HOP for c in bd]
    khoi_f = [int(t / HOP) for t in khoi]
    if het_khoi is None:
        het_khoi = khoi_f[1:] + [N]
    else: het_khoi = [int(t / HOP) if t else N for t in het_khoi]
    chuan = "/tmp/_n_chuan.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", "24000", "-af", "loudnorm=I=-18:TP=-2:LRA=11", chuan], check=True)
    print(f"lần {lan:02d}: khung bài", [round(t, 1) for t in khoi], [round(t * HOP, 1) for t in het_khoi])
    for (b, n), w0, w1 in zip(ds, khoi_f, het_khoi):
        _, loi = tv.kich_ban(b, n)
        cau = [dict(i=i, sub=l["sub"], doc=l["say"] or l["sub"]) for i, l in enumerate(loi, 1)]
        Aw = A[w0:w1]
        uv = {}
        for k, c in enumerate(cau):
            if c["sub"] in mau:
                uv[k] = [(s, a + w0, z + w0) for s, a, z in ung_vien(mau[c["sub"]], Aw, 0.34)]
        neo = chon_neo(cau, uv, w0)
        bien = {k: (a, z) for k, (a, z, _) in neo.items()}
        # câu cuối "Hẹn gặp lại" không thấy thì lấy hết phần còn lại
        k = 0
        while k < len(cau):
            if k in bien: k += 1; continue
            j = k
            while j < len(cau) and j not in bien: j += 1
            tu = bien[k - 1][1] if k - 1 in bien else w0
            if j in bien: den = bien[j][0]
            else:
                den = min(w1, len(noi))
                while den > tu and not noi[den - 1]: den -= 1
            chia_giua(cau, noi, tu, den, k, j, bien, x); k = j
        bao = []
        for k, c in enumerate(cau):
            a, z = bien[k]; nn = noi[a:z].sum() * HOP; e = tv.am_tiet(c["doc"]) * SPS * 0.9
            if not (0.5 < nn / e < 1.8): bao.append(f"{c['i']:02d}{' NEO' if k in neo else '    '} nói {nn:.2f}s mong {e:.2f}s {c['sub'][:40]}")
            thu = os.path.join(GOC, "elio", f"{b}{n:02d}"); os.makedirs(thu, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, a * HOP - 0.05):.3f}", "-to", f"{z * HOP + 0.12:.3f}", "-i", chuan,
                            "-af", "afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse", "-c:a", "pcm_s16le", os.path.join(thu, f"{c['i']:02d}.wav")], check=True)
        json.dump({c["i"]: [round(bien[k][0] * HOP, 2), round(bien[k][1] * HOP, 2), k in neo] for k, c in enumerate(cau)},
                  open(os.path.join(GOC, "elio", f"{b}{n:02d}", "ranh.json"), "w"))
        nmau = sum(1 for c in cau if c["sub"] in mau)
        print(f"   {b}{n:02d}: mốc {len(neo)}/{nmau} (tệ nhất {max(v[2] for v in neo.values()):.2f})" + ("" if not bao else "  ⚠"))
        for x_ in bao: print("      ", x_)


if __name__ == "__main__":
    if sys.argv[1] == "mau": lay_mau()
    else:
        for a in sys.argv[1:]: cat(int(a))
