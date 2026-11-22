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
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: linear-gradient(145deg, #2a103b 0%, #141226 52%, #0a2429 100%);
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 34px;
  }}

  .card {{
    width: 956px;
    height: 956px;
    background: #fcfaf4;
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.55);
    display: flex;
    flex-direction: column;
    position: relative;
    color: #11131a;
  }}

  .header {{
    background: #13161f;
    color: #fcfaf4;
    padding: 22px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .header-left {{
    display: flex;
    align-items: center;
    gap: 18px;
  }}
  .cross-badge {{
    width: 58px;
    height: 58px;
    border-radius: 12px;
    background: #14b8a6;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .hosp-name {{
    font-size: 31px;
    font-weight: 900;
    letter-spacing: 0.4px;
    line-height: 1.08;
  }}
  .hosp-dept {{
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1.8px;
    color: #5eead4;
    margin-top: 4px;
    text-transform: uppercase;
  }}
  .case-box {{
    text-align: right;
    border-left: 2px solid rgba(255,255,255,0.16);
    padding-left: 20px;
  }}
  .case-kicker {{
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1.8px;
    color: #94a3b8;
    text-transform: uppercase;
  }}
  .case-val {{
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
    margin-top: 2px;
  }}

  .main {{
    flex: 1;
    padding: 24px 34px 16px 34px;
    display: flex;
    flex-direction: column;
    position: relative;
  }}

  .dates-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    position: relative;
    padding-bottom: 14px;
  }}
  .dates-left {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .meta-k {{
    font-size: 14px;
    font-weight: 900;
    letter-spacing: 1.4px;
    color: #64748b;
    text-transform: uppercase;
  }}
  .meta-v {{
    font-size: 25px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.15;
    margin-top: 1px;
  }}

  .red-stamp {{
    transform: rotate(-7deg);
    border: 6px solid #dc2626;
    border-radius: 14px;
    padding: 10px 22px;
    color: #dc2626;
    text-align: center;
    background: rgba(254, 242, 242, 0.85);
    box-shadow: 0 0 0 3px #fcfaf4, 0 0 0 6px rgba(220, 38, 38, 0.35);
    margin-top: 2px;
    margin-right: 4px;
  }}
  .stamp-top {{
    font-size: 34px;
    font-weight: 900;
    line-height: 1;
    letter-spacing: 1px;
  }}
  .stamp-bot {{
    font-size: 26px;
    font-weight: 900;
    line-height: 1.08;
    letter-spacing: 3px;
    margin-top: 2px;
  }}

  .reason-row {{
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 13px 0 15px 0;
    border-top: 2px solid #cbd5e1;
    border-bottom: 2px solid #cbd5e1;
    font-size: 21px;
    font-weight: 900;
    color: #1e293b;
  }}
  .reason-label {{
    font-size: 16px;
    letter-spacing: 1.5px;
    color: #64748b;
  }}
  .chk-item {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .chk-box {{
    width: 26px;
    height: 26px;
    border: 3px solid #1e293b;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    font-weight: 900;
  }}
  .chk-box.on {{
    border-color: #dc2626;
    color: #dc2626;
    background: #fef2f2;
  }}

  .bill {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 14px;
    padding: 20px 0 18px 0;
    flex: 1;
  }}
  .line-item {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 26px;
    font-weight: 800;
    color: #1e293b;
    border-bottom: 1.5px dashed #cbd5e1;
    padding-bottom: 11px;
  }}
  .line-item:last-child {{
    border-bottom: none;
    padding-bottom: 0;
  }}
  .line-price {{
    font-weight: 900;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 28px;
    color: #0f172a;
    flex-shrink: 0;
    margin-left: 14px;
  }}

  .total-row {{
    border-top: 4px solid #13161f;
    padding-top: 12px;
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }}
  .total-label {{
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 0.6px;
    color: #13161f;
  }}
  .total-amt {{
    font-size: 46px;
    font-weight: 900;
    color: #13161f;
    font-family: "Consolas", "Courier New", monospace;
    line-height: 1;
  }}

  .footer {{
    background: linear-gradient(90deg, #b8146b 0%, #db2777 100%);
    padding: 18px 34px;
    display: flex;
    align-items: center;
    gap: 26px;
    color: #ffffff;
  }}
  .ghost-wrap {{
    width: 174px;
    height: 174px;
    flex-shrink: 0;
    background: #ffffff;
    border-radius: 50%;
    padding: 6px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.28);
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .ghost-img {{
    width: 162px;
    height: 162px;
    display: block;
  }}
  .footer-copy {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .footer-title {{
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 0.5px;
    line-height: 1.06;
    text-transform: uppercase;
  }}
  .footer-sub {{
    font-size: 22px;
    font-weight: 700;
    color: #fdf2f8;
    line-height: 1.25;
  }}
  .brand-pill {{
    align-self: flex-start;
    margin-top: 4px;
    background: #ffffff;
    border: 4px solid #13161f;
    border-radius: 999px;
    padding: 6px 26px 8px 26px;
    font-size: 36px;
    font-weight: 900;
    color: #13161f;
    line-height: 1;
    letter-spacing: -0.5px;
  }}
  .brand-pill span {{
    color: #db2777;
  }}
</style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="header-left">
        <div class="cross-badge">
          <svg width="34" height="34" viewBox="0 0 40 40" fill="none">
            <rect x="15" y="4" width="10" height="32" rx="2" fill="#13161f"/>
            <rect x="4" y="15" width="32" height="10" rx="2" fill="#13161f"/>
          </svg>
        </div>
        <div>
          <div class="hosp-name">LEONIDA GENERAL HOSPITAL</div>
          <div class="hosp-dept">Vice City ER &middot; Launch-Week Statement</div>
        </div>
      </div>
      <div class="case-box">
        <div class="case-kicker">CASE</div>
        <div class="case-val">V &rarr; VI</div>
      </div>
    </div>

    <div class="main">
      <div class="dates-row">
        <div class="dates-left">
          <div>
            <div class="meta-k">ADMITTED</div>
            <div class="meta-v">LOS SANTOS &middot; SEP 17, 2013</div>
          </div>
          <div>
            <div class="meta-k">DISCHARGED (SICK NOTE INCLUDED)</div>
            <div class="meta-v">VICE CITY &middot; NOV 19, 2026</div>
          </div>
        </div>
        <div class="red-stamp">
          <div class="stamp-top">13 YEARS</div>
          <div class="stamp-bot">WAITING</div>
        </div>
      </div>

      <div class="reason-row">
        <span class="reason-label">DIAGNOSIS</span>
        <span class="chk-item"><span class="chk-box"></span>ACTUALLY SICK</span>
        <span class="chk-item"><span class="chk-box on">&#10003;</span>GTA VI LAUNCH FEVER</span>
      </div>

      <div class="bill">
        <div class="line-item">
          <span>Waiting room chair (4,811 days)</span>
          <span class="line-price">$1,300</span>
        </div>
        <div class="line-item">
          <span>2 delay relapses (&ldquo;Fall 2025&rdquo;, &ldquo;May 2026&rdquo;)</span>
          <span class="line-price">$26</span>
        </div>
        <div class="line-item">
          <span>247 GB SSD emergency transplant</span>
          <span class="line-price">$247</span>
        </div>
        <div class="line-item">
          <span>Leonida alligator bite (Ocean Drive)</span>
          <span class="line-price">$253</span>
        </div>
        <div class="line-item">
          <span>Doctor&apos;s note for boss (Jason &amp; Lucia)</span>
          <span class="line-price">$200</span>
        </div>
      </div>

      <div class="total-row">
        <span class="total-label">TOTAL DUE</span>
        <span class="total-amt">$2,026</span>
      </div>
    </div>

    <div class="footer">
      <div class="ghost-wrap">
        <img class="ghost-img" src="data:image/png;base64,{mark_b64}" alt="make.fun ghost" />
      </div>
      <div class="footer-copy">
        <div class="footer-title">PAID BY MY AI AGENT</div>
        <div class="footer-sub">People &amp; AI agents win real money on</div>
        <div class="brand-pill">make<span>.</span>fun</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

html_path = OUT / "meme.html"
png_path = ROOT / "meme.png"
preview_path = OUT / "preview_480x480.jpg"
html_path.write_text(HTML, encoding="utf-8")

with sync_playwright() as p:
    chrome_exe = Path(r"C:\Users\jiaao\AppData\Local\ms-playwright\chromium-1223\chrome-win64\chrome.exe")
    launch_kw = {"headless": True}
    if chrome_exe.exists():
        launch_kw["executable_path"] = str(chrome_exe)
    else:
        launch_kw["channel"] = "chrome"
    browser = p.chromium.launch(**launch_kw)
    page = browser.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
    page.goto(html_path.as_uri(), wait_until="networkidle")
    page.screenshot(path=str(png_path), type="png")
    browser.close()

img = Image.open(png_path).convert("RGB")
preview = img.resize((480, 480), Image.Resampling.LANCZOS)
preview.save(preview_path, "JPEG", quality=90)
print(f"Rendered {png_path} ({img.size}, {png_path.stat().st_size} bytes)")
print(f"Judge preview {preview_path} ({preview.size}, {preview_path.stat().st_size} bytes)")
