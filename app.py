from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

# Состояние тревоги
alarm_active = False

@app.route('/')
def index():
    main_color = "#ffff00" if alarm_active else "#00ff41"
    status_text = "ALARM SYSTEM ACTIVATED" if alarm_active else "SYSTEM: ONLINE"
    
    # HTML ШАБЛОН (БЕЗ ЛИШНИХ ОТСТУПОВ)
    html_layout = f"""
<html>
<head>
<title>M.A.R.V.E.L. - COMMAND CENTER</title>
<style>
body {{ background: black; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; color: #00ff41; }}
#matrix-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; }}
.wrapper {{ display: flex; justify-content: center; align-items: flex-start; gap: 30px; padding-top: 50px; position: relative; z-index: 1; }}
.main-panel {{ border: 2px solid {main_color}; padding: 25px; box-shadow: 0 0 25px {main_color}; background: rgba(0, 0, 0, 0.85); border-radius: 15px; text-align: center; }}
.side-widget {{ border: 1px solid cyan; padding: 20px; box-shadow: 0 0 15px cyan; background: rgba(0, 0, 10, 0.9); border-radius: 10px; min-width: 220px; text-align: left; }}
.btn {{ background: none; border: 1px solid {main_color}; color: {main_color}; padding: 12px 20px; cursor: pointer; font-weight: bold; transition: 0.3s; margin: 5px; text-transform: uppercase; width: 100%; }}
.btn:hover {{ background: {main_color}; color: #000; box-shadow: 0 0 30px {main_color}; }}
#clock {{ font-size: 2.3em; color: cyan; text-shadow: 0 0 10px cyan; margin: 0; }}
#date-box {{ font-size: 1em; color: white; margin-top: 10px; border-top: 1px solid #333; padding-top: 10px; }}
.day {{ color: yellow; font-weight: bold; }}
</style>
</head>
<body>
<canvas id="matrix-canvas"></canvas>
<div class="wrapper">
<div class="main-panel">
<h1>🛡️ J.A.R.V.I.S. CORE</h1>
<p style="color:cyan; font-size:0.8em;">IP: 192.168.100.141 | MAC: 60:7E:CD:06:86:B3 [HUAWEI]</p>
<hr style="border: 0.5px solid #222;">
<a href="/run_nmap"><button class="btn">📡 SCAN NETWORK</button></a><br>
<a href="/run_sniffer"><button class="btn">🕵️‍♂️ WEB RECON</button></a><br>
<a href="/run_xray"><button class="btn">📡 X-RAY SCAN</button></a><br>
<a href="/toggle_alarm"><button class="btn" style="border-color:red; color:red;">🚨 ALARM SYSTEM</button></a>
</div>
<div class="side-widget">
<h3 style="margin:0; font-size:0.7em; color:cyan;">CHRONOS MODULE:</h3>
<p id="clock">00:00:00</p>
<div id="date-box">
<span id="day-name" class="day">FRIDAY</span><br>
<span id="full-date">27.02.2026</span>
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
const h = String(now.getHours()).padStart(2, '0');
const m = String(now.getMinutes()).padStart(2, '0');
const s = String(now.getSeconds()).padStart(2, '0');
document.getElementById('clock').innerText = h + ":" + m + ":" + s;
const days = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
document.getElementById('day-name').innerText = days[now.getDay()];
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
    return """<script>window.location.href='/';</script>"""

@app.route('/run_nmap')
def run_nmap():
    try:
        res = subprocess.check_output(["nmap", "-F", "192.168.100.1"], stderr=subprocess.STDOUT)
        return f"<body style='background:black;color:#0f0;padding:20px;font-family:monospace;'><h3>📡 SCAN REPORT:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>НАЗАД</a></body>"
    except Exception as e:
        return f"<h3>❌ ERROR:</h3><pre>{e}</pre>"

@app.route('/run_sniffer')
def run_sniffer():
    try:
        res = subprocess.check_output(["python3", "form_sniffer.py"], stderr=subprocess.STDOUT)
        return f"<body style='background:black;color:#0f0;padding:20px;font-family:monospace;'><h3>🕵️‍♂️ RECON REPORT:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>НАЗАД</a></body>"
    except Exception as e:
        return f"<h3>❌ ERROR:</h3><pre>{e}</pre>"

@app.route('/run_xray')
def run_xray():
    try:
        res = subprocess.check_output(["nmap", "-sV", "192.168.100.1"], stderr=subprocess.STDOUT)
        return f"<body style='background:black;color:cyan;padding:20px;font-family:monospace;'><h3>📡 X-RAY REPORT:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>НАЗАД</a></body>"
    except Exception as e:
        return f"<h3>❌ ERROR:</h3><pre>{e}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
