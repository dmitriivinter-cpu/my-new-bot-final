import requests
from bs4 import BeautifulSoup

def get_links(url):
    print(f"🕵️‍♂️ Начинаю разведку на {url}...")
    try:
        # 1. Загружаем страницу
        response = requests.get(url, timeout=5)
        # 2. Превращаем её в понятный Python'у объект
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Ищем все теги <a> (ссылки)
        links = soup.find_all('a')
        
        print(f"✅ Найдено ссылок: {len(links)}")
        for link in links[:10]: # Покажем первые 10
            href = link.get('href')
            if href:
                print(f"🔗 Ссылка: {href}")
                
    except Exception as e:
        print(f"❌ Ошибка связи: {e}")

if __name__ == "__main__":
    target = "https://www.kali.org"
    get_links(target)
