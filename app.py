import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs


def resource_path(relative_path):
    """
    개발 환경과 PyInstaller exe 실행 환경 모두에서
    리소스 파일 경로를 올바르게 찾기 위한 함수
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def calculate(num1, operator, num2):
    num1 = float(num1)
    num2 = float(num2)

    if operator == "+":
        return str(num1 + num2)
    elif operator == "-":
        return str(num1 - num2)
    elif operator == "*":
        return str(num1 * num2)
    elif operator == "/":
        if num2 == 0:
            return "0으로 나눌 수 없습니다."
        return str(num1 / num2)
    else:
        return "지원하지 않는 연산자입니다."


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.render_page("계산 결과가 여기에 표시됩니다.")
        else:
            self.send_error(404, "페이지를 찾을 수 없습니다.")

    def do_POST(self):
        if self.path == "/calculate":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            form_data = parse_qs(post_data)

            num1 = form_data.get("num1", ["0"])[0]
            operator = form_data.get("operator", ["+"])[0]
            num2 = form_data.get("num2", ["0"])[0]

            try:
                result = calculate(num1, operator, num2)
            except ValueError:
                result = "숫자를 올바르게 입력하세요."

            self.render_page(result)
        else:
            self.send_error(404, "페이지를 찾을 수 없습니다.")

    def render_page(self, result):
        with open(resource_path("index.html"), "r", encoding="utf-8") as file:
            html = file.read()

        html = html.replace("{{ result }}", result)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


def run_server():
    server_address = ("localhost", 8000)
    httpd = HTTPServer(server_address, CalculatorHandler)

    print("로컬 서버가 실행되었습니다.")
    print("접속 주소: http://localhost:8000")

    httpd.serve_forever()


if __name__ == "__main__":
    run_server()