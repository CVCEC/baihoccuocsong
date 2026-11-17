"""Căn giờ kịch bản giảng của cô Hà với bản ghi (không có nhận dạng giọng nói).

Đơn vị căn: từng câu văn xuôi và từng câu thơ 3 chữ. Ranh giới đơn vị chỉ được đặt ở
khoảng lặng. Chi phí = sai lệch thời lượng so với dự kiến (theo số âm tiết) trừ điểm
thưởng cho khoảng lặng dài ở ranh giới. Quy hoạch động chọn ranh giới tốt nhất.
"""
import re, json, sys
import numpy as np
from scipy.io import wavfile

SUA_LOI = [("cô cô Hà", "cô Hà"), ("cốt lộ", "cốt lõi"), ("Vàng lời dặn", "Và lời dặn"),
           ("\"con trong ruột\"", "\"còn trong ruột\""), ("những món đồ chơi vỉa hè", "những món đồ ăn vỉa hè")]
CAT_TU = re.compile(r"(Bây giờ, trước khi kết thúc phần giảng|Trước khi kết thúc phần giảng|Bây giờ, cô trò chúng ta sẽ cùng nhau bước vào)")


def am_tiet(s):
    return len(re.findall(r"[0-9A-Za-zÀ-ỹđĐ]+", s))


def tach_cau(van):
    # tách câu ở . ! ? : … khi theo sau là khoảng trắng + chữ hoa hoặc ngoặc kép
    phan = re.split(r'(?<=[.!?:…])\s+(?=["“A-ZÀ-ỸĐ])', van)
    return [p.strip() for p in phan if p.strip()]


def tach_tho(trich):
    trich = trich.replace("“", "").replace("”", "").replace('"', "")
    tu = trich.replace("\n", " ").split()
    cau = []
    for i in range(0, len(tu), 3):
        cau.append(" ".join(tu[i:i + 3]))
    return cau


def chuan_bi(kho):
    """Trả về: danh sách đoạn (để hiển thị) và danh sách đơn vị (để căn giờ)."""
    doan_hien, don_vi = [], []
    cat = False
    for p in kho["doan"]:
        for a, b in SUA_LOI:
            p = p.replace(a, b)
        if cat:
            continue
        la_tho = bool(re.match(r'^["“][^"“”]*(\n["“]?[^"“”]*)*["”]\s*$', p.strip())) and am_tiet(p) % 3 == 0 and am_tiet(p) <= 24
        if la_tho:
            cau = tach_tho(p)
            doan_hien.append({"tho": cau})
            for c in cau:
                don_vi.append({"doan": len(doan_hien) - 1, "tho": True, "chu": c, "at": am_tiet(c)})
            continue
        m = CAT_TU.search(p)
        if m:
            p = p[:m.start()].strip()
            cat = True
            if not p:
                continue
        doan_hien.append({"vi": p})
        don_vi.append({"doan": len(doan_hien) - 1, "tho": False, "chu": p, "at": am_tiet(p)})
    # phần bị cắt (câu hỏi + lời kết) vẫn căn để biết điểm cắt
    duoi = []
    bat_dau = False
    for p in kho["doan"]:
        for a, b in SUA_LOI:
            p = p.replace(a, b)
        m = CAT_TU.search(p)
        if not bat_dau and m:
            bat_dau = True
            p = p[m.start():]
        if bat_dau:
            duoi.append({"doan": -1, "tho": False, "chu": p, "at": am_tiet(p), "duoi": True})
    cau_hoi = [re.sub(r"^Câu hỏi\s*\d+\s*:\s*", "", p) for p in kho["doan"] if p.startswith("Câu hỏi")]
    # Tinh chỉnh quanh điểm cắt: câu cuối trước điểm cắt và vế đầu của câu cắt thành đơn vị riêng
    if don_vi and not don_vi[-1]["tho"]:
        cuoi = don_vi.pop()
        cau = tach_cau(cuoi["chu"])
        if len(cau) > 1:
            dau = " ".join(cau[:-1])
            don_vi.append({"doan": cuoi["doan"], "tho": False, "chu": dau, "at": am_tiet(dau)})
        don_vi.append({"doan": cuoi["doan"], "tho": False, "chu": cau[-1], "at": am_tiet(cau[-1])})
    if duoi:
        dau = duoi.pop(0)
        m = re.match(r"^([^,]+,)\s*(.*)$", dau["chu"], re.S)
        them = []
        if m:
            them.append({"doan": -1, "tho": False, "chu": m.group(1), "at": am_tiet(m.group(1)), "duoi": True, "cat": True})
            them.append({"doan": -1, "tho": False, "chu": m.group(2), "at": am_tiet(m.group(2)), "duoi": True})
        else:
            dau["cat"] = True; them.append(dau)
        duoi = them + duoi
    return doan_hien, don_vi + duoi, cau_hoi


