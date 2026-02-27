from flask import Flask, render_template_string
import subprocess
import requests

app = Flask(__name__)

# --- [ СЕКРЕТНЫЙ БЛОК TELEGRAM ] ---
TOKEN = "8509780467:AAEUm13wvtANYCAxzIxR_9OpRBPRMz4Mm50"
CHAT_ID = "1421473166"

# Состояние тревоги
alarm_active = False

def send_telegram(text):
    try:
        url = f"https://api.telegram.org{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except: pass

@app.route('/')
def index():
    # ЛОГИКА ЦВЕТА (ЗЕЛЕНЫЙ -> ЖЕЛТЫЙ)
    main_color = "#ffff00" if alarm_active else "#00ff41"
    sun_class = "sun-active" if alarm_active else ""
    status_text = "ALARM SYSTEM ACTIVATED" if alarm_active else "SYSTEM: ONLINE"
    
    html_layout = f"""
<html>
<head>
<title>M.A.R.V.E.L. - SOLAR ALARM</title>
<style>
body {{ background: black; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; color: {main_color}; }}
#matrix-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; }}
.wrapper {{ display: flex; justify-content: center; align-items: flex-start; gap: 20px; padding-top: 30px; position: relative; z-index: 1; }}
.main-panel {{ border: 2px solid {main_color}; padding: 20px; box-shadow: 0 0 20px {main_color}; background: rgba(0, 0, 0, 0.9); border-radius: 15px; text-align: center; min-width: 350px; }}
.side-container {{ display: flex; flex-direction: column; gap: 20px; }}
.side-widget {{ border: 1px solid cyan; padding: 15px; box-shadow: 0 0 15px cyan; background: rgba(0, 5, 10, 0.9); border-radius: 10px; min-width: 280px; text-align: center; }}
.btn {{ background: none; border: 1px solid {main_color}; color: {main_color}; padding: 12px; cursor: pointer; font-weight: bold; margin: 5px; width: 100%; text-transform: uppercase; transition: 0.3s; }}
.btn:hover {{ background: {main_color}; color: #000; box-shadow: 0 0 25px {main_color}; }}

/* --- СОЛНЦЕ АЛАРМА --- */
.alarm-sun {{ width: 50px; height: 50px; border-radius: 50%; margin: 0 auto 10px; background: #111; border: 2px solid #333; transition: all 0.5s ease; }}
.sun-active {{ background: #ffff00; border-color: #fff; box-shadow: 0 0 50px 15px #ffff00; animation: pulse 1s infinite alternate; }}
@keyframes pulse {{ from {{ transform: scale(1); opacity: 0.8; }} to {{ transform: scale(1.1); opacity: 1; }} }}

/* ТЕАТР ЗОМБИ */
#zombie-stage {{ height: 140px; position: relative; overflow: hidden; border: 1px solid #333; background: #050505; border-radius: 5px; margin-top: 10px; }}
.zombie-unit {{ position: absolute; display: flex; flex-direction: column; align-items: center; animation: walk 15s linear infinite, bob 0.8s ease-in-out infinite alternate; bottom: 10px; }}
.zombie-icon {{ font-size: 40px; text-shadow: 0 0 15px #0f0; }}
.zombie-id {{ font-size: 8px; color: #555; }}
@keyframes walk {{ from {{ left: -200px; }} to {{ left: 110%; }} }}
@keyframes bob {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-10px); }} }}
</style>
</head>
<body>
<canvas id="matrix-canvas"></canvas>
<div class="wrapper">
    <div class="main-panel">
        <h1>🛡️ J.A.R.V.I.S. CORE</h1>
        <p style="color:cyan; font-size:0.75em;">TARGET_MAC: 60:7E:CD:06:86:B3 [HUAWEI]</p>
        <hr style="border: 0.5px solid #222;">
        <a href="/run_nmap"><button class="btn">📡 SCAN NETWORK</button></a><br>
        <a href="/run_sniffer"><button class="btn">🕵️‍♂️ WEB RECON</button></a><br>
        <a href="/run_xray"><button class="btn">📡 X-RAY SCAN</button></a><br>
        <a href="/toggle_alarm"><button class="btn" style="border-color:red; color:red;">🚨 TOGGLE ALARM</button></a>
    </div>
    <div class="side-container">
        <div class="side-widget" style="border-color: #88ff88; box-shadow: 0 0 10px #0f0;">
            <h3 style="margin:0 0 10px 0; font-size:0.7em; color:#88ff88;">NECRO-LOGIC STAGE:</h3>
            <div class="alarm-sun {sun_class}"></div> <!-- НАШЕ СОЛНЦЕ -->
            <div id="zombie-stage">
                <div class="zombie-unit" style="animation-delay: 0s;"><span class="zombie-icon">🧟</span><span class="zombie-id">192.168.100.1</span></div>
                <div class="zombie-unit" style="animation-delay: 6s;"><span class="zombie-icon">🧟</span><span class="zombie-id">TARGET: HUAWEI</span></div>
            </div>
        </div>
        <div class="side-widget">
            <p id="clock" style="font-size:2em; color:cyan; margin:0;">00:00:00</p>
            <p id="full-date" style="font-size:0.8em; color:white; margin:0;">27.02.2026</p>
        </div>
    </div>
</div>
<script>
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth; canvas.height = window.innerHeight;
const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const fontSize = 16; const columns = canvas.width / fontSize;
const drops = []; for (let i = 0; i < columns; i++) drops[i] = 1;
function draw() {{
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '{main_color}'; ctx.font = fontSize + 'px arial';
    for (let i = 0; i < drops.length; i++) {{
        const text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    }}
}}
setInterval(draw, 33);
function updateClock() {{
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleTimeString();
    document.getElementById('full-date').innerText = now.toLocaleDateString();
}}
setInterval(updateClock, 1000); updateClock();
</script>
</body>
</html>
"""
    return render_template_string(html_layout)

@app.route('/toggle_alarm')
def toggle_alarm():
    global alarm_active
    alarm_active = not alarm_active
    status = "ТРЕВОГА ВКЛЮЧЕНА" if alarm_active else "ТРЕВОГА ВЫКЛЮЧЕНА"
    send_telegram(f"🚨 ВНИМАНИЕ: {status}") # УВЕДОМЛЕНИЕ В TG ПРИ ПЕРЕКЛЮЧЕНИИ
    return """<script>window.location.href='/';</script>"""

@app.route('/run_nmap')
def run_nmap():
    try:
        res = subprocess.check_output(["nmap", "-F", "192.168.100.1"], stderr=subprocess.STDOUT)
        send_telegram("📡 SCAN COMPLETED")
        return f"<body style='background:black;color:#0f0;padding:20px;'><h3>📡 REPORT:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>BACK</a></body>"
    except Exception as e: return f"<h3>ERROR: {e}</h3>"

@app.route('/run_xray')
def run_xray():
    try:
        res = subprocess.check_output(["nmap", "-sV", "192.168.100.1"], stderr=subprocess.STDOUT)
        report = res.decode('utf-8')
        send_telegram(f"🕵️‍♂️ X-RAY REPORT:\n{report}")
        return f"<body style='background:black;color:cyan;padding:20px;'><h3>📡 X-RAY REPORT SENT:</h3><pre>{report}</pre><br><a href='/' style='color:yellow;'>BACK</a></body>"
    except Exception as e: return f"<h3>ERROR: {e}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
