import json
import urllib.request
from http.server import BaseHTTPRequestHandler

# Ваш токен бота
BOT_TOKEN = "8872260684:AAHU65LnhHmLAItW3J6ECA-l9RyAOaSwAy8"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Читаем данные, полученные от Mini App
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = json.loads(self.rfile.read(content_length)) if content_length > 0 else {}
            stars = int(post_data.get('stars', 5))

            # Отправляем запрос к Telegram API для создания ссылки на счет в звездах
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/createInvoiceLink"
            payload = json.dumps({
                "title": "Попытка в рулетке",
                "description": f"Вращение рулетки за {stars} зв.",
                "payload": f"spin_{stars}_stars",
                "provider_token": "",  # Для XTR (Telegram Stars) обязательно пустая строка!
                "currency": "XTR",
                "prices": [{"label": "Звезды", "amount": stars}]
            }).encode('utf-8')

            req = urllib.request.Request(
                url, 
                data=payload, 
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                invoice_url = result.get('result', '')

                # Отправляем ссылку на счет обратно на веб-сайт
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'invoice_url': invoice_url}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

    # Обработка предварительных CORS-запросов от браузера
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
