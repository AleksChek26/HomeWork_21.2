import http.server
import socketserver
import os

PORT = 8000


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Если запрос к статическим файлам (CSS/JS)
        if self.path.startswith('/static/'):
            try:
                # Формируем полный путь к файлу
                file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))

                with open(file_path, 'rb') as f:
                    content = f.read()

                # Определяем Content-Type
                if self.path.endswith('.css'):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                elif self.path.endswith('.js'):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/javascript')
                else:
                    self.send_response(404)
                    return

                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "File not found")
            return

        # Для всех остальных запросов отдаём contacts.html
        try:
            with open('contacts.html', 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "contacts.html not found")


# Запускаем сервер
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Сервер запущен на http://localhost:{PORT}")
    httpd.serve_forever()