"""Mở lần lượt các bài, báo lỗi trang và các phần còn 'Sắp có'."""
import asyncio, sys
from playwright.async_api import async_playwright
sys.path.insert(0, '/home/claude/tools')
from chup import phuc_vu
async def main(ds):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1024, "height": 900}); loi = []
        await pg.route("https://mau.cvcec.org/**", lambda r: phuc_vu(r, '/home/claude/mau-chung/', 'mau.cvcec.org/'))
        await pg.route("https://cuocsong.cvcec.org/**", lambda r: phuc_vu(r, '/home/claude/baihoccuocsong/', 'cuocsong.cvcec.org/'))
        pg.on("pageerror", lambda e: loi.append(f"pageerror: {e}"))
        for h in ds:
            n0 = len(loi)
            await pg.goto("about:blank"); await pg.goto("https://cuocsong.cvcec.org/kho.html#" + h); await pg.wait_for_timeout(600)
            r = await pg.evaluate("""() => ({sap: [...document.querySelectorAll('.bh-sap-co li')].map(e=>e.textContent.trim()),
                 phan: [...document.querySelectorAll('section h2')].length, tranh: document.querySelectorAll('.bh-lua-chon svg').length})""")
            print(h, '| mục', r['phan'], '| tranh', r['tranh'], '| sắp có:', r['sap'], loi[n0:] or '')
        await b.close()
asyncio.run(main(sys.argv[1:]))
