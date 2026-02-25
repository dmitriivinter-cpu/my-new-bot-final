import requests
from bs4 import BeautifulSoup

def analyze_form(url):
    print(f"📡 Сканирую формы на: {url}")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    forms = soup.find_all('form')
    
    for i, form in enumerate(forms, 1):
        action = form.get('action')
        method = form.get('method', 'post')
        print(f"\n📦 ФОРМА №{i} (Цель найдена!):")
        print(f"🔗 Куда летят данные (Action): {action}")
        print(f"📩 Метод (Method): {method.upper()}")
        
        for inp in form.find_all('input'):
            name = inp.get('name')
            type = inp.get('type', 'text')
            print(f"   🔑 Поле: [{name}] | Тип: {type}")

if __name__ == "__main__":
    # Наш учебный полигон
    target = "http://testphp.vulnweb.com"
    analyze_form(target)
