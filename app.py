from flask import Flask, render_template_string
import recon_tools  # МЫ ПОДКЛЮЧИЛИ НАШ МОДУЛЬ!
import subprocess
import requests

app = Flask(__name__)

# --- [ КОНФИГУРАЦИЯ J.A.R.V.I.S. ] ---
TOKEN = "8509780467:AAHBc_IkTBKWOHGPaVJnM00rnl57MiBEhfs"
CHAT_ID = "1421473166"
print(f"--- SYSTEM STATUS: {recon_tools.STATUS} ---")
recon_tools.scan_log("192.168.100.1", 53)

alarm_active = False

def send_telegram(text):
    try:
        url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"⚠️ TG ERROR: {e}")

# --- [ ЛОГИЧЕСКИЙ ДВИЖОК AI ] ---
def ai_analyze_report(report_text):
    analysis = "🧠 J.A.R.V.I.S. INTELLIGENCE REPORT:\n"
    if "53/tcp open" in report_text:
        analysis += "🔴 CRITICAL: DNS Port 53 is OPEN. Риск перехвата запросов!\n"
    if "Huawei" in report_text:
        analysis += "🟡 VENDOR: Huawei Technologies. Проверьте прошивку.\n"
    if "22/tcp filtered" in report_text:
        analysis += "🟢 SAFE: SSH Port is Hidden (Filtered).\n"
    analysis += "🛠️ ADVICE: Смените пароль админа и проверьте Firewall."
    return analysis

