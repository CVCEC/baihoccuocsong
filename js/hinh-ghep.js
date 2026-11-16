/* =====================================================================
   Tranh ghép cho câu hỏi và video (dùng chung mọi bài).
   Mã tranh viết ngắn trong dữ liệu bài, ví dụ:
     "me:cuoi|be:cuoi:om"        – mẹ và bé ôm nhau
     "be:ngu|giuong"             – bé đang ngủ
     "ban-tho|be::cui"           – bé cúi chào trước bàn thờ
     "be:khoc|x"                 – bé khóc (dấu x đỏ: điều không nên)
     "noi:Dạ, con chào bà ạ|be|ba"
   Phần tử cách nhau bằng "|"; mỗi phần tử là "tên:biểu cảm:tư thế" (người) hoặc "tên:chữ" (vật có chữ).
   Dấu phủ (không chiếm chỗ): x (không nên), v (nên), tim, hoi, zz, sao-nho.
   Không vẽ Trâu Con ở đây – Trâu Con luôn là ảnh chính thức.
   Cần js/hinh.js nạp trước (dùng window.HINH cho các tranh có sẵn).
   ===================================================================== */
(function () {
  "use strict";
  var G = 104; // mặt đất
  function f(n) { return Math.round(n * 10) / 10; }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---------- Khuôn mặt (toạ độ tuyệt đối trong khung cục bộ) ---------- */
  function mat(cx, cy, r, kieu, toc) {
    var s = "", w = Math.max(2, r * 0.09);
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" class="f-da"/>';
    if (toc !== "khong") {
      s += '<path d="M' + f(cx - r) + ',' + cy + ' A' + r + ',' + r + ' 0 0 1 ' + f(cx + r) + ',' + cy +
        ' L' + f(cx + r * 0.82) + ',' + f(cy - r * 0.18) + ' Q' + cx + ',' + f(cy - r * 0.62) + ' ' + f(cx - r * 0.82) + ',' + f(cy - r * 0.18) + ' Z" class="' + (toc || "f-toc") + '"/>';
    }
    s += '<circle cx="' + f(cx - r * 0.55) + '" cy="' + f(cy + r * 0.32) + '" r="' + f(r * 0.13) + '" class="f-ma"/>';
    s += '<circle cx="' + f(cx + r * 0.55) + '" cy="' + f(cy + r * 0.32) + '" r="' + f(r * 0.13) + '" class="f-ma"/>';
    var ex = r * 0.34, ey = cy + r * 0.05;
    if (kieu === "ngu" || kieu === "khoc" || kieu === "vui") {
      var q = kieu === "vui" ? -1 : 1;
      s += '<path d="M' + f(cx - ex - r * 0.13) + ',' + f(ey) + ' q' + f(r * 0.13) + ',' + f(q * r * 0.1) + ' ' + f(r * 0.26) + ',0" class="s-muc" stroke-width="' + f(w) + '" fill="none" stroke-linecap="round"/>';
      s += '<path d="M' + f(cx + ex - r * 0.13) + ',' + f(ey) + ' q' + f(r * 0.13) + ',' + f(q * r * 0.1) + ' ' + f(r * 0.26) + ',0" class="s-muc" stroke-width="' + f(w) + '" fill="none" stroke-linecap="round"/>';
    } else {
      s += '<circle cx="' + f(cx - ex) + '" cy="' + f(ey) + '" r="' + f(r * 0.1) + '" class="f-muc"/>';
      s += '<circle cx="' + f(cx + ex) + '" cy="' + f(ey) + '" r="' + f(r * 0.1) + '" class="f-muc"/>';
    }
    if (kieu === "phung" || kieu === "gian") {
      s += '<path d="M' + f(cx - ex - r * 0.15) + ',' + f(ey - r * 0.28) + ' l' + f(r * 0.28) + ',' + f(r * 0.1) + ' M' + f(cx + ex + r * 0.15) + ',' + f(ey - r * 0.28) + ' l' + f(-r * 0.28) + ',' + f(r * 0.1) + '" class="s-muc" stroke-width="' + f(w) + '" stroke-linecap="round"/>';
    }
    if (kieu === "mo") {
      s += '<ellipse cx="' + cx + '" cy="' + f(cy + r * 0.47) + '" rx="' + f(r * 0.2) + '" ry="' + f(r * 0.16) + '" class="f-son"/>';
    } else if (kieu === "khoc" || kieu === "phung" || kieu === "buon" || kieu === "gian" || kieu === "om") {
      s += '<path d="M' + f(cx - r * 0.25) + ',' + f(cy + r * 0.58) + ' Q' + cx + ',' + f(cy + r * 0.36) + ' ' + f(cx + r * 0.25) + ',' + f(cy + r * 0.58) + '" class="s-muc" stroke-width="' + f(w) + '" fill="none" stroke-linecap="round"/>';
    } else if (kieu === "ngu") {
      s += '<ellipse cx="' + cx + '" cy="' + f(cy + r * 0.48) + '" rx="' + f(r * 0.09) + '" ry="' + f(r * 0.07) + '" class="f-muc"/>';
    } else if (kieu === "hoi") {
      s += '<path d="M' + f(cx - r * 0.18) + ',' + f(cy + r * 0.5) + ' l' + f(r * 0.36) + ',0" class="s-muc" stroke-width="' + f(w) + '" stroke-linecap="round"/>';
    } else {
      s += '<path d="M' + f(cx - r * 0.3) + ',' + f(cy + r * 0.38) + ' Q' + cx + ',' + f(cy + r * 0.66) + ' ' + f(cx + r * 0.3) + ',' + f(cy + r * 0.38) + '" class="s-muc" stroke-width="' + f(w) + '" fill="none" stroke-linecap="round"/>';
    }
    if (kieu === "khoc") {
      [-1, 1].forEach(function (d) {
        s += '<path d="M' + f(cx + d * ex) + ',' + f(ey + r * 0.15) + ' q' + f(-r * 0.1) + ',' + f(r * 0.25) + ' 0,' + f(r * 0.32) + ' q' + f(r * 0.1) + ',' + f(-r * 0.07) + ' 0,' + f(-r * 0.32) + 'z" class="f-nuoc-mat"/>';
      });
    }
    if (kieu === "om") { // ốm: khăn chườm trên trán
      s += '<rect x="' + f(cx - r * 0.7) + '" y="' + f(cy - r * 0.62) + '" width="' + f(r * 1.4) + '" height="' + f(r * 0.32) + '" rx="' + f(r * 0.12) + '" class="f-trang s-xam" stroke-width="1.5"/>';
    }
    return s;
  }

  /* ---------- Người: khung cục bộ, chân ở y = 0, đứng giữa x = 0 ---------- */
  var VAI = {
    be:  { r: 14, dau: -62, than: [-48, 26], ao: "f-son", toc: "f-toc", nho: true },
    ban: { r: 14, dau: -62, than: [-48, 26], ao: "f-dung", toc: "f-toc", nho: true, toc2: "bim" },
    em:  { r: 12, dau: -48, than: [-36, 22], ao: "f-sao", toc: "f-toc", nho: true },
    anh: { r: 14, dau: -72, than: [-58, 28], ao: "f-troi-dam", toc: "f-toc", nho: true },
    chi: { r: 14, dau: -72, than: [-58, 28], ao: "f-goc", toc: "f-toc", nho: true, toc2: "dai" },
    me:  { r: 15, dau: -84, than: [-69, 34], ao: "f-goc", toc: "f-toc", toc2: "dai" },
    bo:  { r: 15, dau: -86, than: [-71, 36], ao: "f-muc", toc: "f-toc" },
    co:  { r: 15, dau: -84, than: [-69, 32], ao: "f-troi-dam", toc: "f-toc", toc2: "dai", aoDai: true },
    thay:{ r: 15, dau: -86, than: [-71, 36], ao: "f-dung", toc: "f-toc", kinh: true },
    ba:  { r: 15, dau: -80, than: [-65, 34], ao: "f-goc-dam", toc: "f-toc-bac", toc2: "bui" },
    ong: { r: 15, dau: -82, than: [-67, 36], ao: "f-xam", toc: "f-toc-bac", rau: true },
    bacsi: { r: 15, dau: -86, than: [-71, 34], ao: "f-trang s-xam", toc: "f-toc", bacSi: true }
  };
  function nguoi(vai, cam, tuThe) {
    var v = VAI[vai] || VAI.be, r = v.r, y0 = v.dau, s = "";
    var top = v.than[0], w = v.than[1];
    if (v.toc2 === "dai") s += '<path d="M' + f(-r * 1.05) + ',' + f(y0 - r * 0.2) + ' Q' + f(-r * 1.2) + ',' + f(y0 + r * 1.5) + ' ' + f(-r * 0.7) + ',' + f(y0 + r * 1.7) + ' H' + f(r * 0.7) + ' Q' + f(r * 1.2) + ',' + f(y0 + r * 1.5) + ' ' + f(r * 1.05) + ',' + f(y0 - r * 0.2) + ' Z" class="' + v.toc + '"/>';
    // thân áo + tay
    var ao = '<path d="M' + f(-w / 2 + 3) + ',' + top + ' H' + f(w / 2 - 3) + ' Q' + f(w / 2 + 2) + ',' + top + ' ' + f(w / 2 + 2) + ',' + (top + 6) + ' L' + f(w / 2 + (v.aoDai ? 6 : 2)) + ',' + (v.aoDai ? -4 : -10) + ' H' + f(-w / 2 - (v.aoDai ? 6 : 2)) + ' L' + f(-w / 2 - 2) + ',' + (top + 6) + ' Q' + f(-w / 2 - 2) + ',' + top + ' ' + f(-w / 2 + 3) + ',' + top + ' Z" class="' + v.ao + '"' + (v.bacSi ? ' stroke-width="2"' : '') + '/>';
    var chan = v.aoDai ? '' : '<rect x="' + f(-w / 2 + 3) + '" y="-11" width="' + f(w / 2 - 4) + '" height="11" rx="3" class="f-muc"/><rect x="' + f(1) + '" y="-11" width="' + f(w / 2 - 4) + '" height="11" rx="3" class="f-muc"/>';
    var tay;
    var vai1 = top + 6, sx = w / 2 + 1;
    if (tuThe === "gio-tay") {
      tay = '<path d="M' + f(-sx) + ',' + vai1 + ' L' + f(-sx - 6) + ',' + (top + 26) + '" class="s-tay" stroke-width="7" stroke-linecap="round"/>' +
            '<path d="M' + f(sx) + ',' + vai1 + ' L' + f(sx + 10) + ',' + (top - 22) + '" class="s-tay" stroke-width="7" stroke-linecap="round"/>';
    } else if (tuThe === "khoanh" || tuThe === "cui") {
      tay = '<path d="M' + f(-sx) + ',' + vai1 + ' Q' + f(-sx + 2) + ',' + (top + 22) + ' ' + f(sx - 6) + ',' + (top + 18) + ' M' + f(sx) + ',' + vai1 + ' Q' + f(sx - 2) + ',' + (top + 22) + ' ' + f(-sx + 6) + ',' + (top + 18) + '" class="s-tay" stroke-width="6" fill="none" stroke-linecap="round"/>';
    } else if (tuThe === "om" || tuThe === "dua") {
      tay = '<path d="M' + f(-sx) + ',' + vai1 + ' L' + f(-sx - 4) + ',' + (top + 22) + ' M' + f(sx) + ',' + vai1 + ' L' + f(sx + 16) + ',' + (top + 14) + '" class="s-tay" stroke-width="7" stroke-linecap="round" fill="none"/>';
    } else {
      tay = '<path d="M' + f(-sx) + ',' + vai1 + ' L' + f(-sx - 5) + ',' + (top + 26) + ' M' + f(sx) + ',' + vai1 + ' L' + f(sx + 5) + ',' + (top + 26) + '" class="s-tay" stroke-width="7" stroke-linecap="round" fill="none"/>';
    }
    s += chan + tay + ao;
    if (v.bacSi) s += '<path d="M-6,' + (top + 4) + ' q6,14 12,0" class="s-muc" stroke-width="2" fill="none"/><circle cx="6" cy="' + (top + 4) + '" r="3" class="f-xam"/>';
    s += mat(0, y0, r, cam || "cuoi", v.toc);
    if (v.toc2 === "bim") s += '<circle cx="' + f(-r * 0.95) + '" cy="' + f(y0 - r * 0.55) + '" r="' + f(r * 0.3) + '" class="f-toc"/><circle cx="' + f(r * 0.95) + '" cy="' + f(y0 - r * 0.55) + '" r="' + f(r * 0.3) + '" class="f-toc"/>';
    if (v.toc2 === "bui") s += '<circle cx="0" cy="' + f(y0 - r * 1.05) + '" r="' + f(r * 0.38) + '" class="f-toc-bac"/>';
    if (v.rau) s += '<path d="M' + f(-r * 0.45) + ',' + f(y0 + r * 0.72) + ' Q0,' + f(y0 + r * 1.55) + ' ' + f(r * 0.45) + ',' + f(y0 + r * 0.72) + ' Z" class="f-toc-bac"/>';
    if (v.kinh) s += '<circle cx="' + f(-r * 0.34) + '" cy="' + f(y0 + r * 0.05) + '" r="' + f(r * 0.24) + '" class="s-muc" stroke-width="1.8" fill="none"/><circle cx="' + f(r * 0.34) + '" cy="' + f(y0 + r * 0.05) + '" r="' + f(r * 0.24) + '" class="s-muc" stroke-width="1.8" fill="none"/>';
    return { svg: s, rong: Math.max(w + 12, r * 2 + 6) + (tuThe === "cui" ? 18 : 0), cao: -(y0 - r), cui: tuThe === "cui" };
  }

  /* ---------- Đồ vật: khung cục bộ, đáy ở y = 0 ---------- */
  function sach(x, y, w) {
    var h = w * 0.42, m = x + w / 2;
    return '<path d="M' + x + ',' + (y + 6) + ' Q' + f(x + w * 0.25) + ',' + (y - 2) + ' ' + m + ',' + (y + 6) + ' L' + m + ',' + f(y + h + 6) + ' Q' + f(x + w * 0.25) + ',' + f(y + h - 2) + ' ' + x + ',' + f(y + h + 6) + ' Z" class="f-trang s-vien" stroke-width="3"/>' +
      '<path d="M' + m + ',' + (y + 6) + ' Q' + f(x + w * 0.75) + ',' + (y - 2) + ' ' + (x + w) + ',' + (y + 6) + ' L' + (x + w) + ',' + f(y + h + 6) + ' Q' + f(x + w * 0.75) + ',' + f(y + h - 2) + ' ' + m + ',' + f(y + h + 6) + ' Z" class="f-trang s-vien" stroke-width="3"/>' +
      '<path d="M' + f(x + w * 0.1) + ',' + f(y + h * 0.45) + ' h' + f(w * 0.3) + ' M' + f(x + w * 0.1) + ',' + f(y + h * 0.7) + ' h' + f(w * 0.25) + ' M' + f(x + w * 0.6) + ',' + f(y + h * 0.45) + ' h' + f(w * 0.3) + ' M' + f(x + w * 0.6) + ',' + f(y + h * 0.7) + ' h' + f(w * 0.25) + '" class="s-xam" stroke-width="3" stroke-linecap="round"/>';
  }
  function ngoiSao(cx, cy, r, lop) {
    var p = [];
    for (var i = 0; i < 10; i++) {
      var g = Math.PI / 5 * i - Math.PI / 2, rr = i % 2 ? r * 0.45 : r;
      p.push(f(cx + rr * Math.cos(g)) + "," + f(cy + rr * Math.sin(g)));
    }
    return '<polygon points="' + p.join(" ") + '" class="' + (lop || "f-sao") + '"/>';
  }
  function tim(cx, cy, r, lop) {
    return '<path d="M' + cx + ',' + f(cy + r * 0.9) + ' C' + f(cx - r * 1.6) + ',' + f(cy - r * 0.2) + ' ' + f(cx - r * 0.7) + ',' + f(cy - r * 1.2) + ' ' + cx + ',' + f(cy - r * 0.4) + ' C' + f(cx + r * 0.7) + ',' + f(cy - r * 1.2) + ' ' + f(cx + r * 1.6) + ',' + f(cy - r * 0.2) + ' ' + cx + ',' + f(cy + r * 0.9) + ' Z" class="' + (lop || "f-son") + '"/>';
  }
  function chuNho(x, y, chu, co, lop, neo) {
    return '<text x="' + x + '" y="' + y + '" text-anchor="' + (neo || "middle") + '" font-size="' + co + '" class="' + (lop || "f-muc") + '" font-family="Andika, Nunito, sans-serif" font-weight="700">' + esc(chu) + '</text>';
  }
  var VAT = {
    "sach": function () { return { svg: sach(-30, -34, 60), rong: 64, cao: 36 }; },
    "chong-sach": function () {
      var s = "", m = ["f-son", "f-troi-dam", "f-sao", "f-dung"];
      for (var i = 0; i < 4; i++) s += '<rect x="' + (-26 + i * 2) + '" y="' + (-12 - i * 12) + '" width="' + (52 - i * 4) + '" height="11" rx="2" class="' + m[i] + '"/><rect x="' + (-22 + i * 2) + '" y="' + (-9 - i * 12) + '" width="' + (40 - i * 4) + '" height="2" class="f-trang"/>';
      return { svg: s, rong: 56, cao: 50 };
    },
    "vo-but": function () {
      return { svg: '<rect x="-26" y="-40" width="40" height="40" rx="4" class="f-trang s-vien" stroke-width="3"/><path d="M-20,-28 h28 M-20,-19 h28 M-20,-10 h20" class="s-xam" stroke-width="2.5" stroke-linecap="round"/>' +
        '<g transform="rotate(28 16 -24)"><rect x="12" y="-48" width="9" height="38" rx="2" class="f-sao"/><path d="M12,-10 h9 l-4.5,9z" class="f-da"/><rect x="12" y="-52" width="9" height="6" rx="2" class="f-son"/></g>', rong: 56, cao: 52 };
    },
    "ban-hoc": function () {
      return { svg: '<rect x="-34" y="-34" width="68" height="8" rx="3" class="f-goc"/><rect x="-30" y="-26" width="6" height="26" class="f-goc-dam"/><rect x="24" y="-26" width="6" height="26" class="f-goc-dam"/>' + sach(-22, -52, 44), rong: 72, cao: 54 };
    },
    "giuong": function (kieu) {
      var s = '<rect x="-48" y="-30" width="96" height="16" rx="5" class="f-goc"/><rect x="-48" y="-14" width="7" height="14" class="f-goc-dam"/><rect x="41" y="-14" width="7" height="14" class="f-goc-dam"/><rect x="-48" y="-50" width="8" height="36" rx="3" class="f-goc-dam"/>';
      s += '<rect x="-40" y="-44" width="30" height="16" rx="8" class="f-trang s-vien" stroke-width="2.5"/>';
      if (kieu !== "trong") s += mat(-26, -38, 12, kieu === "om" ? "om" : (kieu || "ngu"), "f-toc") + '<path d="M-14,-32 h58 a4,4 0 0 1 4,4 v2 h-62z" class="f-goc-nhat"/>';
      if (!kieu || kieu === "ngu") s += chuNho(30, -50, "z", 12, "f-muc") + chuNho(40, -60, "Z", 15, "f-muc");
      return { svg: s, rong: 100, cao: 62 };
    },
    "bat-com": function () {
      return { svg: '<path d="M-24,-26 h48 a24,24 0 0 1 -48,0z" class="f-trang s-vien" stroke-width="3"/><path d="M-22,-26 q22,-22 44,0z" class="f-trang"/><path d="M-14,-30 q14,-12 28,0" class="s-xam" stroke-width="1.5" fill="none"/>' +
        '<path d="M8,-58 L28,-26 M16,-60 L32,-28" class="s-goc-dam" stroke-width="3.5" stroke-linecap="round"/><rect x="-10" y="-4" width="20" height="4" rx="2" class="f-goc"/>', rong: 56, cao: 60 };
    },
    "mam-com": function () {
      var s = '<ellipse cx="0" cy="-8" rx="50" ry="10" class="f-goc"/><rect x="-50" y="-8" width="100" height="6" class="f-goc-dam"/>';
      [-30, 0, 30].forEach(function (x, i) {
        s += '<path d="M' + (x - 12) + ',-22 h24 a12,12 0 0 1 -24,0z" class="' + (i === 1 ? "f-sao" : "f-trang s-vien") + '" stroke-width="2"/><path d="M' + (x - 11) + ',-22 q11,-10 22,0z" class="' + (i === 1 ? "f-lua" : "f-trang") + '"/>';
      });
      return { svg: s, rong: 104, cao: 34 };
    },
    "mat-troi": function () {
      var s = "", cx = 0, cy = -46, r = 18;
      for (var i = 0; i < 8; i++) { var g = Math.PI / 4 * i; s += '<path d="M' + f(cx + Math.cos(g) * r * 1.3) + ',' + f(cy + Math.sin(g) * r * 1.3) + ' L' + f(cx + Math.cos(g) * r * 1.7) + ',' + f(cy + Math.sin(g) * r * 1.7) + '" class="s-sao" stroke-width="4" stroke-linecap="round"/>'; }
      return { svg: s + '<circle cx="0" cy="-46" r="18" class="f-sao"/>', rong: 66, cao: 80 };
    },
    "trang": function () {
      return { svg: '<path d="M8,-80 a26,26 0 1 0 14,46 a20,20 0 1 1 -14,-46z" class="f-sao"/>' + ngoiSao(-22, -70, 6) + ngoiSao(30, -30, 5) + ngoiSao(-26, -24, 4), rong: 64, cao: 84 };
    },
    "nha": function () {
      return { svg: '<rect x="-30" y="-40" width="60" height="40" class="f-kem"/><path d="M-38,-38 L0,-68 L38,-38 Z" class="f-son"/><rect x="-8" y="-24" width="16" height="24" rx="2" class="f-goc-dam"/><rect x="-24" y="-30" width="12" height="10" class="f-troi"/><rect x="12" y="-30" width="12" height="10" class="f-troi"/>', rong: 80, cao: 70 };
    },
    "cay": function () {
      return { svg: '<rect x="-5" y="-40" width="10" height="40" rx="3" class="f-goc-dam"/><circle cx="0" cy="-58" r="24" class="f-lua"/><circle cx="-18" cy="-46" r="14" class="f-lua"/><circle cx="18" cy="-46" r="14" class="f-lua"/><circle cx="-6" cy="-64" r="5" class="f-lua-sang"/><circle cx="10" cy="-50" r="4" class="f-lua-sang"/>', rong: 64, cao: 84 };
    },
    "truong": function () {
      return { svg: '<rect x="-46" y="-44" width="92" height="44" class="f-kem"/><path d="M-52,-42 H52 L42,-56 H-42 Z" class="f-son"/><rect x="-10" y="-74" width="20" height="20" class="f-kem"/><path d="M-14,-72 L0,-84 L14,-72Z" class="f-son"/><circle cx="0" cy="-64" r="5" class="f-sao"/>' +
        '<rect x="-8" y="-24" width="16" height="24" class="f-goc-dam"/><rect x="-38" y="-34" width="12" height="10" class="f-troi"/><rect x="-22" y="-34" width="10" height="10" class="f-troi"/><rect x="14" y="-34" width="10" height="10" class="f-troi"/><rect x="28" y="-34" width="12" height="10" class="f-troi"/>', rong: 104, cao: 86 };
    },
    "ban-tho": function () {
      var s = '<rect x="-40" y="-36" width="80" height="8" rx="2" class="f-son"/><rect x="-36" y="-28" width="72" height="28" class="f-goc-dam"/><rect x="-28" y="-22" width="56" height="16" rx="2" class="f-son"/>';
      s += '<rect x="-10" y="-52" width="20" height="16" rx="3" class="f-sao"/>';
      [-5, 0, 5].forEach(function (x) { s += '<path d="M' + x + ',-52 V-74" class="s-goc-dam" stroke-width="1.6"/><circle cx="' + x + '" cy="-75" r="1.6" class="f-son"/>'; });
      s += '<path d="M0,-80 q-5,-6 0,-12 q5,-6 0,-12" class="s-xam" stroke-width="1.5" fill="none" opacity=".7"/>';
      s += '<path d="M-34,-40 h20 l-3,4 h-14z" class="f-sao"/><circle cx="-28" cy="-45" r="5" class="f-son"/><circle cx="-20" cy="-45" r="5" class="f-sao"/><circle cx="-24" cy="-51" r="5" class="f-lua"/>';
      s += '<rect x="22" y="-56" width="6" height="20" class="f-trang s-xam" stroke-width="1"/><path d="M25,-56 q-3,-5 0,-9 q3,4 0,9z" class="f-sao"/>';
      return { svg: s, rong: 84, cao: 92 };
    },
    "thuoc": function () {
      return { svg: '<rect x="-20" y="-46" width="28" height="46" rx="6" class="f-troi"/><rect x="-22" y="-54" width="32" height="10" rx="3" class="f-trang s-xam" stroke-width="2"/><rect x="-16" y="-34" width="20" height="16" rx="2" class="f-trang"/><path d="M-6,-32 v12 M-12,-26 h12" class="s-son" stroke-width="3"/>' +
        '<g transform="rotate(-30 22 -14)"><rect x="12" y="-20" width="22" height="11" rx="5.5" class="f-son"/><rect x="23" y="-20" width="11" height="11" rx="5.5" class="f-trang s-xam" stroke-width="1"/></g>', rong: 60, cao: 56 };
    },
    "ban-chai": function () {
      return { svg: '<path d="M-26,0 L-30,-40 H-6 L-10,0 Z" class="f-troi"/><g transform="rotate(-18 10 -30)"><rect x="6" y="-70" width="8" height="64" rx="4" class="f-son"/><rect x="2" y="-74" width="16" height="12" rx="2" class="f-trang s-xam" stroke-width="1.5"/></g>' +
        '<circle cx="22" cy="-58" r="5" class="f-trang s-troi" stroke-width="1.5"/><circle cx="30" cy="-48" r="3.5" class="f-trang s-troi" stroke-width="1.5"/>', rong: 64, cao: 78 };
    },
    "xa-phong": function () {
      return { svg: '<rect x="-24" y="-18" width="40" height="18" rx="8" class="f-sao"/><circle cx="18" cy="-34" r="9" class="f-trang s-troi" stroke-width="2"/><circle cx="-4" cy="-38" r="6" class="f-trang s-troi" stroke-width="2"/><circle cx="6" cy="-56" r="5" class="f-trang s-troi" stroke-width="2"/>' +
        '<path d="M-30,-60 q4,10 0,14 q-4,-4 0,-14z M-18,-70 q4,10 0,14 q-4,-4 0,-14z" class="f-troi"/>', rong: 62, cao: 72 };
    },
    "nuoc": function () {
      return { svg: '<path d="M-16,-50 L-12,0 H12 L16,-50 Z" class="f-trang s-xam" stroke-width="2.5"/><path d="M-14.5,-32 L-12,-2 H12 L14.5,-32 Z" class="f-troi"/>', rong: 40, cao: 52 };
    },
    "qua": function () {
      return { svg: '<ellipse cx="0" cy="-6" rx="34" ry="7" class="f-trang s-vien" stroke-width="2.5"/><circle cx="-14" cy="-20" r="12" class="f-son"/><circle cx="12" cy="-20" r="12" class="f-sao"/><circle cx="0" cy="-36" r="11" class="f-lua"/><path d="M-14,-32 q4,-6 8,-4" class="s-dung" stroke-width="2.5" fill="none"/>', rong: 72, cao: 50 };
    },
    "hoa": function () {
      var s = '<path d="M-14,0 L-18,-24 H18 L14,0 Z" class="f-goc-dam"/><path d="M0,-24 V-50" class="s-dung" stroke-width="3"/><path d="M0,-34 q-14,-2 -16,-14 q12,2 16,14z" class="f-lua"/>';
      for (var i = 0; i < 6; i++) { var g = Math.PI / 3 * i; s += '<circle cx="' + f(Math.cos(g) * 9) + '" cy="' + f(-60 + Math.sin(g) * 9) + '" r="7" class="f-son"/>'; }
      return { svg: s + '<circle cx="0" cy="-60" r="6" class="f-sao"/>', rong: 46, cao: 78 };
    },
    "o": function () {
      return { svg: '<path d="M-40,-50 Q0,-96 40,-50 Q30,-56 20,-50 Q10,-56 0,-50 Q-10,-56 -20,-50 Q-30,-56 -40,-50Z" class="f-son"/><path d="M0,-50 V-6 q0,6 -6,6 q-6,0 -6,-6" class="s-muc" stroke-width="3.5" fill="none" stroke-linecap="round"/>', rong: 84, cao: 76 };
    },
    "mua": function () {
      var s = '<circle cx="-14" cy="-62" r="14" class="f-xam-nhat"/><circle cx="6" cy="-68" r="18" class="f-xam-nhat"/><circle cx="24" cy="-60" r="12" class="f-xam-nhat"/><rect x="-28" y="-62" width="64" height="14" rx="7" class="f-xam-nhat"/>';
      [-16, -2, 12, 26].forEach(function (x, i) { s += '<path d="M' + x + ',' + (-40 + (i % 2) * 6) + ' l-4,10" class="s-troi-dam" stroke-width="3.5" stroke-linecap="round"/>'; });
      return { svg: s, rong: 72, cao: 88 };
    },
    "lua": function () {
      return { svg: '<path d="M0,0 C-26,0 -28,-26 -14,-40 C-14,-30 -6,-28 -4,-34 C-6,-48 4,-60 10,-66 C10,-52 26,-42 24,-20 C22,-6 12,0 0,0Z" class="f-son"/><path d="M0,0 C-12,0 -14,-12 -6,-20 C-4,-14 2,-14 2,-20 C6,-16 12,-10 10,-4 C8,0 4,0 0,0Z" class="f-sao"/>', rong: 56, cao: 68 };
    },
    "bong": function () {
      return { svg: '<circle cx="0" cy="-22" r="22" class="f-trang s-muc" stroke-width="3"/><path d="M-22,-22 H22 M0,-44 V0" class="s-son" stroke-width="3"/><path d="M-15,-38 q15,16 0,32 M15,-38 q-15,16 0,32" class="s-son" stroke-width="3" fill="none"/>', rong: 50, cao: 46 };
    },
    "dien-thoai": function () {
      return { svg: '<rect x="-16" y="-58" width="32" height="58" rx="6" class="f-muc"/><rect x="-12" y="-52" width="24" height="42" rx="2" class="f-troi"/><circle cx="0" cy="-5" r="2.5" class="f-trang"/>' + ngoiSao(0, -31, 7), rong: 40, cao: 60 };
    },
    "tivi": function () {
      return { svg: '<rect x="-34" y="-58" width="68" height="46" rx="5" class="f-muc"/><rect x="-28" y="-53" width="56" height="36" rx="2" class="f-troi"/><path d="M-10,-12 L-16,0 M10,-12 L16,0" class="s-muc" stroke-width="4" stroke-linecap="round"/><circle cx="-6" cy="-38" r="6" class="f-sao"/><path d="M6,-44 l10,6 l-10,6z" class="f-son"/>', rong: 74, cao: 60 };
    },
    "keo": function () {
      return { svg: '<path d="M-36,-26 l14,-10 v20z M36,-26 l-14,-10 v20z" class="f-sao"/><ellipse cx="0" cy="-26" rx="24" ry="14" class="f-son"/><path d="M-12,-34 q12,-5 24,0" class="s-trang" stroke-width="3" fill="none" opacity=".6"/>', rong: 76, cao: 42 };
    },
    "trai-tim": function () { return { svg: tim(0, -30, 20), rong: 50, cao: 52 }; },
    "sao": function () { return { svg: ngoiSao(0, -28, 24), rong: 52, cao: 54 }; },
    "dong-ho": function () {
      return { svg: '<circle cx="-14" cy="-54" r="7" class="f-son"/><circle cx="14" cy="-54" r="7" class="f-son"/><circle cx="0" cy="-28" r="24" class="f-trang s-muc" stroke-width="4"/><path d="M0,-28 v-14 M0,-28 l9,8" class="s-muc" stroke-width="4" stroke-linecap="round"/><path d="M-14,-4 l-4,4 M14,-4 l4,4" class="s-muc" stroke-width="4" stroke-linecap="round"/>', rong: 56, cao: 62 };
    },
    "tien": function () {
      return { svg: '<ellipse cx="-8" cy="-6" rx="18" ry="6" class="f-sao"/><rect x="-26" y="-14" width="36" height="8" class="f-sao"/><ellipse cx="-8" cy="-14" rx="18" ry="6" class="f-sao s-goc-dam" stroke-width="1.5"/><circle cx="18" cy="-24" r="14" class="f-sao s-goc-dam" stroke-width="2"/><circle cx="18" cy="-24" r="8" class="s-goc-dam" stroke-width="2" fill="none"/>', rong: 60, cao: 40 };
    },
    "qua-tang": function () {
      return { svg: '<rect x="-24" y="-36" width="48" height="36" rx="4" class="f-son"/><rect x="-28" y="-46" width="56" height="12" rx="3" class="f-son"/><rect x="-4" y="-46" width="8" height="46" class="f-sao"/><path d="M0,-46 q-16,-16 -18,-4 q2,6 18,4 q16,2 18,-4 q-2,-12 -18,4z" class="f-sao"/>', rong: 60, cao: 58 };
    },
    "meo": function () {
      return { svg: '<path d="M-16,0 Q-20,-26 0,-28 Q20,-26 16,0 Z" class="f-cam"/><path d="M14,-4 Q32,-4 30,-22" class="s-cam" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="0" cy="-36" r="13" class="f-cam"/><path d="M-11,-43 l3,-13 l8,9 Z M11,-43 l-3,-13 l-8,9 Z" class="f-cam"/><circle cx="-5" cy="-37" r="2" class="f-muc"/><circle cx="5" cy="-37" r="2" class="f-muc"/><path d="M-2,-32 h4 l-2,2.5z" class="f-son"/>', rong: 56, cao: 56 };
    },
    "cho": function () {
      return { svg: '<rect x="-30" y="-24" width="48" height="22" rx="11" class="f-nau"/><rect x="-26" y="-8" width="8" height="8" rx="3" class="f-nau"/><rect x="6" y="-8" width="8" height="8" rx="3" class="f-nau"/><path d="M-29,-18 Q-40,-26 -36,-36" class="s-nau" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="22" cy="-32" r="14" class="f-nau"/><path d="M13,-42 Q8,-28 15,-23 Q20,-31 18,-42 Z" class="f-goc-dam"/><ellipse cx="32" cy="-27" rx="7" ry="5.5" class="f-kem"/><circle cx="24" cy="-35" r="2" class="f-muc"/><circle cx="38" cy="-28" r="2.2" class="f-muc"/>', rong: 72, cao: 48 };
    },
    "ga": function () {
      return { svg: '<path d="M-16,-12 Q-18,-32 0,-30 Q10,-30 14,-20 L16,-26 Q24,-30 22,-18 Q20,-2 2,0 Q-14,0 -16,-12 Z" class="f-trang s-xam" stroke-width="1.5"/><path d="M-15,-17 Q-28,-30 -24,-40 Q-17,-28 -12,-24 Z" class="f-goc-dam"/><path d="M15,-30 q2,-7 6,-2 q3,-5 5,2 Z" class="f-son"/><path d="M24,-23 l7,2.5 l-7,2.5 Z" class="f-sao"/><circle cx="20" cy="-24" r="1.6" class="f-muc"/>' +
        '<g transform="translate(34 0)"><circle cx="0" cy="-7" r="7" class="f-sao"/><circle cx="6" cy="-14" r="5" class="f-sao"/><path d="M10.5,-14.5 l4,1.3 l-4,1.3 Z" class="f-son"/></g>', rong: 70, cao: 42 };
    },
    "chim": function () {
      return { svg: '<path d="M-30,-40 q15,-14 30,0 q15,-14 30,0" class="s-muc" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M-10,-62 q8,-8 16,0 q8,-8 16,0" class="s-muc" stroke-width="3" fill="none" stroke-linecap="round"/>', rong: 64, cao: 66 };
    },
    "huou": function () { // hươu sao
      var s = '<rect x="-24" y="-46" width="44" height="22" rx="11" class="f-nau"/>';
      [-20, -10, 6, 14].forEach(function (x) { s += '<rect x="' + x + '" y="-28" width="5" height="28" rx="2" class="f-nau"/>'; });
      s += '<path d="M14,-40 L22,-66 L32,-64 L26,-38 Z" class="f-nau"/><ellipse cx="30" cy="-68" rx="10" ry="7" class="f-nau"/><path d="M24,-74 l-6,-14 M22,-82 l-6,-2 M30,-74 l4,-14 M32,-82 l6,-2" class="s-goc-dam" stroke-width="2.5" stroke-linecap="round"/>';
      [[-14, -40], [-4, -36], [6, -42], [-10, -32]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="2.4" class="f-trang"/>'; });
      return { svg: s + '<circle cx="33" cy="-70" r="1.8" class="f-muc"/><path d="M-24,-40 q-8,-2 -8,-8" class="s-nau" stroke-width="4" stroke-linecap="round" fill="none"/>', rong: 76, cao: 90 };
    },
    "ba-ba": function () { // ba ba bò bên bờ nước
      return { svg: '<path d="M-56,0 q14,-5 28,0 t28,0 t28,0 t28,0" class="s-troi-dam" stroke-width="3" fill="none"/>' +
        '<ellipse cx="0" cy="-16" rx="30" ry="15" class="f-lua-dam"/><ellipse cx="0" cy="-18" rx="20" ry="9" class="f-lua"/><circle cx="34" cy="-14" r="7" class="f-lua-dam"/><path d="M38,-14 l6,-1" class="s-muc" stroke-width="2"/>' +
        '<circle cx="36" cy="-16" r="1.6" class="f-muc"/><ellipse cx="-20" cy="-4" rx="7" ry="4" class="f-lua-dam"/><ellipse cx="18" cy="-4" rx="7" ry="4" class="f-lua-dam"/>', rong: 96, cao: 34 };
    },
    "bo-cau": function () {
      return { svg: '<ellipse cx="0" cy="-16" rx="22" ry="14" class="f-xam-nhat"/><circle cx="18" cy="-32" r="10" class="f-xam-nhat"/><path d="M12,-26 q6,6 12,0 v6 q-6,4 -12,0 Z" class="f-dung"/>' +
        '<path d="M-20,-18 l-14,-4 l4,12 Z" class="f-xam"/><path d="M-6,-24 q10,-14 22,-4 q-12,2 -22,4z" class="f-xam"/><path d="M27,-33 l6,2 l-6,2 Z" class="f-sao"/><circle cx="20" cy="-34" r="1.8" class="f-muc"/><path d="M-4,-2 v4 M6,-2 v4" class="s-son" stroke-width="2.5"/>', rong: 66, cao: 44 };
    },
    "ca": function () {
      return { svg: '<path d="M-56,0 q14,-5 28,0 t28,0 t28,0 t28,0" class="s-troi-dam" stroke-width="3" fill="none"/><ellipse cx="0" cy="-24" rx="24" ry="12" class="f-sao"/><path d="M-22,-24 l-14,-10 v20 Z" class="f-sao"/><circle cx="12" cy="-27" r="2.4" class="f-muc"/><path d="M-4,-34 q6,10 0,20" class="s-goc-dam" stroke-width="2" fill="none"/>', rong: 96, cao: 40 };
    },
    "cay-mit": function () { // cây thân gỗ nhiều cành, có quả mít
      var s = '<path d="M-6,0 V-40 L-26,-60 M-4,-42 L4,-70 M2,-40 L26,-58" class="s-goc-dam" stroke-width="7" stroke-linecap="round" fill="none"/><rect x="-7" y="-44" width="14" height="44" rx="4" class="f-goc-dam"/>';
      [[-28, -66, 16], [4, -78, 18], [28, -64, 16], [-12, -58, 12], [16, -54, 12]].forEach(function (c) { s += '<circle cx="' + c[0] + '" cy="' + c[1] + '" r="' + c[2] + '" class="f-lua-dam"/>'; });
      s += '<ellipse cx="-2" cy="-34" rx="6" ry="9" class="f-lua-sang"/><ellipse cx="10" cy="-26" rx="5" ry="8" class="f-lua-sang"/>';
      return { svg: s, rong: 76, cao: 96 };
    },
    "co-gianh": function () { // cỏ, thân có đốt
      var s = "";
      [-18, -6, 6, 18].forEach(function (x, i) {
        var h = 54 + (i % 2) * 14;
        s += '<path d="M' + x + ',0 V' + (-h) + '" class="s-dung" stroke-width="4"/>';
        for (var k = 1; k < 4; k++) s += '<rect x="' + (x - 3.5) + '" y="' + (-k * h / 4 - 1.5) + '" width="7" height="3" rx="1" class="f-lua-dam"/>';
        s += '<path d="M' + x + ',' + (-h * .6) + ' q' + (i % 2 ? 14 : -14) + ',-8 ' + (i % 2 ? 18 : -18) + ',-26" class="s-dung" stroke-width="2.5" fill="none"/>';
      });
      return { svg: s, rong: 56, cao: 70 };
    },
    "da": function () { // hòn đá, đá cuội bên bờ sông
      return { svg: '<path d="M-56,0 q14,-5 28,0 t28,0 t28,0 t28,0" class="s-troi-dam" stroke-width="3" fill="none"/>' +
        '<ellipse cx="-14" cy="-16" rx="22" ry="15" class="f-da-xam"/><ellipse cx="16" cy="-10" rx="15" ry="10" class="f-xam-nhat"/><ellipse cx="-30" cy="-6" rx="9" ry="6" class="f-xam-nhat"/><ellipse cx="32" cy="-5" rx="7" ry="5" class="f-da-xam"/>' +
        '<path d="M-24,-22 q6,-4 12,-2" class="s-trang" stroke-width="2.5" fill="none" opacity=".7"/>', rong: 96, cao: 34 };
    },
    "chum": function () { // chum, vại đất nung
      return { svg: '<path d="M-14,-62 h28 v6 q20,8 18,30 q-2,22 -20,26 h-24 q-18,-4 -20,-26 q-2,-22 18,-30 Z" class="f-dat-nung"/><rect x="-16" y="-66" width="32" height="7" rx="3" class="f-dat-nung-dam"/><path d="M-22,-36 h44" class="s-dat-nung-dam" stroke-width="2.5"/>', rong: 52, cao: 68 };
    },
    "manh-sanh": function () {
      return { svg: '<path d="M-34,-4 l10,-20 l14,6 l-4,14 Z" class="f-dat-nung"/><path d="M-4,-2 l6,-24 l18,4 l2,18 Z" class="f-dat-nung-dam"/><path d="M22,-2 l8,-14 l10,10 l-4,4 Z" class="f-dat-nung"/>', rong: 80, cao: 30 };
    },
    "cuoc": function () { // đồ dùng bằng sắt: cuốc, dao
      return { svg: '<path d="M-30,-4 L4,-60" class="s-goc-dam" stroke-width="6" stroke-linecap="round"/><path d="M-6,-62 h22 l-2,14 h-18 Z" class="f-sat"/>' +
        '<g transform="rotate(-20 24 -20)"><rect x="14" y="-30" width="8" height="22" rx="3" class="f-goc-dam"/><path d="M14,-30 h8 l10,-34 q-12,4 -18,34 Z" class="f-sat"/></g>', rong: 72, cao: 66 };
    },
    "noi-dong": function () {
      return { svg: '<path d="M-28,-34 h56 q-2,30 -28,32 q-26,-2 -28,-32 Z" class="f-dong"/><rect x="-32" y="-40" width="64" height="7" rx="3" class="f-dong-dam"/><path d="M-32,-36 q-10,0 -10,8 M32,-36 q10,0 10,8" class="s-dong-dam" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M-16,-24 q6,-4 10,0" class="s-trang" stroke-width="2.5" fill="none" opacity=".6"/>', rong: 88, cao: 42 };
    },
    "vang": function () { // vàng thỏi, bạc nén
      return { svg: '<path d="M-36,0 l6,-16 h26 l6,16 Z" class="f-sao s-goc-dam" stroke-width="1.5"/><path d="M-30,-16 l5,-12 h18 l5,12 Z" class="f-sao s-goc-dam" stroke-width="1.5"/><path d="M6,0 l6,-16 h22 l6,16 Z" class="f-bac s-xam" stroke-width="1.5"/>' +
        '<path d="M-22,-24 l4,-4 M30,-22 l4,-4" class="s-trang" stroke-width="2.5" stroke-linecap="round"/>' + ngoiSao(-6, -38, 6) + ngoiSao(26, -30, 5), rong: 80, cao: 46 };
    },
    "ban-hang": function () { // quầy hàng – mua bán
      return { svg: '<rect x="-44" y="-30" width="88" height="30" class="f-goc"/><rect x="-44" y="-36" width="88" height="8" class="f-goc-dam"/><path d="M-48,-60 h96 l-6,-14 h-84 Z" class="f-son"/><path d="M-40,-60 v24 M40,-60 v24" class="s-goc-dam" stroke-width="3"/>' +
        '<circle cx="-24" cy="-42" r="7" class="f-son"/><circle cx="-12" cy="-42" r="7" class="f-sao"/><circle cx="10" cy="-42" r="7" class="f-lua"/><circle cx="22" cy="-42" r="7" class="f-son"/>', rong: 96, cao: 74 };
    },
    "em-be": function (kieu) { // em bé quấn khăn
      return { svg: '<ellipse cx="0" cy="-16" rx="24" ry="16" class="f-kem"/><path d="M-22,-20 q22,14 44,0" class="s-goc" stroke-width="2.5" fill="none"/>' + mat(-14, -26, 12, kieu || "ngu", "f-toc") + (kieu === "khoc" ? '' : '<path d="M6,-44 q2,-4 6,-2" class="s-muc" stroke-width="1.5" fill="none"/>'), rong: 56, cao: 40 };
    },
    "noi-em-be": function () { // nôi đung đưa có em bé
      return { svg: '<path d="M-40,-52 Q0,-96 40,-52" class="s-goc-dam" stroke-width="3" fill="none"/><path d="M-36,-40 Q0,4 36,-40 Z" class="f-goc"/><path d="M-36,-40 H36" class="s-goc-dam" stroke-width="3"/>' + mat(-10, -44, 11, "ngu", "f-toc") + '<path d="M-30,-40 q30,10 58,0" class="f-kem"/>' +
        '<path d="M-28,-2 q28,8 56,0" class="s-goc-dam" stroke-width="4" fill="none" stroke-linecap="round"/>', rong: 84, cao: 76 };
    },
    "bien": function () { // sông bể mênh mông
      return { svg: '<rect x="-56" y="-46" width="112" height="46" rx="6" class="f-troi"/><path d="M-56,-36 q14,-8 28,0 t28,0 t28,0 t28,0 M-56,-20 q14,-8 28,0 t28,0 t28,0 t28,0" class="s-troi-dam" stroke-width="3" fill="none"/><circle cx="34" cy="-62" r="10" class="f-sao"/>', rong: 112, cao: 72 };
    },
    "tom-cua": function () {
      return { svg: '<ellipse cx="-16" cy="-12" rx="14" ry="9" class="f-son"/><path d="M-30,-14 q-8,-10 -2,-16 M-2,-14 q8,-10 2,-16" class="s-son" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="-34" cy="-30" r="4" class="f-son"/><circle cx="2" cy="-30" r="4" class="f-son"/><circle cx="-20" cy="-16" r="1.6" class="f-muc"/><circle cx="-12" cy="-16" r="1.6" class="f-muc"/>' +
        '<path d="M14,-10 q10,-18 26,-10 q-6,6 -4,12 q-12,6 -22,-2 Z" class="f-cam"/><path d="M36,-20 l6,-10 M38,-18 l8,-6" class="s-cam" stroke-width="1.5"/><circle cx="34" cy="-17" r="1.4" class="f-muc"/>', rong: 84, cao: 40 };
    },
    "chau-lan-cuc": function () { // một chậu, nhiều cành lan và cúc
      var s = '<path d="M-30,-26 h60 l-8,26 h-44z" class="f-dat-nung"/><rect x="-33" y="-30" width="66" height="7" rx="3" class="f-dat-nung-dam"/>';
      var canh = [[-24, -62, 'c'], [-10, -78, 'l'], [4, -68, 'c'], [16, -82, 'l'], [26, -58, 'c']];
      canh.forEach(function (c) { s += '<path d="M' + (c[0] / 3) + ',-30 Q' + (c[0] * 0.8) + ',' + ((c[1] - 30) / 2) + ' ' + c[0] + ',' + c[1] + '" class="s-goc-dam" stroke-width="2.5" fill="none"/>'; });
      s += '<path d="M-6,-30 q-18,-6 -26,-20 M6,-30 q18,-6 24,-18" class="s-goc-dam" stroke-width="4" fill="none" stroke-linecap="round"/>';
      canh.forEach(function (c) {
        if (c[2] === 'c') { for (var k = 0; k < 10; k++) { var g = k * Math.PI / 5; s += '<ellipse cx="' + (c[0] + Math.cos(g) * 6).toFixed(1) + '" cy="' + (c[1] + Math.sin(g) * 6).toFixed(1) + '" rx="5" ry="2.4" transform="rotate(' + (k * 36) + ' ' + (c[0] + Math.cos(g) * 6).toFixed(1) + ' ' + (c[1] + Math.sin(g) * 6).toFixed(1) + ')" class="f-sao"/>'; } s += '<circle cx="' + c[0] + '" cy="' + c[1] + '" r="4" class="f-cam"/>'; }
        else { s += '<path d="M' + c[0] + ',' + (c[1] - 9) + ' q7,4 8,10 q-8,4 -8,8 q0,-4 -8,-8 q1,-6 8,-10z" class="f-son-nhat"/><circle cx="' + c[0] + '" cy="' + (c[1] + 2) + '" r="3" class="f-son"/>'; }
      });
      return { svg: s, rong: 76, cao: 94 };
    },
    "ao-quan": function () { // bộ quần áo gấp gọn
      var s = '<path d="M-44,-60 l14,-8 h12 q6,8 12,0 h12 l14,8 l-8,14 l-8,-4 v34 h-32 v-34 l-8,4z" class="f-troi"/><path d="M-20,-68 q6,8 12,0" class="s-muc" stroke-width="1.5" fill="none"/>';
      s += '<path d="M10,-56 h32 v8 l-4,44 h-10 l-2,-36 l-2,36 h-10 l-4,-44z" class="f-troi-dam"/><path d="M10,-50 h32" class="s-muc" stroke-width="1.2"/>';
      return { svg: s, rong: 92, cao: 72 };
    },
    "co-xuan": function () { // khóm cỏ non mùa xuân
      var s = '<ellipse cx="0" cy="-3" rx="40" ry="5" class="f-dat"/>';
      [-30, -20, -10, 0, 10, 20, 30].forEach(function (x, i) { var h = 26 + (i % 3) * 8; s += '<path d="M' + (x - 4) + ',-4 Q' + (x + (i % 2 ? 6 : -6)) + ',' + (-h / 2) + ' ' + (x + (i % 2 ? 4 : -4)) + ',' + (-h) + ' Q' + (x + 2) + ',' + (-h / 2) + ' ' + (x + 4) + ',-4z" class="f-lua"/>'; });
      s += '<circle cx="-16" cy="-24" r="4" class="f-sao"/><circle cx="18" cy="-30" r="4" class="f-son-nhat"/>';
      return { svg: s, rong: 84, cao: 46 };
    },
    "to-chim": function () { // tổ chim có chim non đang mọc cánh
      var s = '<path d="M-6,0 V-30" class="s-goc-dam" stroke-width="5"/><path d="M-40,-30 H40" class="s-goc-dam" stroke-width="5" stroke-linecap="round"/>';
      s += '<path d="M-30,-34 q30,22 60,0 q-4,-10 -30,-10 q-26,0 -30,10z" class="f-nau"/>';
      [-14, 2, 16].forEach(function (x) { s += '<circle cx="' + x + '" cy="-44" r="8" class="f-sao"/><path d="M' + (x + 6) + ',-46 l5,2 l-5,2z" class="f-son"/><circle cx="' + (x + 2) + '" cy="-46" r="1.4" class="f-muc"/>'; });
      s += '<path d="M34,-70 q14,-12 26,0" class="s-muc" stroke-width="3" fill="none"/>';
      return { svg: s, rong: 84, cao: 76 };
    },
    "gieng": function () { // giếng nước làng quê
      return { svg: '<ellipse cx="0" cy="-30" rx="30" ry="9" class="f-troi-dam"/><path d="M-30,-30 V0 H30 V-30" class="f-gach"/><ellipse cx="0" cy="-30" rx="30" ry="9" class="s-goc-dam" stroke-width="3" fill="none"/>' +
        '<path d="M-30,-20 H30 M-30,-10 H30 M-15,-30 V-20 M10,-20 V-10 M-5,-10 V0" class="s-goc-dam" stroke-width="1.5" opacity=".6"/>' +
        '<path d="M-22,-34 V-74 M22,-34 V-74 M-28,-74 H28" class="s-goc-dam" stroke-width="4" stroke-linecap="round"/><path d="M6,-74 V-52" class="s-muc" stroke-width="1.5"/><path d="M-2,-52 h16 l-2,12 h-12 Z" class="f-goc"/>', rong: 68, cao: 80 };
    },
    "bo-rom": function () {
      var s = "";
      for (var i = 0; i < 6; i++) {
        var x = -30 + i * 11, y = -10 - Math.sin(i / 5 * Math.PI) * 10;
        s += '<circle cx="' + x + '" cy="' + f(y) + '" r="8" class="f-cam"/>';
        for (var k = -1; k <= 1; k++) s += '<path d="M' + x + ',' + f(y - 8) + ' l' + (k * 3) + ',-7" class="s-muc" stroke-width="1.6" stroke-linecap="round"/>';
      }
      return { svg: s + '<circle cx="31" cy="-12" r="2" class="f-muc"/>', rong: 76, cao: 40 };
    },
    "cay-lua": function () {
      var s = '<rect x="-40" y="-8" width="80" height="8" class="f-troi"/>';
      [-28, -12, 4, 20].forEach(function (x) { s += '<path d="M' + x + ',-6 q-4,-24 -10,-34 M' + x + ',-6 q2,-26 8,-38 M' + x + ',-6 q6,-20 14,-26" class="s-dung" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="' + (x + 8) + '" cy="-44" rx="3" ry="6" class="f-sao"/>'; });
      return { svg: s, rong: 84, cao: 56 };
    },
    "tre": function () {
      var s = "";
      [-14, 0, 14].forEach(function (x, i) {
        s += '<rect x="' + (x - 3) + '" y="' + (-90 + i * 8) + '" width="6" height="' + (90 - i * 8) + '" rx="2" class="f-lua-dam"/>';
        for (var k = 1; k < 4; k++) s += '<rect x="' + (x - 4) + '" y="' + (-90 + i * 8 + k * 22) + '" width="8" height="2.5" class="f-dung"/>';
        s += '<path d="M' + x + ',' + (-80 + i * 8) + ' q16,-6 22,-16 q-14,0 -22,16z" class="f-lua"/>';
      });
      return { svg: s, rong: 56, cao: 96 };
    },
    "nui": function () {
      return { svg: '<path d="M-56,0 L-20,-60 L4,-26 L24,-48 L56,0 Z" class="f-lua-dam"/><path d="M-20,-60 L-28,-46 L-12,-46 Z" class="f-trang"/><path d="M-56,0 Q-10,-14 56,-4 V0Z" class="f-troi"/>' + '<circle cx="34" cy="-70" r="10" class="f-sao"/>', rong: 112, cao: 82 };
    },
    "thuyen": function () {
      return { svg: '<path d="M-40,-8 Q0,4 40,-8 L32,-18 H-32 Z" class="f-goc-dam"/><path d="M-6,-18 V-70 L26,-26 H-6" class="f-kem s-goc-dam" stroke-width="2"/><path d="M-56,0 q14,-6 28,0 t28,0 t28,0 t28,0" class="s-troi-dam" stroke-width="3" fill="none"/>', rong: 112, cao: 74 };
    },
    "but-long": function () {
      return { svg: '<rect x="-30" y="-12" width="60" height="12" rx="2" class="f-goc-dam"/><g transform="rotate(-35 0 -40)"><rect x="-3" y="-80" width="6" height="56" rx="3" class="f-goc"/><path d="M-4,-24 h8 l-4,14z" class="f-muc"/></g>' + chuNho(18, -20, "永", 22, "f-muc"), rong: 64, cao: 76 };
    },
    "bang": function (chu) {
      chu = chu || "a b c";
      return { svg: '<rect x="-46" y="-76" width="92" height="60" rx="5" class="f-bang s-goc-dam" stroke-width="4"/><path d="M-30,-16 L-36,0 M30,-16 L36,0" class="s-goc-dam" stroke-width="4" stroke-linecap="round"/>' + chuNho(0, -40, chu, chu.length > 8 ? 13 : 18, "f-trang"), rong: 96, cao: 78 };
    },
    "chu": function (chu) { // tấm thẻ có chữ
      chu = chu || "";
      var co = chu.length > 12 ? 13 : chu.length > 8 ? 16 : chu.length > 4 ? 20 : 30;
      return { svg: '<rect x="-46" y="-70" width="92" height="64" rx="10" class="f-trang s-vien" stroke-width="3"/><rect x="-46" y="-70" width="92" height="12" rx="6" class="f-goc-nhat"/>' + chuNho(0, -26, chu, co, "f-muc"), rong: 96, cao: 72 };
    },
    "noi": function (chu) { // bóng lời nói (đặt trên cao)
      chu = chu || "…";
      var w = Math.max(40, Math.min(152, chu.length * 7.6 + 22));
      return { svg: '<rect x="' + f(-w / 2) + '" y="-104" width="' + f(w) + '" height="28" rx="12" class="f-trang s-vien" stroke-width="2.5"/><path d="M-6,-77 l-2,10 l12,-10z" class="f-trang"/>' + chuNho(0, -85, chu, 13, "f-muc"), rong: w, cao: 104, phu: true };
    }
  };

  /* ---------- Dấu phủ (góc trên phải, không chiếm chỗ) ---------- */
  var DAU = {
    "x": '<circle cx="140" cy="20" r="15" class="f-son"/><path d="M133,13 l14,14 M147,13 l-14,14" class="s-trang" stroke-width="4" stroke-linecap="round"/>',
    "v": '<circle cx="140" cy="20" r="15" class="f-dung"/><path d="M132,20 l6,7 l11,-13" class="s-trang" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "tim": tim(140, 18, 9) + tim(124, 30, 6, "f-son-nhat"),
    "hoi": chuNho(140, 30, "?", 30, "f-son") + chuNho(124, 22, "?", 18, "f-son"),
    "zz": chuNho(130, 26, "z", 14, "f-muc") + chuNho(142, 16, "Z", 18, "f-muc"),
    "sao-nho": ngoiSao(140, 18, 10) + ngoiSao(124, 30, 6)
  };

  function boc(noiDung) {
    return '<svg viewBox="0 0 160 110" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="hinh">' + noiDung + '</svg>';
  }
  var ViTri = { 1: [80], 2: [52, 110], 3: [30, 80, 130], 4: [22, 60, 100, 138] };

  function ghep(ma) {
    var phan = String(ma).split("|"), dau = "", ds = [];
    phan.forEach(function (p) {
      p = p.trim(); if (!p) return;
      if (DAU[p]) { dau += DAU[p]; return; }
      var t = p.split(":"), ten = t[0];
      if (VAI[ten]) ds.push(nguoi(ten, t[1], t[2]));
      else if (VAT[ten]) ds.push(VAT[ten](t.slice(1).join(":")));
    });
    var chinh = ds.filter(function (d) { return !d.phu; }), phu = ds.filter(function (d) { return d.phu; });
    var n = Math.max(1, Math.min(4, chinh.length)), vt = ViTri[n];
    var tong = chinh.reduce(function (a, d) { return a + d.rong; }, 0) + 6 * (n - 1);
    var tran = phu.length ? 66 : 100; // có bóng lời nói thì chừa khoảng trên đầu
    var k = Math.min(n === 1 ? 1.3 : 1.15, 150 / Math.max(tong, 1), tran / Math.max.apply(null, chinh.map(function (d) { return d.cao; }).concat([1])));
    var s = '<rect x="0" y="' + G + '" width="160" height="6" class="f-dat"/>';
    // dàn đều theo bề rộng thật
    var x = 80 - (tong * k) / 2;
    chinh.slice(0, 4).forEach(function (d, i) {
      var cx = n > 1 ? x + d.rong * k / 2 : vt[0];
      var svg = d.cui ? '<g transform="rotate(' + (cx > 80 ? -12 : 12) + ' 0 0)">' + d.svg + '</g>' : d.svg; // cúi chào về phía giữa tranh
      s += '<g transform="translate(' + f(cx) + ' ' + G + ') scale(' + f(k) + ')">' + svg + '</g>';
      x += d.rong * k + 6;
    });
    phu.forEach(function (d) { s += '<g transform="translate(80 ' + (G + 2) + ')">' + d.svg + '</g>'; });
    return boc(s + dau);
  }

  var cache = {};
  window.layHinh = function (ma) {
    if (!ma) return "";
    if (window.HINH && window.HINH[ma]) return window.HINH[ma];
    if (!cache[ma]) cache[ma] = ghep(ma);
    return cache[ma];
  };
  window.HINH_GHEP = { vai: Object.keys(VAI), vat: Object.keys(VAT), dau: Object.keys(DAU) };
})();
