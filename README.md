# Bài học cuộc sống – cuocsong.cvcec.org

Góc học "Bài học cuộc sống" của Trường Tiếng Việt Của Em (CVCEC): hai bài thơ "Lên Sáu" và "Lên Tám" của Tản Đà. Quy tắc và cấu trúc kho: xem [CLAUDE.md](CLAUDE.md); công cụ: [tools/README.md](tools/README.md).

- Ghi kết quả học (từ 17-11-2026): xong một hoạt động có sao, kho.html gọi `TTV.ghiKetQua({ bai: "lensau-3", hoatDong: "hoi", soTroChoi, diem, diemToiDa, sao, thoiGianGiay })` của bộ mẫu; cổng ghi vào tài khoản. Không thêm khoá localStorage mới.

## Kết quả từng câu (từ 26-11-2026)

kho.html gửi thêm `cau` (tối đa 40) trong cùng lần gọi `TTV.ghiKetQua`, theo hợp đồng ở README của bộ mẫu (mau-chung). Mỗi câu ghi lần trả lời **đầu tiên** trong lượt mở trang; chỉ giữ trong bộ nhớ, không thêm khoá localStorage. `tu` luôn lấy từ dữ liệu bài (≤30 ký tự), không bao giờ là chữ người học chọn hay gõ.

| Hoạt động | `ma` | `tu` | `mang` | `loi` khi sai |
|---|---|---|---|---|
| `hoi` – Trả lời câu hỏi | `hoi-1`, `hoi-2`… | cụm trong “…” của câu hỏi “… nghĩa là gì?”, còn lại là đáp án đúng | `tu-vung` (cụm ≤3 tiếng hỏi nghĩa), còn lại `doc-hieu` | `nghia` |
| `viet` – mức Dễ, điền từ | `viet-de-1`… (thứ tự chỗ trống) | từ đúng của chỗ trống | `viet` | `TTV.loaiLoi(dapAn, chon)` nếu bộ mẫu có, không thì `nghia` |

Lật thẻ từ, nghe thơ, xem video, nghe giảng, việc tốt và viết mức Vừa/Khó không có đúng/sai nên không gửi `cau`. Sao `viet` đến từ mức Vừa/Khó trước thì lượt đó không có `cau`. Đã thử bằng Playwright (bọc `TTV.ghiKetQua` trên localhost, Lên Sáu Bài 1).
