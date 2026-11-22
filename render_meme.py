import base64
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / "assets"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

mark_b64 = base64.b64encode((ASSETS / "mark-1024.png").read_bytes()).decode("ascii")

HTML = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1536px;
    height: 960px;
    overflow: hidden;
    background: radial-gradient(circle at 15% 15%, #2a183b 0%, #151125 55%, #0c1824 100%);
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }}
  .glow-top {{
    position: absolute;
    top: -120px; left: -80px;
    width: 650px; height: 320px;
    background: radial-gradient(ellipse, rgba(236, 72, 153, 0.30), transparent 70%);
    pointer-events: none;
  }}
  .glow-bot {{
    position: absolute;
    bottom: -120px; right: -80px;
    width: 720px; height: 360px;
    background: radial-gradient(ellipse, rgba(20, 184, 166, 0.28), transparent 70%);
    pointer-events: none;
  }}

  .sheet {{
    width: 1436px;
    height: 876px;
    background: #fcf9f2;
    border-radius: 14px;
    box-shadow: 0 28px 70px rgba(0,0,0,0.62), 0 0 0 2px rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding: 36px 48px 34px 48px;
    color: #16181f;
  }}

  .top-stripe {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 14px;
    background: linear-gradient(90deg, #0d9488 0%, #14b8a6 45%, #ec4899 75%, #c026d3 100%);
  }}

  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 4px solid #16181f;
    padding-bottom: 18px;
    margin-top: 6px;
  }}
  .hosp-left {{
    display: flex;
    align-items: center;
    gap: 18px;
  }}
  .cross-box {{
    width: 68px;
    height: 68px;
    border-radius: 14px;
    background: #0d9488;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: inset 0 0 0 3px #16181f;
  }}
  .hosp-title {{
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 0.6px;
    color: #11131a;
    line-height: 1.05;
  }}
  .hosp-sub {{
    font-size: 20px;
    font-weight: 700;
    color: #0f766e;
    letter-spacing: 1.6px;
    margin-top: 5px;
    text-transform: uppercase;
  }}
  .badge-right {{
    text-align: right;
  }}
  .excuse-pill {{
    display: inline-block;
    background: #16181f;
    color: #fcf9f2;
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 1.4px;
    padding: 9px 18px;
    border-radius: 8px;
    text-transform: uppercase;
  }}
  .date-line {{
    font-size: 20px;
    font-weight: 700;
    color: #475569;
    margin-top: 8px;
    font-family: "Consolas", "Courier New", monospace;
  }}

  .form-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 18px;
    padding-top: 20px;
  }}

  .field {{
    display: flex;
    align-items: baseline;
    gap: 16px;
    border-bottom: 2px dashed #cbd5e1;
    padding-bottom: 13px;
  }}
  .label {{
    width: 225px;
    flex-shrink: 0;
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 1px;
    color: #0f766e;
    text-transform: uppercase;
  }}
  .value {{
    font-size: 29px;
    font-weight: 800;
    color: #111827;
    line-height: 1.25;
  }}
  .value .hi {{
    color: #be185d;
  }}
  .value .sub {{
    font-weight: 700;
    color: #334155;
  }}

  .rx-box {{
    background: #eef6f6;
    border: 2px solid #99f6e4;
    border-left: 10px solid #0d9488;
    border-radius: 10px;
    padding: 18px 24px;
    display: flex;
    align-items: flex-start;
    gap: 20px;
  }}
  .rx-sym {{
    font-size: 54px;
    font-weight: 900;
    color: #0d9488;
    line-height: 1;
    font-family: Georgia, serif;
    margin-top: 2px;
  }}
  .rx-text {{
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.32;
  }}
  .rx-text .muted {{
    color: #334155;
    font-weight: 700;
  }}

  .symptoms-row {{
    display: flex;
    align-items: center;
    gap: 16px;
    padding-top: 4px;
  }}
  .symptoms-grid {{
    display: flex;
    gap: 14px;
    flex: 1;
  }}
  .sym-chip {{
    flex: 1;
    background: #ffffff;
    border: 2px solid #cbd5e1;
    border-radius: 10px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 22px;
    font-weight: 800;
    color: #1e293b;
  }}
  .sym-check {{
    width: 30px;
    height: 30px;
    border-radius: 7px;
    background: #be185d;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 900;
    flex-shrink: 0;
  }}

  .bottom-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-top: auto;
    padding-top: 10px;
    gap: 24px;
  }}

  .sig-block {{
    width: 490px;
  }}
  .sig-script {{
    font-family: "Georgia", "Times New Roman", serif;
    font-style: italic;
    font-size: 38px;
    font-weight: 700;
    color: #1e293b;
    padding-left: 6px;
    margin-bottom: 4px;
  }}
  .sig-line {{
    border-top: 3px solid #16181f;
    padding-top: 8px;
    font-size: 22px;
    font-weight: 800;
    color: #1e293b;
  }}
  .sig-role {{
    font-size: 21px;
    font-weight: 800;
    color: #be185d;
    margin-top: 5px;
  }}

  .stamp-wrap {{
    transform: rotate(-3deg);
    background: #fdf2f8;
    border: 6px solid #be185d;
    border-radius: 20px;
    padding: 16px 26px 16px 20px;
    box-shadow: 0 0 0 4px #fcf9f2, 0 0 0 8px #be185d, 0 12px 26px rgba(190, 24, 93, 0.22);
    display: flex;
    align-items: center;
    gap: 22px;
    max-width: 850px;
  }}
  .stamp-mark {{
    width: 144px;
    height: 144px;
    flex-shrink: 0;
    display: block;
  }}
  .stamp-copy {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  .stamp-kicker {{
    font-size: 19px;
    font-weight: 900;
    letter-spacing: 1.8px;
    color: #9d174d;
    text-transform: uppercase;
  }}
  .stamp-brand {{
    font-size: 44px;
    font-weight: 900;
    color: #11131a;
    line-height: 1.02;
    letter-spacing: -0.5px;
  }}
  .stamp-brand span {{
    color: #be185d;
  }}
  .stamp-sub {{
    font-size: 24px;
    font-weight: 800;
    color: #1e293b;
    line-height: 1.24;
    margin-top: 2px;
  }}
</style>
</head>
<body>
  <div class="glow-top"></div>
  <div class="glow-bot"></div>
  <div class="sheet">
    <div class="top-stripe"></div>

    <div class="header">
      <div class="hosp-left">
        <div class="cross-box">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
            <rect x="15" y="4" width="10" height="32" rx="2" fill="#fcf9f2"/>
            <rect x="4" y="15" width="32" height="10" rx="2" fill="#fcf9f2"/>
          </svg>
        </div>
        <div>
          <div class="hosp-title">LEONIDA GENERAL HOSPITAL</div>
          <div class="hosp-sub">Vice City Dept. of Launch-Week Emergencies</div>
        </div>
      </div>
      <div class="badge-right">
        <div class="excuse-pill">DOCTOR&apos;S SICK NOTE</div>
        <div class="date-line">ISSUED: NOV 19, 2026 &nbsp;|&nbsp; CASE #VI-4811</div>
      </div>
    </div>

    <div class="form-body">
      <div class="field">
        <div class="label">PATIENT</div>
        <div class="value">Everyone who waited <span class="hi">13 years</span> <span class="sub">(Sept 17, 2013 &ndash; Nov 19, 2026)</span></div>
      </div>

      <div class="field">
        <div class="label">DIAGNOSIS</div>
        <div class="value">Acute <span class="hi">GTA VI Launch Fever</span> <span class="sub">(4,811-day incubation &middot; 247 GB SSD failure)</span></div>
      </div>

      <div class="rx-box">
        <div class="rx-sym">Rx</div>
        <div class="rx-text">
          Mandatory 7-day bed rest in Vice City with Jason &amp; Lucia.<br/>
          <span class="muted">No Slack. No standups. Return to work only after 100% completion.</span>
        </div>
      </div>

      <div class="symptoms-row">
        <div class="label">SYMPTOMS</div>
        <div class="symptoms-grid">
          <div class="sym-chip"><span class="sym-check">&#10003;</span>Sudden Vice City accent</div>
          <div class="sym-chip"><span class="sym-check">&#10003;</span>2 trailers memorized</div>
          <div class="sym-chip"><span class="sym-check">&#10003;</span>Allergic to Slack pings</div>
        </div>
      </div>
    </div>

    <div class="bottom-row">
      <div class="sig-block">
        <div class="sig-script">Dr. T. Vercetti, MD</div>
        <div class="sig-line">Chief of Unpaid PTO &middot; Leonida Health</div>
        <div class="sig-role">Unpaid sick days? Covered by stamp &rarr;</div>
      </div>

      <div class="stamp-wrap">
        <img class="stamp-mark" src="data:image/png;base64,{mark_b64}" alt="make.fun ghost" />
        <div class="stamp-copy">
          <div class="stamp-kicker">LOST WAGES COVERED BY</div>
          <div class="stamp-brand">make<span>.</span>fun</div>
          <div class="stamp-sub">My AI agent wins real $$$ bounties<br/>while I&apos;m &ldquo;too sick to work&rdquo; in Vice City</div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

html_path = OUT / "meme.html"
png_path = ROOT / "meme.png"
preview_path = OUT / "preview_768x480.jpg"
html_path.write_text(HTML, encoding="utf-8")

with sync_playwright() as p:
    chrome_exe = Path(r"C:\Users\jiaao\AppData\Local\ms-playwright\chromium-1223\chrome-win64\chrome.exe")
    launch_kw = {"headless": True}
    if chrome_exe.exists():
        launch_kw["executable_path"] = str(chrome_exe)
    else:
        launch_kw["channel"] = "chrome"
    browser = p.chromium.launch(**launch_kw)
    page = browser.new_page(viewport={"width": 1536, "height": 960}, device_scale_factor=1)
    page.goto(html_path.as_uri(), wait_until="networkidle")
    page.screenshot(path=str(png_path), type="png")
    browser.close()

img = Image.open(png_path).convert("RGB")
preview = img.resize((768, 480), Image.Resampling.LANCZOS)
preview.save(preview_path, "JPEG", quality=90)
print(f"Rendered {png_path} ({img.size}, {png_path.stat().st_size} bytes)")
print(f"Judge preview {preview_path} ({preview.size}, {preview_path.stat().st_size} bytes)")
