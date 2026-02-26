from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    html_layout = """
    <html>
    <head>
        <title>M.A.R.V.E.L. - MATRIX EDITION</title>
        <style>
            body { background: black; margin: 0; overflow: hidden; font-family: 'Courier New', monospace; }
            #matrix-canvas { position: fixed; top: 0; left: 0; z-index: -1; }
            .container { 
                position: relative; z-index: 1; margin-top: 50px; 
                border: 2px solid #00ff41; padding: 30px; display: inline-block; 
                box-shadow: 0 0 25px #00ff41; background: rgba(0, 0, 0, 0.85); 
                border-radius: 15px; left: 50%; transform: translateX(-50%);
            }
            .btn { background: none; border: 1px solid #00ff41; color: #00ff41; padding: 15px 25px; cursor: pointer; font-weight: bold; transition: 0.3s; margin: 10px; text-transform: uppercase; }
            .btn:hover { background: #00ff41; color: #000; box-shadow: 0 0 30px #00ff41; }
            .log-window { background: rgba(10, 10, 10, 0.9); border: 1px solid #333; color: #0f0; padding: 20px; margin-top: 20px; text-align: left; height: 350px; width: 600px; overflow-y: auto; white-space: pre-wrap; font-size: 0.9em; border-radius: 5px; }
            h1 { letter-spacing: 5px; text-shadow: 0 0 15px #00ff41; color: #00ff41; }
        </style>
    </head>
    <body>
        <canvas id="matrix-canvas"></canvas>
        <div class="container">
            <h1>🛡️ J.A.R.V.I.S. CORE</h1>
            <p style="color:yellow;">[ SYSTEM: ONLINE | AUTHENTICATED ]</p>
            <hr style="border: 0.5px solid #222;">
            <a href="/run_nmap"><button class="btn">📡 СКАН СЕТИ (МАСКИРОВКА ВКЛ)</button></a>
            <a href="/run_sniffer"><button class="btn">🕵️‍♂️ WEB RECON</button></a>
            <div class="log-window">> Вход в систему подтвержден... > Загрузка протоколов Matrix... > Ожидаю ввода, Сэр.</div>
        </div>

        <script>
            const canvas = document.getElementById('matrix-canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()*&^%';
            const fontSize = 16;
            const columns = canvas.width / fontSize;
            const drops = [];
            for (let i = 0; i < columns; i++) drops[i] = 1;

            function draw() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#0F0';
                ctx.font = fontSize + 'px arial';
                for (let i = 0; i < drops.length; i++) {
                    const text = letters[Math.floor(Math.random() * letters.length)];
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                    drops[i]++;
                }
            }
            setInterval(draw, 33);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_layout)

@app.route('/run_nmap')
def run_nmap():
    res = subprocess.check_output(["nmap", "-F", "192.168.100.141"], stderr=subprocess.STDOUT)
    return f"<body style='background:black;color:#0f0;font-family:monospace;padding:20px;'><h3>📡 SCAN REPORT:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>[ BACK TO CORE ]</a></body>"

@app.route('/run_sniffer')
def run_sniffer():
    res = subprocess.check_output(["python3", "form_sniffer.py"], stderr=subprocess.STDOUT)
    return f"<body style='background:black;color:#0f0;font-family:monospace;padding:20px;'><h3>🕵️‍♂️ WEB RECON REPORT:</h3><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>[ BACK TO CORE ]</a></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