def nang_luong(path):
    from scipy.signal import butter, sosfiltfilt, find_peaks
    sr, x = wavfile.read(path)
    x = x.astype(np.float32) / 32768
    hop, win = sr // 100, int(sr * 0.025)
    n = (len(x) - win) // hop
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i * hop:i * hop + win] ** 2)) + 1e-9) for i in range(n)])
    noise, sp = np.percentile(db, 10), np.percentile(db, 90)
    thr = noise + 0.35 * (sp - noise)
    sos = butter(4, [300, 3000], btype="band", fs=sr, output="sos"); y = sosfiltfilt(sos, x)
    env = np.array([np.sqrt(np.mean(y[i * hop:i * hop + win] ** 2)) for i in range(n)])
    edb = 20 * np.log10(np.convolve(env, np.ones(5) / 5, "same") + 1e-9)
    pk, _ = find_peaks(edb, prominence=4, distance=9, height=thr)
    cum = np.zeros(n + 1, dtype=int)
    cum[pk + 1] = 1
    cum = np.cumsum(cum)
    return db > thr, cum


def can(path, don_vi):
    s, cum = nang_luong(path)
    n = len(s)
    on = int(np.argmax(s)); off = n - int(np.argmax(s[::-1]))
    # các khoảng lặng >= 0.1 s là ứng viên ranh giới
    cand = [(on, on)]
    i = on
    while i < off:
        if not s[i]:
            j = i
            while j < off and not s[j]:
                j += 1
            if j - i >= 10:
                cand.append((i, j))
            i = j
        else:
            i += 1
    cand.append((off, off))
    K = len(cand)
    # tốc độ: thơ ~ 0.33 s/âm tiết; văn xuôi ước theo tổng thời lượng
    tong = (off - on) / 100
    lang = sum((b - a) for a, b in cand[1:-1]) / 100
    at_tho = sum(u["at"] for u in don_vi if u["tho"])
    at_xuoi = sum(u["at"] for u in don_vi if not u["tho"])
    r_tho = 0.33
    kdet = (cum[off] - cum[on]) / max(1, at_tho + at_xuoi)
    n_tho = sum(1 for u in don_vi if u["tho"])
    r_xuoi = max(0.15, (tong - n_tho * 1.45) / max(1, at_xuoi))
    U = len(don_vi)
    INF = 1e18
    dp = np.full((U + 1, K), INF)
    bk = np.zeros((U + 1, K), dtype=int)
    dp[0][0] = 0.0
    for u in range(1, U + 1):
        dv = don_vi[u - 1]
        e = dv["at"] * (r_tho if dv["tho"] else r_xuoi)
        trong_so = 3.0 if dv["tho"] else 1.0
        prev = np.nonzero(dp[u - 1] < INF)[0]
        if len(prev) == 0:
            break
        for b in range(1, K):
            best, arg = INF, -1
            tb = cand[b][0]
            for a in prev:
                if a >= b:
                    break
                d = (tb - cand[a][1]) / 100
                if d <= 0.15:
                    continue
                if d > e * 2.2 + 8:
                    continue
                det = cum[tb] - cum[cand[a][1]]
                ky = kdet * dv["at"]
                c = (dp[u - 1][a] + trong_so * 1.0 * ((d - e) / max(e, 0.8)) ** 2
                     + 1.5 * ((det - ky) / max(ky, 2.5)) ** 2
                     - 0.35 * min(1.0, (cand[b][1] - cand[b][0]) / 100))
                if c < best:
                    best, arg = c, a
            dp[u][b] = best
            bk[u][b] = arg
    # kết thúc ở ứng viên cuối
    ket = []
    b = K - 1
    for u in range(U, 0, -1):
        a = bk[u][b]
        ket.append(((cand[a][1]) / 100, cand[b][0] / 100))
        b = a
    ket = ket[::-1]
    for dv, (a, b) in zip(don_vi, ket):
        dv["bd"], dv["kt"] = round(a, 2), round(b, 2)
    return don_vi, r_xuoi


