/* =====================================================================
   Tranh minh hoạ đơn giản (SVG phẳng, màu lấy từ biến --ttv-* qua lớp CSS).
   Dùng chung cho trang bài học và video. Không vẽ Trâu Con ở đây –
   Trâu Con luôn dùng ảnh chính thức.
   Lớp màu: f-muc f-son f-sao f-goc f-goc-dam f-goc-nhat f-nen f-trang f-da f-toc
            f-ma f-troi f-lua f-xam f-dung ; s-muc s-son s-xam s-vien s-dung (nét)
   ===================================================================== */
(function () {
  "use strict";
  function mat(cx, cy, r, kieu) {
    var s = "";
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" class="f-da"/>';
    // tóc
    s += '<path d="M' + (cx - r) + ',' + cy + ' A' + r + ',' + r + ' 0 0 1 ' + (cx + r) + ',' + cy +
         ' L' + (cx + r * 0.82) + ',' + (cy - r * 0.18) + ' Q' + cx + ',' + (cy - r * 0.62) + ' ' + (cx - r * 0.82) + ',' + (cy - r * 0.18) + ' Z" class="f-toc"/>';
    // má hồng
    s += '<circle cx="' + (cx - r * 0.55) + '" cy="' + (cy + r * 0.32) + '" r="' + (r * 0.13) + '" class="f-ma"/>';
    s += '<circle cx="' + (cx + r * 0.55) + '" cy="' + (cy + r * 0.32) + '" r="' + (r * 0.13) + '" class="f-ma"/>';
    var ex = r * 0.34, ey = cy + r * 0.05, w = Math.max(2, r * 0.08);
    if (kieu === "ngu" || kieu === "khoc") {
      // mắt nhắm
      s += '<path d="M' + (cx - ex - r * 0.13) + ',' + ey + ' q' + (r * 0.13) + ',' + (r * 0.1) + ' ' + (r * 0.26) + ',0" class="s-muc" stroke-width="' + w + '" fill="none" stroke-linecap="round"/>';
      s += '<path d="M' + (cx + ex - r * 0.13) + ',' + ey + ' q' + (r * 0.13) + ',' + (r * 0.1) + ' ' + (r * 0.26) + ',0" class="s-muc" stroke-width="' + w + '" fill="none" stroke-linecap="round"/>';
    } else {
      s += '<circle cx="' + (cx - ex) + '" cy="' + ey + '" r="' + (r * 0.1) + '" class="f-muc"/>';
      s += '<circle cx="' + (cx + ex) + '" cy="' + ey + '" r="' + (r * 0.1) + '" class="f-muc"/>';
    }
    if (kieu === "phung") {
      s += '<path d="M' + (cx - ex - r * 0.15) + ',' + (ey - r * 0.28) + ' l' + (r * 0.28) + ',' + (r * 0.1) + '" class="s-muc" stroke-width="' + w + '" stroke-linecap="round"/>';
      s += '<path d="M' + (cx + ex + r * 0.15) + ',' + (ey - r * 0.28) + ' l' + (-r * 0.28) + ',' + (r * 0.1) + '" class="s-muc" stroke-width="' + w + '" stroke-linecap="round"/>';
    }
    if (kieu === "mo") {
      s += '<ellipse cx="' + cx + '" cy="' + (cy + r * 0.47) + '" rx="' + (r * 0.2) + '" ry="' + (r * 0.16) + '" class="f-son"/>';
    } else if (kieu === "khoc" || kieu === "phung") {
      s += '<path d="M' + (cx - r * 0.25) + ',' + (cy + r * 0.58) + ' Q' + cx + ',' + (cy + r * 0.36) + ' ' + (cx + r * 0.25) + ',' + (cy + r * 0.58) + '" class="s-muc" stroke-width="' + w + '" fill="none" stroke-linecap="round"/>';
    } else if (kieu === "ngu") {
      s += '<ellipse cx="' + cx + '" cy="' + (cy + r * 0.48) + '" rx="' + (r * 0.09) + '" ry="' + (r * 0.07) + '" class="f-muc"/>';
    } else if (kieu === "hoi") {
      s += '<path d="M' + (cx - r * 0.18) + ',' + (cy + r * 0.5) + ' l' + (r * 0.36) + ',0" class="s-muc" stroke-width="' + w + '" stroke-linecap="round"/>';
    } else {
      s += '<path d="M' + (cx - r * 0.3) + ',' + (cy + r * 0.38) + ' Q' + cx + ',' + (cy + r * 0.66) + ' ' + (cx + r * 0.3) + ',' + (cy + r * 0.38) + '" class="s-muc" stroke-width="' + w + '" fill="none" stroke-linecap="round"/>';
    }
    if (kieu === "khoc") {
      s += '<path d="M' + (cx - ex) + ',' + (ey + r * 0.15) + ' q-' + (r * 0.1) + ',' + (r * 0.25) + ' 0,' + (r * 0.32) + ' q' + (r * 0.1) + ',-' + (r * 0.07) + ' 0,-' + (r * 0.32) + 'z" class="f-nuoc-mat"/>';
      s += '<path d="M' + (cx + ex) + ',' + (ey + r * 0.15) + ' q-' + (r * 0.1) + ',' + (r * 0.25) + ' 0,' + (r * 0.32) + ' q' + (r * 0.1) + ',-' + (r * 0.07) + ' 0,-' + (r * 0.32) + 'z" class="f-nuoc-mat"/>';
    }
    return s;
  }
  function giay(chu, co, phong) {
    return '<rect x="26" y="10" width="108" height="90" rx="12" class="f-trang s-vien" stroke-width="3"/>' +
      '<rect x="26" y="10" width="108" height="16" rx="8" class="f-goc-nhat"/>' +
      '<text x="80" y="' + (co > 40 ? 78 : 70) + '" text-anchor="middle" font-size="' + co + '" class="f-muc" font-family="' + (phong || "Andika, Nunito, sans-serif") + '" font-weight="700">' + chu + '</text>';
  }
  function sach(x, y, w) {
    var h = w * 0.42, m = x + w / 2;
    return '<path d="M' + x + ',' + (y + 6) + ' Q' + (x + w * 0.25) + ',' + (y - 2) + ' ' + m + ',' + (y + 6) + ' L' + m + ',' + (y + h + 6) + ' Q' + (x + w * 0.25) + ',' + (y + h - 2) + ' ' + x + ',' + (y + h + 6) + ' Z" class="f-trang s-vien" stroke-width="3"/>' +
      '<path d="M' + m + ',' + (y + 6) + ' Q' + (x + w * 0.75) + ',' + (y - 2) + ' ' + (x + w) + ',' + (y + 6) + ' L' + (x + w) + ',' + (y + h + 6) + ' Q' + (x + w * 0.75) + ',' + (y + h - 2) + ' ' + m + ',' + (y + h + 6) + ' Z" class="f-trang s-vien" stroke-width="3"/>' +
      '<path d="M' + (x + w * 0.1) + ',' + (y + h * 0.45) + ' h' + (w * 0.3) + ' M' + (x + w * 0.1) + ',' + (y + h * 0.7) + ' h' + (w * 0.25) + ' M' + (x + w * 0.6) + ',' + (y + h * 0.45) + ' h' + (w * 0.3) + ' M' + (x + w * 0.6) + ',' + (y + h * 0.7) + ' h' + (w * 0.25) + '" class="s-xam" stroke-width="3" stroke-linecap="round"/>';
  }
  function song(x, y, huong) { // vòng âm thanh
    var d = huong < 0 ? -1 : 1;
    return '<path d="M' + x + ',' + (y - 8) + ' q' + (d * 7) + ',8 0,16 M' + (x + d * 8) + ',' + (y - 14) + ' q' + (d * 11) + ',14 0,28" class="s-son" stroke-width="3.5" fill="none" stroke-linecap="round"/>';
  }
  function ngoiSao(cx, cy, r) {
    var p = [];
    for (var i = 0; i < 10; i++) {
      var g = Math.PI / 5 * i - Math.PI / 2, rr = i % 2 ? r * 0.45 : r;
      p.push((cx + rr * Math.cos(g)).toFixed(1) + "," + (cy + rr * Math.sin(g)).toFixed(1));
    }
    return '<polygon points="' + p.join(" ") + '" class="f-sao"/>';
  }
  function dongHo(cx, cy, r) {
    return '<circle cx="' + (cx - r * 0.7) + '" cy="' + (cy - r * 0.85) + '" r="' + (r * 0.32) + '" class="f-son"/>' +
      '<circle cx="' + (cx + r * 0.7) + '" cy="' + (cy - r * 0.85) + '" r="' + (r * 0.32) + '" class="f-son"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" class="f-trang s-muc" stroke-width="4"/>' +
      '<path d="M' + cx + ',' + cy + ' v-' + (r * 0.6) + ' M' + cx + ',' + cy + ' l-' + (r * 0.32) + ',' + (r * 0.45) + '" class="s-muc" stroke-width="4" stroke-linecap="round"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="3" class="f-muc"/>';
  }
  function matTroi(cx, cy, r) {
    var s = "";
    for (var i = 0; i < 8; i++) {
      var g = Math.PI / 4 * i;
      s += '<path d="M' + (cx + Math.cos(g) * r * 1.3).toFixed(1) + ',' + (cy + Math.sin(g) * r * 1.3).toFixed(1) + ' L' + (cx + Math.cos(g) * r * 1.65).toFixed(1) + ',' + (cy + Math.sin(g) * r * 1.65).toFixed(1) + '" class="s-sao" stroke-width="4" stroke-linecap="round"/>';
    }
    return s + '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" class="f-sao"/>';
  }
  function boc(noiDung) {
    return '<svg viewBox="0 0 160 110" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="hinh">' + noiDung + '</svg>';
  }
  var HINH = {
    "chu-han": boc(giay("字", 54, "'Noto Serif CJK SC','Songti SC',serif")),
    "chu-quoc-ngu": boc(giay("Xin chào", 22)),
    "chu-tieng-anh": boc(giay("Hello", 26, "Nunito, sans-serif")),
    "noi-chuyen": boc(
      mat(46, 66, 24, "mo") + mat(114, 66, 24, "cuoi") +
      '<path d="M58,8 h44 a10,10 0 0 1 10,10 v10 a10,10 0 0 1 -10,10 h-16 l-6,8 l-6,-8 h-16 a10,10 0 0 1 -10,-10 v-10 a10,10 0 0 1 10,-10z" class="f-trang s-vien" stroke-width="3"/>' +
      '<circle cx="68" cy="23" r="3.5" class="f-muc"/><circle cx="80" cy="23" r="3.5" class="f-muc"/><circle cx="92" cy="23" r="3.5" class="f-muc"/>'),
    "an-keo": boc(
      '<path d="M22,55 l18,-14 v28z M138,55 l-18,-14 v28z" class="f-sao"/>' +
      '<ellipse cx="80" cy="55" rx="42" ry="24" class="f-son"/>' +
      '<path d="M58,42 q22,-8 44,0" class="s-trang" stroke-width="4" fill="none" stroke-linecap="round" opacity=".6"/>' +
      '<path d="M120,14 v24 M120,14 l14,-4 v20" class="s-muc" stroke-width="4" fill="none" stroke-linecap="round"/>' +
      '<ellipse cx="116" cy="39" rx="5.5" ry="4.5" class="f-muc"/><ellipse cx="130" cy="31" rx="5.5" ry="4.5" class="f-muc"/>'),
    "doc-nghe": boc(
      sach(36, 72, 88) + mat(80, 40, 26, "mo") + song(110, 50, 1) +
      '<path d="M44,28 q-14,4 -10,22 q2,8 8,8" class="s-muc" stroke-width="4" fill="none" stroke-linecap="round"/>' +
      '<path d="M30,18 l-8,-6 M26,34 h-10 M30,50 l-8,6" class="s-son" stroke-width="3.5" stroke-linecap="round"/>'),
    "voi-vang": boc(
      '<path d="M30,82 l12,-14 l10,12 l12,-16 l10,14 l12,-18 l10,16" class="s-son" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round"/>' +
      '<g transform="rotate(35 112 44)"><rect x="104" y="14" width="16" height="56" rx="3" class="f-sao"/><path d="M104,70 h16 l-8,16z" class="f-da"/><path d="M109,80 h6 l-3,6z" class="f-muc"/><rect x="104" y="10" width="16" height="8" rx="3" class="f-son"/></g>' +
      '<path d="M8,30 h22 M14,44 h20 M8,58 h18" class="s-xam" stroke-width="4" stroke-linecap="round"/>' +
      '<path d="M146,18 q-6,10 0,14 q6,-4 0,-14z" class="f-troi"/>'),
    "ngu-quen": boc(
      '<rect x="14" y="62" width="132" height="22" rx="6" class="f-goc"/>' +
      '<rect x="14" y="84" width="10" height="16" class="f-goc-dam"/><rect x="136" y="84" width="10" height="16" class="f-goc-dam"/>' +
      '<rect x="20" y="40" width="44" height="26" rx="12" class="f-trang s-vien" stroke-width="3"/>' +
      mat(44, 46, 18, "ngu") +
      '<path d="M58,56 h82 a6,6 0 0 1 6,6 v4 h-88z" class="f-goc-nhat"/>' +
      '<text x="96" y="34" font-size="18" class="f-muc" font-family="Nunito, sans-serif" font-weight="800">Z</text>' +
      '<text x="112" y="22" font-size="22" class="f-muc" font-family="Nunito, sans-serif" font-weight="800">Z</text>' +
      '<text x="132" y="12" font-size="14" class="f-muc" font-family="Nunito, sans-serif" font-weight="800" dy="6">z</text>'),
    "hoc-cham": boc(
      mat(70, 38, 24, "cuoi") +
      '<rect x="18" y="74" width="124" height="12" rx="4" class="f-goc"/>' +
      '<rect x="26" y="86" width="8" height="18" class="f-goc-dam"/><rect x="126" y="86" width="8" height="18" class="f-goc-dam"/>' +
      sach(40, 54, 64) + ngoiSao(128, 26, 16)),
    "khoc-nhe": boc(
      '<rect x="22" y="56" width="116" height="34" rx="16" class="f-goc-nhat"/>' +
      mat(80, 50, 32, "khoc") +
      '<text x="154" y="26" text-anchor="end" font-size="17" class="f-xam" font-family="Nunito, sans-serif" font-weight="800">hu hu</text>'),
    "day-dung-gio": boc(
      matTroi(28, 28, 13) + dongHo(86, 62, 26) + mat(130, 70, 16, "cuoi")),
    "me-nheo": boc(
      mat(66, 58, 30, "phung") +
      '<path d="M100,14 h44 a8,8 0 0 1 8,8 v14 a8,8 0 0 1 -8,8 h-30 l-10,8 l2,-8 h-6 a8,8 0 0 1 -8,-8 v-14 a8,8 0 0 1 8,-8z" class="f-trang s-vien" stroke-width="3"/>' +
      '<text x="122" y="35" text-anchor="middle" font-size="16" class="f-son" font-family="Nunito, sans-serif" font-weight="800">Không!</text>'),
    "hoc-nhanh": boc(
      '<path d="M10,40 h30 M16,56 h26 M10,72 h28" class="s-xam" stroke-width="4" stroke-linecap="round"/>' +
      '<rect x="90" y="8" width="16" height="10" rx="3" class="f-son"/>' +
      '<circle cx="98" cy="60" r="38" class="f-trang s-muc" stroke-width="5"/>' +
      '<path d="M98,60 V32 M98,60 L118,72" class="s-son" stroke-width="5" stroke-linecap="round"/>' +
      '<circle cx="98" cy="60" r="4" class="f-muc"/>'),
    "hoc-vet": boc(
      sach(40, 72, 80) + mat(80, 40, 26, "hoi") +
      '<text x="20" y="40" font-size="26" class="f-son" font-family="Nunito, sans-serif" font-weight="900">?</text>' +
      '<text x="124" y="34" font-size="30" class="f-son" font-family="Nunito, sans-serif" font-weight="900">?</text>' +
      '<text x="132" y="68" font-size="20" class="f-son" font-family="Nunito, sans-serif" font-weight="900">?</text>'),
    "hieu-bai": boc(
      sach(36, 72, 88) +
      '<path d="M80,6 a26,26 0 0 1 14,48 v6 h-28 v-6 a26,26 0 0 1 14,-48z" class="f-sao"/>' +
      '<rect x="68" y="60" width="24" height="8" rx="3" class="f-xam"/>' +
      '<path d="M40,26 h-12 M120,26 h12 M50,8 l-8,-6 M110,8 l8,-6" class="s-sao" stroke-width="4" stroke-linecap="round"/>' +
      '<path d="M70,30 l7,8 l14,-16" class="s-trang" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'),
    "sau-tuoi": boc(
      '<rect x="30" y="58" width="100" height="40" rx="8" class="f-goc"/>' +
      '<rect x="30" y="58" width="100" height="12" rx="6" class="f-trang"/>' +
      '<path d="M30,70 q12,10 25,0 q12,10 25,0 q12,10 25,0 q12,10 25,0" class="f-trang"/>' +
      '<g class="f-son">' + [44, 58, 72, 86, 100, 114].map(function (x) { return '<rect x="' + (x - 3) + '" y="36" width="6" height="22" rx="2"/>'; }).join("") + '</g>' +
      '<g class="f-sao">' + [44, 58, 72, 86, 100, 114].map(function (x) { return '<path d="M' + x + ',22 q6,8 0,12 q-6,-4 0,-12z"/>'; }).join("") + '</g>'),
    "vo-long": boc(
      sach(28, 70, 104) +
      '<path d="M80,74 V40" class="s-dung" stroke-width="5" stroke-linecap="round"/>' +
      '<path d="M80,52 q-26,-4 -30,-26 q24,2 30,26z" class="f-lua"/>' +
      '<path d="M80,44 q22,-6 28,-28 q-22,4 -28,28z" class="f-lua"/>')
  };
  window.HINH = HINH;
})();
