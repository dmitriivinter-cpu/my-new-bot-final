import nmap
import time
import subprocess
import os
from scapy.all import ARP, Ether, srp, conf
import telebot
from gtts import gTTS

# --- НАСТРОЙКИ ---
TOKEN = '8509780467:AAEUm13wvtANYCAxzIxR_9OpRBPRMz4Mm50'
CHAT_ID = '1421473166'
bot = telebot.TeleBot(TOKEN)

# ТВОЙ ИМЕННОЙ СПИСОК (уже с новыми адресами)
DEVICES = {
    "60:7e:cd:06:86:b3": "🏠 Роутер",
    "70:08:94:dc:4f:0d": "📱 Телефон Дмитро",
    "72:17:d2:6d:36:b1": "📱 Смартфон (Гость 1)",
    "4e:91:c8:d2:26:2a": "📱 Смартфон (Гость 2)"
}

conf.iface = "eth0"
last_seen = set()

def get_scan():
    try:
        subprocess.run(["fping", "-g", "192.168.100.0/24", "-a", "-r", "0"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        arp = ARP(pdst="192.168.100.0/24")
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        answered, unanswered = srp(packet, timeout=3, verbose=False, retry=1)
        return {received.hwsrc for sent, received in answered}
    except:
        return set()

def send_voice(text):
    try:
        tts = gTTS(text=text, lang='ru')
        tts.save("alert.ogg")
        with open("alert.ogg", "rb") as voice:
            bot.send_voice(CHAT_ID, voice)
        os.remove("alert.ogg")
    except:
        pass
def scan_ports(ip):
    nm = nmap.PortScanner()
    print(f"🔎 Сканирую порты для {ip}...")
    # Сканируем самые популярные порты (1-1024)
    nm.scan(ip, '1-1024')
    
    report = f"📋 Отчет по портам [{ip}]:\n"
    for proto in nm[ip].all_protocols():
        lport = nm[ip][proto].keys()
        for port in lport:
            state = nm[ip][proto][port]['state']
            report += f"🚪 Порт {port}: {state}\n"
    return report

def monitor():
    global last_seen
    print("📢 Голосовой Охранник 2.0 запущен...")
    last_seen = get_scan()
    bot.send_message(CHAT_ID, f"📢 Система Голос ВКЛ. В сети: {len(last_seen)}")

    while True:
        try:
            time.sleep(30) # Увеличили до 30 сек, чтобы не частил
            current_scan = get_scan()
            
            # КТО ПРИШЕЛ
            for mac in (current_scan - last_seen):
                name = DEVICES.get(mac, f"Неизвестный")
                ip = "192.168.100.XXX" # Сюда мы добавим поиск IP по MAC ниже
                
                msg = f"🟢 В СЕТИ: {name}\n📍 MAC: {mac}"
                bot.send_message(CHAT_ID, msg)
                
                # --- НОВЫЙ БЛОК: СКАН ПОРТОВ ---
                # Мы вызываем функцию, которую ты вставил раньше
                try:
                    # Для теста возьмем твой роутер или телефон
                    port_report = scan_ports("192.168.100.1") 
                    bot.send_message(CHAT_ID, port_report)
                except Exception as e:
                    print(f"❌ Ошибка скана портов: {e}")
            
            # КТО УШЕЛ
            for mac in (last_seen - current_scan):
                name = DEVICES.get(mac, f"Неизвестный")
                msg = f"Устройство {name} покинуло сеть"
                bot.send_message(CHAT_ID, f"🔴 {msg}")
                send_voice(msg)

            last_seen = current_scan
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    monitor()