if __name__ == "__main__":
    pass


# ---------------- tinh chỉnh điểm cắt bằng thanh điệu ----------------
import unicodedata

def thanh(am):
    """Lớp đường nét thanh điệu: +1 lên, -1 xuống, 0 ngang."""
    d = unicodedata.normalize("NFD", am)
    if "́" in d or "̃" in d:   # sắc, ngã
        return 1
    if "̀" in d or "̣" in d or "̉" in d:  # huyền, nặng, hỏi
        return -1
    return 0


def tu_am_tiet(s):
    return re.findall(r"[0-9A-Za-zÀ-ỹđĐ]+", s)


def nhan_am_tiet(path):
    from scipy.signal import butter, sosfiltfilt, find_peaks
    sr, x = wavfile.read(path)
    x = x.astype(np.float32) / 32768
    hop, win = sr // 100, int(sr * 0.025)
    n = (len(x) - win) // hop
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i * hop:i * hop + win] ** 2)) + 1e-9) for i in range(n)])
    noise, sp = np.percentile(db, 10), np.percentile(db, 90)
    thr = noise + 0.35 * (sp - noise)
    sos = butter(4, [300, 3000], btype="band", fs=sr, output="sos"); y = sosfiltfilt(sos, x)
    env = np.array([np.sqrt(np.mean(y[i * hop:i * hop + win] ** 2)) for i in range(n)])
    edb = 20 * np.log10(np.convolve(env, np.ones(5) / 5, "same") + 1e-9)
    pk, _ = find_peaks(edb, prominence=4, distance=9, height=thr)
    return pk / 100.0


def doc_cao_do(path):
    import parselmouth
    snd = parselmouth.Sound(path)
    p = snd.to_pitch(time_step=0.01, pitch_floor=120, pitch_ceiling=450)
    return p


def lop_doan(pitch, t):
    vals = []
    for dt in np.arange(-0.10, 0.11, 0.02):
        f = pitch.get_value_at_time(t + dt)
        if not np.isnan(f):
            vals.append((dt, f))
    if len(vals) < 4:
        return None
    a = np.array(vals)
    hs = np.polyfit(a[:, 0], np.log(a[:, 1]), 1)[0]  # độ dốc log-F0 / giây
    if hs > 1.0:
        return 1
    if hs < -1.0:
        return -1
    return 0


def tinh_chinh_cat(path, t_dp, cau_cat, cau_truoc, pitch=None, nhan=None, cand=None):
    pitch = pitch or doc_cao_do(path)
    nhan = nhan if nhan is not None else nhan_am_tiet(path)
    mong = [thanh(a) for a in tu_am_tiet(cau_cat)[:4]]
    mong_truoc = [thanh(a) for a in tu_am_tiet(cau_truoc)[-3:]]
    tot = []
    for (bd, kt) in cand:
        if abs(kt - t_dp) > 4.5:
            continue
        sau = [t for t in nhan if t >= kt - 0.02][:4]
        truoc = [t for t in nhan if t <= bd + 0.02][-3:]
        diem = 0.0
        for t, m in zip(sau, mong):
            c = lop_doan(pitch, t)
            if c is not None:
                diem += 1.0 if c == m else (-0.5 if c == -m and m != 0 else 0)
        for t, m in zip(truoc, mong_truoc):
            c = lop_doan(pitch, t)
            if c is not None:
                diem += 0.5 if c == m else (-0.25 if c == -m and m != 0 else 0)
        diem += 0.6 * min(1.0, kt - bd) - 0.08 * abs(kt - t_dp)
        tot.append((diem, bd, kt))
    tot.sort(reverse=True)
    return tot
