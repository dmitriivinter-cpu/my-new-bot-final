from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

# Состояние тревоги
alarm_active = False

@app.route('/')
def index():
    main_color = "#ffff00" if alarm_active else "#00ff41"
    status_text = "ALARM SYSTEM ACTIVATED" if alarm_active else "SYSTEM: ONLINE"
    
    html_layout = f"""
    <html>
    <head>
        <title>M.A.R.V.E.L. Command</title>
        <style>
            body {{ background: black; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; }}
            #matrix-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; }}
            .container {{ 
                position: relative; z-index: 1; margin-top: 50px; 
                border: 3px solid {main_color}; padding: 30px; display: inline-block; 
                box-shadow: 0 0 30px {main_color}; background: rgba(0, 0, 0, 0.85); 
                border-radius: 15px; left: 50%; transform: translateX(-50%);
                transition: all 0.5s ease; text-align: center;
            }}
            .btn {{ background: none; border: 1px solid {main_color}; color: {main_color}; padding: 15px 25px; cursor: pointer; font-weight: bold; margin: 10px; text-transform: uppercase; }}
            .btn:hover {{ background: {main_color}; color: #000; box-shadow: 0 0 30px {main_color}; }}
            h1 {{ letter-spacing: 5px; text-shadow: 0 0 15px {main_color}; color: {main_color}; }}
            .log-window {{ background: rgba(10, 10, 10, 0.9); border: 1px solid #333; color: {main_color}; padding: 15px; margin-top: 20px; text-align: left; height: 200px; width: 600px; overflow-y: auto; white-space: pre-wrap; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <canvas id="matrix-canvas"></canvas>
        <div class="container">
            <h1>🛡️ J.A.R.V.I.S. CORE</h1>
            <p style="color:{main_color}; font-weight:bold;">[{status_text}]</p>
            <hr style="border: 0.5px solid #222;">
            
            <a href="/run_nmap"><button class="btn">📡 SCAN NETWORK</button></a>
            <a href="/run_sniffer"><button class="btn">🕵️‍♂️ WEB RECON</button></a>
            <a href="/toggle_alarm"><button class="btn" style="border-color:red; color:red;">🚨 TOGGLE ALARM</button></a>
            <a href="/run_xray"><button class="btn" style="border-color:cyan; color:cyan;">📡 X-RAY SCAN</button></a>

            
            <div class="log-window">> Вход подтвержден... > Все системы активны...</div>
        </div>

        <script>
            const canvas = document.getElementById('matrix-canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            const fontSize = 16;
            const columns = canvas.width / fontSize;
            const drops = [];
            for (let i = 0; i < columns; i++) drops[i] = 1;

            function draw() {{
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '{main_color}';
                ctx.font = fontSize + 'px arial';
                for (let i = 0; i < drops.length; i++) {{
                    const text = letters[Math.floor(Math.random() * letters.length)];
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                    drops[i]++;
                }}
            }}
            setInterval(draw, 33);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_layout)

# --- ЛОГИКА ОЖИВЛЕНИЯ КНОПОК ---

@app.route('/toggle_alarm')
def toggle_alarm():
    global alarm_active
    alarm_active = not alarm_active
    return """<script>window.location.href='/';</script>"""

@app.route('/run_nmap')
def run_nmap():
    try:
        # Используем быстрый скан твоего IP для теста
        res = subprocess.check_output(["nmap", "-F", "192.168.100.1"], stderr=subprocess.STDOUT)
        return f"<body style='background:black;color:#0f0;padding:20px;font-family:monospace;'><h3>📡 ОТЧЕТ СЕТЕВОГО ДОЗОРА:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>НАЗАД В ШТАБ</a></body>"
    except Exception as e:
        return f"<h3>❌ ОШИБКА NMAP:</h3><pre>{e}</pre><br><a href='/'>НАЗАД</a>"

@app.route('/run_sniffer')
def run_sniffer():
    try:
        res = subprocess.check_output(["python3", "form_sniffer.py"], stderr=subprocess.STDOUT)
        return f"<body style='background:black;color:#0f0;padding:20px;font-family:monospace;'><h3>🕵️‍♂️ ОТЧЕТ ВЕБ-РАЗВЕДКИ:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>НАЗАД В ШТАБ</a></body>"
    except Exception as e:
        return f"<h3>❌ ОШИБКА SNIFFER:</h3><pre>{e}</pre><br><a href='/'>НАЗАД</a>"
@app.route('/run_xray')
def run_xray():
    try:
        # X-Ray Scan: Определяем ОС и производителя железа (-O -sV)
        # Внимание: для этого Nmap ТРЕБУЕТ прав администратора (sudo)
        # Но мы попробуем запустить быстрый скан с определением сервисов
        res = subprocess.check_output(["nmap", "-sV", "192.168.100.1"], stderr=subprocess.STDOUT)
        return f"<body style='background:black;color:cyan;padding:20px;font-family:monospace;'><h3>📡 X-RAY REPORT (HARDWARE & SERVICES):</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>НАЗАД В ШТАБ</a></body>"
    except Exception as e:
        return f"<h3>❌ X-RAY ERROR:</h3><p>Для глубокого сканирования ОС нужны права sudo. Ошибка: {e}</p><br><a href='/'>НАЗАД</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
