import base64, json
from playwright.sync_api import sync_playwright

URL = "https://mhvnsnt.github.io/western-heart/game/"
OUT = "/home/hatch/workspace/your_files"
errs, failed = [], []

STEP_JS = """() => {
  const hud = document.getElementById('hud');
  if (hud && hud.className.includes('active')) return 'HUD';
  const screens = [...document.querySelectorAll('.screen.active')].map(e => e.id);
  const act = document.querySelector('.screen.active');
  if (act) {
    const btns = [...act.querySelectorAll('button')].filter(b => !b.disabled && b.offsetParent !== null);
    const conf = btns.find(b => /confirm|start|fight|random/i.test(b.textContent || '') || b.id === 'confirm-stage' || b.id === 'random-stage');
    if (conf) { conf.click(); return 'clicked:' + (conf.id || conf.textContent.trim()); }
  }
  return 'screens:' + screens.join(',');
}"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=[
        "--enable-unsafe-swiftshader", "--use-gl=angle", "--use-angle=swiftshader",
        "--no-sandbox", "--disable-dev-shm-usage", "--mute-audio", "--ignore-certificate-errors",
    ])
    ctx = b.new_context(viewport={"width": 1280, "height": 800}, proxy={"server": "http://127.0.0.1:18080"})
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.on("requestfailed", lambda r: failed.append(r.url))
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(10000)
    pg.click('[data-action="mode-training"]', timeout=15000)
    pg.wait_for_timeout(4000)
    r = pg.evaluate("() => { const c=[...document.querySelectorAll('[data-fighter=\"pantera\"],[data-id=\"pantera\"]')]; if(c.length){c[0].click(); return 'ok';} return 'notfound'; }")
    print("pantera click:", r, flush=True)
    pg.wait_for_timeout(3000)
    btn = pg.query_selector('#confirm-fighter')
    if btn and pg.evaluate("(b)=>!b.disabled", btn):
        btn.click(); print("confirmed fighter", flush=True)
    hud_on = False
    for i in range(16):
        pg.wait_for_timeout(6000)
        state = pg.evaluate(STEP_JS)
        print(f"step {i}: {state}", flush=True)
        if state == 'HUD':
            hud_on = True; break
    print("HUD REACHED:", hud_on, flush=True)
    pg.wait_for_timeout(8000)
    pb = pg.query_selector('[data-btn="punch"]')
    if pb:
        for _ in range(3):
            try: pb.click(timeout=3000)
            except Exception: pass
            pg.wait_for_timeout(700)
    for tag in ("a", "b"):
        data = pg.evaluate("""() => new Promise(res => {
          requestAnimationFrame(() => requestAnimationFrame(() => {
            const c = document.getElementById('game-canvas');
            try { res(c.toDataURL('image/png')); } catch(e) { res('ERR:'+e.message); }
          }));
        })""")
        if data and data.startswith("data:image"):
            path = f"{OUT}/live-deploy-fight-canvas-{tag}-20261020.png"
            open(path, "wb").write(base64.b64decode(data.split(",", 1)[1]))
            print("CANVAS SAVED", path, flush=True)
        else:
            print("CANVAS CAPTURE FAILED:", str(data)[:120], flush=True)
        pg.wait_for_timeout(2500)
    print("PAGEERRORS:", json.dumps(errs[:6]), flush=True)
    print("FAILED:", json.dumps(failed[:6]), flush=True)
    b.close()
print("DONE", flush=True)
