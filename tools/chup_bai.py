"""Chụp toàn trang một bài (iPad hoặc điện thoại), cắt thành nhiều ảnh để xem."""
import asyncio, sys
from playwright.async_api import async_playwright
sys.path.insert(0, '/home/claude/tools')
from chup import phuc_vu
from PIL import Image
async def main(hash_, w, ten):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": w, "height": 900}); loi = []
        await pg.route("https://mau.cvcec.org/**", lambda r: phuc_vu(r, '/home/claude/mau-chung/', 'mau.cvcec.org/'))
        await pg.route("https://cuocsong.cvcec.org/**", lambda r: phuc_vu(r, '/home/claude/baihoccuocsong/', 'cuocsong.cvcec.org/'))
        pg.on("pageerror", lambda e: loi.append(f"pageerror: {e}"))
        pg.on("console", lambda m: loi.append(f"console: {m.text}") if m.type == 'error' else None)
        await pg.goto("https://cuocsong.cvcec.org/kho.html#" + hash_); await pg.wait_for_timeout(900)
        await pg.evaluate("""() => { const m = document.querySelector('.ttv-man-khoa'); if (m) m.remove();
          document.querySelectorAll('[inert]').forEach(e => { e.removeAttribute('inert'); e.removeAttribute('aria-hidden'); }); document.documentElement.style.overflow=''; }""")
        await pg.wait_for_timeout(400)
        # mở hết phần tiếng Anh và bấm thử câu hỏi đầu
        await pg.screenshot(path=f"/home/claude/scratch/{ten}.png", full_page=True)
        thieu = await pg.evaluate("[...document.querySelectorAll('.bh-thieu li, #phan-sap li')].map(e=>e.textContent)")
        await b.close()
    im = Image.open(f"/home/claude/scratch/{ten}.png"); H = im.size[1]; k = 0
    for y in range(0, H, 1800):
        im.crop((0, y, im.size[0], min(H, y + 1800))).save(f"/home/claude/scratch/{ten}_{k}.png"); k += 1
    print(loi or 'ok', '| sắp có:', thieu, '| số ảnh', k, 'cao', H)
asyncio.run(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1024, sys.argv[3] if len(sys.argv) > 3 else 'bai'))
