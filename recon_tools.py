# Модуль RECON_TOOLS v1.0
from datetime import datetime as dt

# Секретные константы
TARGET_VERSION = 2.4
STATUS = "GHOST_MODE_ACTIVE"

def get_time_stamp():
    """Возвращает красивое время для логов"""
    return dt.now().strftime("[%H:%M:%S]")

def scan_log(target, port):
    """Имитация записи сканирования в лог"""
    time = get_time_stamp()
    print(f"{time} 📡 SCANNING: {target} on PORT: {port}...")
