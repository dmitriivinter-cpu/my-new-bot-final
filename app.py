from flask import Flask, render_template, request
import subprocess
import requests
import recon_tools  # Наш новый боевой модуль

app = Flask(__name__)

# --- [ КОНФИГУРАЦИЯ J.A.R.V.I.S. ] ---
TOKEN = "8509780467:AAHBc_IkTBKWOHGPaVJnM00rnl57MiBEhfs"
CHAT_ID = "1421473166"

alarm_active = False

def send_telegram(text):
    try:
        url = f"https://api.telegram.org{TOKEN}/sendMessage"
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
    analysis += "🛠️ ADVICE: Смените пароль админа и проверьте Firewall."
    return analysis

# --- [ ГЛАВНЫЙ ВХОД (УРОВЕНЬ 1: ТЕСТЕР) ] ---
@app.route('/')
def index():
    # Логируем вход через наш модуль Mark-22
    print(f"📡 JARVIS ALERT: {recon_tools.get_time_stamp()} | STATUS: {recon_tools.STATUS}")
    # Flask сам возьмет файл templates/index.html
    return render_template('index.html')

@app.route('/toggle_alarm')
def toggle_alarm():
    global alarm_active
    alarm_active = not alarm_active
    send_telegram(f"🚨 ALERT: {'ACTIVATED' if alarm_active else 'DEACTIVATED'}")
    return """<script>window.location.href='/';</script>"""

@app.route('/run_nmap')
def run_nmap():
    try:
        res = subprocess.check_output(["nmap", "-F", "192.168.100.1"], stderr=subprocess.STDOUT)
        send_telegram("📡 SCAN COMPLETED")
        return f"<body style='background:black;color:#0f0;padding:20px;'><pre>{res.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>НАЗАД</a></body>"
    except Exception as e: return f"<h3>ERROR: {e}</h3>"

@app.route('/run_xray')
def run_xray():
    try:
        res = subprocess.check_output(["nmap", "-sV", "192.168.100.1"], stderr=subprocess.STDOUT)
        report = res.decode('utf-8')
        advice = ai_analyze_report(report)
        send_telegram(f"🧠 AI ANALYSIS:\n{advice}")
        return f"<body style='background:black;color:cyan;padding:20px;'><h3>🧠 AI ANALYSIS:</h3><pre>{advice}</pre><hr><pre>{report}</pre><br><a href='/' style='color:yellow;'>НАЗАД</a></body>"
    except Exception as e: return f"<h3>ERROR: {e}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
