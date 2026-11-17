"""Chụp trang cuocsong như đang ở tên miền thật (định tuyến về tệp trong máy), gỡ màn khoá 'chỉ học qua cổng'."""
import asyncio, sys, mimetypes, os
from playwright.async_api import async_playwright
GOC = '/home/claude/baihoccuocsong/'; MAU = '/home/claude/mau-chung/'
async def phuc_vu(route, goc, tien_to):
    duong = route.request.url.split(tien_to, 1)[-1].split('?')[0].split('#')[0] or 'index.html'
    p = goc + duong
    if not os.path.isfile(p): return await route.fulfill(status=404, body='')
    ct = mimetypes.guess_type(p)[0] or 'application/octet-stream'
    if ct.startswith('text/') or ct.endswith('javascript'): ct += '; charset=utf-8'
    await route.fulfill(status=200, body=open(p, 'rb').read(), headers={'content-type': ct})
async def main(trang, co):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        loi = []
        for w, h, tag in co:
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.route("https://mau.cvcec.org/**", lambda r: phuc_vu(r, MAU, 'mau.cvcec.org/'))
            await pg.route("https://cuocsong.cvcec.org/**", lambda r: phuc_vu(r, GOC, 'cuocsong.cvcec.org/'))
            pg.on("pageerror", lambda e: loi.append(f"pageerror: {e}"))
            pg.on("console", lambda m: loi.append(f"console: {m.text}") if m.type == 'error' else None)
            for url, ten in trang:
                await pg.goto("https://cuocsong.cvcec.org/" + url); await pg.wait_for_timeout(800)
                await pg.evaluate("""() => { const m = document.querySelector('.ttv-man-khoa'); if (m) m.remove();
                  document.querySelectorAll('[inert]').forEach(e => { e.removeAttribute('inert'); e.removeAttribute('aria-hidden'); });
                  document.documentElement.style.overflow = ''; }""")
                await pg.wait_for_timeout(700)
                await pg.screenshot(path=f"/home/claude/scratch/{tag}_{ten}.png", full_page=False)
                if await pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1"): loi.append(f"{tag} {ten}: tràn ngang")
            await pg.close()
        await b.close()
        print("\n".join(loi) or "ok")
if __name__ == "__main__":
  trang = [tuple(x.split('=')) for x in sys.argv[1:]] or [("index.html", "idx"), ("kho.html#lentam-3", "lt3")]
  asyncio.run(main(trang, [(1024, 900, 'ipad'), (390, 844, 'phone')]))
