# Công cụ dựng nội dung – Bài học cuộc sống

Các tệp này để làm lại hoặc làm thêm bài (ví dụ Lên Tám bài 33 trở đi khi có ghi âm mới).
Chúng chạy trong máy làm việc của Claude (đường dẫn gốc `/home/claude/…`). Khi dùng lại, sửa các đường dẫn ở đầu tệp cho hợp.

## 1. Ghi âm cô Hà → dữ liệu bài (`am-thanh/`)
- `can_gio.py`, `can_neo.py`, `can_lentam.py`: căn mốc từng câu thơ và từng đoạn lời giảng trong ghi âm (theo năng lượng, đỉnh âm tiết và phổ mel; không cần nhận dạng giọng nói).
- `xuat_moi.py`: cắt `…-tho.mp3`, `…-giang.mp3` vào `audio/<bài thơ>/` và ghi mốc vào `data/`.
- `doi_chieu.py`: so hai bản ghi bằng phổ mel (tìm đoạn lặp, đoạn ghép).

## 2. Nội dung chữ
- `ghep_noi_dung.py`: ghép `noi-dung/<bài thơ>/NN.json` (dịch xuôi, từ khó, câu hỏi, viết, bài học…) vào `data/`.
- `kiem_hinh.py`: kiểm tra mã tranh ghép trong câu hỏi; `doc_bai.py`: in thơ và lời giảng một bài.
- `kiem_tat_ca.py`, `chup.py`, `chup_bai.py`: mở từng bài trong trình duyệt ẩn để tìm lỗi và chụp màn hình.
- `ve_tap_the.py`: vẽ lại banner khu tập thể (`js/canh-tap-the.js`).

## 3. Video Trâu Con (`video/`)
1. `python3 tao_video.py lentam 33 --kich-ban` – in lời Trâu Con của bài (soạn tự động từ dữ liệu bài).
2. `python3 lo_tts.py lentam:33 lentam:34 lentam:35` – in đoạn JavaScript dán lời vào AI Studio (Gemini TTS, giọng **Elio**, kiểu đọc: *Warm, gentle and slow, like a kind older friend reading to young children. Clear standard Northern Vietnamese pronunciation. Calm, friendly, a small pause after each line.*). Mỗi lượt 2–3 bài, tải tệp .wav về.
3. Ghi lượt mới vào `elio-nhat-ky.json` (tệp, các bài), rồi `python3 chia_neo.py <số lượt>` – cắt giọng thành từng câu: tìm các câu cố định bằng mẫu `mau_co_dinh.json`, phần giữa chia theo quãng lặng và giọng máy espeak (chỉ làm thước đo, không đưa vào video). Nếu AI Studio đọc lặp, truyền `khoi`/`het_khoi` như lượt 14.
4. `python3 kiem_toc_do.py` – báo câu có tốc độ nói lạ (có thể phụ đề lệch).
5. `python3 tao_video.py lentam 33 --xuat` – dựng video 1920×1080, 30 khung/giây vào `video/`, kèm ảnh bìa; rồi `python3 ../gan_video.py` để gắn vào dữ liệu bài.

`bai.html` là trang dựng hình (cần thư mục `assets/` ảnh Trâu Con chính thức và `fonts/` lấy từ CVCEC/mau-chung, cùng `cvcec-chung.css`). Màu góc lấy từ `TTV_DANH_SACH`.
