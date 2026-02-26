import requests
from bs4 import BeautifulSoup

def analyze_form(url):
    # 1. НАША МАСКА (User-Agent)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','X-Forwarded-For': '8.8.8.8'
    }
    
    print(f"📡 Сканирую формы на: {url} (Маскировка Chrome ВКЛ)")
    
    try:
        # 2. ЗАПРОС С МАСКОЙ
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        forms = soup.find_all('form')
        
        print(f"✅ Найдено форм: {len(forms)}")
        
        for i, form in enumerate(forms, 1):
            action = form.get('action')
            method = form.get('method', 'post')
            print(f"\n📦 ФОРМА №{i}:")
            print(f"🔗 Куда летят данные (Action): {action}")
            print(f"📩 Метод (Method): {method.upper()}")
            
            for inp in form.find_all('input'):
                name = inp.get('name')
                type = inp.get('type', 'text')
                print(f"   🔑 Поле: [{name}] | Тип: {type}")
                
    except Exception as e:
        print(f"❌ Ошибка связи: {e}")

if __name__ == "__main__":
    target = "http://testphp.vulnweb.com"
    analyze_form(target)