@app.route('/')
def index():
    main_color = "#ffff00" if alarm_active else "#00ff41"
    alarm_style = "animation: blink 1s infinite;" if alarm_active else ""
    
    html_layout = f"""
<html>
<head>
<title>J.A.R.V.I.S. - PARTICLE CORE</title>
<style>
body {{ background: black; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; color: {main_color}; }}
#matrix-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; }}
.wrapper {{ display: flex; justify-content: center; align-items: flex-start; gap: 20px; padding-top: 30px; position: relative; z-index: 1; }}
.main-panel {{ border: 3px solid {main_color}; padding: 20px; box-shadow: 0 0 25px {main_color}; background: rgba(0, 0, 0, 0.9); border-radius: 15px; text-align: center; min-width: 350px; {alarm_style} }}
.side-container {{ display: flex; flex-direction: column; gap: 20px; }}
.side-widget {{ border: 1px solid cyan; padding: 15px; box-shadow: 0 0 15px cyan; background: rgba(0, 5, 10, 0.9); border-radius: 10px; min-width: 280px; text-align: center; }}
.btn {{ background: none; border: 1px solid {main_color}; color: {main_color}; padding: 12px; cursor: pointer; font-weight: bold; margin: 5px; width: 100%; text-transform: uppercase; transition: 0.3s; }}
.btn:hover {{ background: {main_color}; color: #000; }}
#particle-stage {{ width: 100%; height: 150px; background: #050505; border: 1px solid #333; border-radius: 5px; margin-top: 10px; }}
@keyframes blink {{ 0% {{ border-color: red; box-shadow: 0 0 40px red; }} 50% {{ border-color: {main_color}; box-shadow: 0 0 10px {main_color}; }} 100% {{ border-color: red; box-shadow: 0 0 40px red; }} }}
</style>
</head>
<body>
<canvas id="matrix-canvas"></canvas>
<div class="wrapper">
    <div class="main-panel">
        <h1>🛡️ J.A.R.V.I.S. CORE</h1>
        <p style="color:cyan; font-size:0.75em;">NETWORK_NODES: ACTIVE | TARGET: HUAWEI</p>
        <hr style="border: 0.5px solid #222;">
        <a href="/run_nmap"><button class="btn">📡 SCAN NETWORK</button></a><br>
        <a href="/run_xray"><button class="btn">🧠 AI-OFFENSIVE SCAN</button></a><br>
        <a href="/toggle_alarm"><button class="btn" style="border-color:red; color:red;">🚨 TOGGLE ALARM</button></a>
    </div>
    <div class="side-container">
        <div class="side-widget" style="border-color: #88ff88;">
            <h3 style="margin:0; font-size:0.7em; color:#88ff88;">TRAFFIC MONITOR:</h3>
            <canvas id="particle-stage"></canvas>
        </div>
        <div class="side-widget">
            <p id="clock" style="font-size:2em; color:cyan; margin:0;">00:00:00</p>
            <p id="full-date" style="font-size:0.8em; color:white; margin:0;">28.02.2026</p>
        </div>
    </div>
</div>
<script>
// --- ЛОГИКА ШАРИКОВ ---
const pCanvas = document.getElementById('particle-stage');
const pCtx = pCanvas.getContext('2d');
pCanvas.width = 280; pCanvas.height = 150;
const particles = [
    {{ x: 50, y: 50, dx: 2.2, dy: 1.8, radius: 12, color: 'cyan', label: '100.1' }},
    {{ x: 150, y: 80, dx: -1.8, dy: 2.1, radius: 15, color: '#00ff41', label: 'HUAWEI' }},
    {{ x: 200, y: 30, dx: 2, dy: -1.5, radius: 10, color: 'yellow', label: 'KALI' }}
];
function animate() {{
    pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);
    particles.forEach(p => {{
        pCtx.beginPath(); pCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        pCtx.fillStyle = p.color; pCtx.shadowBlur = 10; pCtx.shadowColor = p.color; pCtx.fill();
        pCtx.fillStyle = "white"; pCtx.font = "8px Arial"; pCtx.fillText(p.label, p.x - 15, p.y - p.radius - 5);
        if(p.x + p.radius > pCanvas.width || p.x - p.radius < 0) p.dx *= -1;
        if(p.y + p.radius > pCanvas.height || p.y - p.radius < 0) p.dy *= -1;
        p.x += p.dx; p.y += p.dy;
    }});
    requestAnimationFrame(animate);
}}
animate();

// --- МАТРИЦА ---
const mCanvas = document.getElementById('matrix-canvas');
const mCtx = mCanvas.getContext('2d');
mCanvas.width = window.innerWidth; mCanvas.height = window.innerHeight;
const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const drops = []; for (let i = 0; i < mCanvas.width/16; i++) drops[i] = 1;
function drawM() {{
    mCtx.fillStyle = 'rgba(0, 0, 0, 0.05)'; mCtx.fillRect(0, 0, mCanvas.width, mCanvas.height);
    mCtx.fillStyle = '{main_color}'; mCtx.font = '16px arial';
    for (let i = 0; i < drops.length; i++) {{
        mCtx.fillText(letters[Math.floor(Math.random()*letters.length)], i*16, drops[i]*16);
        if (drops[i]*16 > mCanvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    }}
}}
setInterval(drawM, 33);
function updateClock() {{
    document.getElementById('clock').innerText = new Date().toLocaleTimeString();
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
    send_telegram(f"🚨 ALERT: {{'ACTIVATED' if alarm_active else 'DEACTIVATED'}}")
    return """<script>window.location.href='/';</script>"""

@app.route('/run_nmap')
def run_nmap():
    try:
        res = subprocess.check_output(["nmap", "-F", "192.168.100.1"], stderr=subprocess.STDOUT)
        send_telegram("📡 SCAN COMPLETED")
        return f"<body style='background:black;color:#0f0;padding:20px;'><h3>📡 REPORT:</h3><pre>{{res.decode('utf-8')}}</pre><br><a href='/' style='color:yellow;'>НАЗАД</a></body>"
    except Exception as e: return f"<h3>ERROR: {{e}}</h3>"

@app.route('/run_xray')
def run_xray():
    try:
        res = subprocess.check_output(["nmap", "-sV", "192.168.100.1"], stderr=subprocess.STDOUT)
        report = res.decode('utf-8')
        advice = ai_analyze_report(report)
        send_telegram(f"🧠 AI ANALYSIS:\\n{{advice}}")
        return f"<body style='background:black;color:cyan;padding:20px;font-family:monospace;'><h3>🧠 AI ANALYSIS:</h3><pre>{{advice}}</pre><hr><pre>{{report}}</pre><br><a href='/' style='color:yellow;'>НАЗАД</a></body>"
    except Exception as e: return f"<h3>ERROR: {{e}}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
