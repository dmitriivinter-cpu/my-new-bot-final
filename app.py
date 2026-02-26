from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

# ГЛАВНЫЙ ИНТЕРФЕЙС
@app.route('/')
def index():
    html_layout = """
    <body style="background:#050505; color:#00ff41; font-family:monospace; text-align:center; padding:50px;">
        <h1 style="border:2px solid #00ff41; padding:20px; display:inline-block;">🛡️ PROJECT M.A.R.V.E.L. - DASHBOARD</h1>
        <hr style="border:0.5px solid #333; margin:30px;">
        <div style="display:flex; justify-content:center; gap:30px;">
            <form action="/run_sniffer">
                <button style="background:none; border:1px solid #00ff41; color:#00ff41; padding:15px; cursor:pointer; font-weight:bold;">📡 АНАЛИЗ ВЕБ-ФОРМ</button>
            </form>
        </div>
        <p style="margin-top:50px; color:#555;">Система готова к командам, Сэр.</p>
    </body>
    """    
    return render_template_string(html_layout)

# ЛОГИКА КНОПКИ "АНАЛИЗ ФОРМ"
@app.route('/run_sniffer')
def run_sniffer():
    try:
        # Запускаем ваш скрипт шпиона и получаем текст отчета
        result = subprocess.check_output(["python3", "form_sniffer.py"], stderr=subprocess.STDOUT)
        # Показываем результат прямо в браузере
        return f"<h1>📝 ОТЧЕТ РАЗВЕДКИ:</h1><pre style='background:#111; color:#0f0; padding:20px;'>{result.decode('utf-8')}</pre><br><a href='/' style='color:yellow;'>Вернуться в штаб</a>"
    except Exception as e:
        return f"<h1>❌ ОШИБКА ЗАПУСКА:</h1><pre>{e}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
