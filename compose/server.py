import sys
import os

# 动态将上一层目录（根目录）加入到包搜索路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from http.server import HTTPServer, SimpleHTTPRequestHandler
from api.steps import handler as ApiStepsHandler

class RouterHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        if self.path.startswith('/api/steps'):
            ApiStepsHandler.do_OPTIONS(self)
        else:
            super().do_OPTIONS()

    def do_POST(self):
        if self.path.startswith('/api/steps'):
            ApiStepsHandler.do_POST(self)
        else:
            self.send_error(405, "Method Not Allowed")

    # Inherit the custom method so that ApiStepsHandler.do_POST(self) can use it
    send_json_response = ApiStepsHandler.send_json_response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 11400))
    server = HTTPServer(('0.0.0.0', port), RouterHandler)
    print(f"Starting server on port {port}")
    server.serve_forever()
