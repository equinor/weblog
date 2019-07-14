import time
import contextlib
import web_log

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ModuleNotFoundError:
    from http.server import BaseHTTPRequestHandler, HTTPServer


try:
    import SocketServer as socketserver
except ModuleNotFoundError:
    import socketserver


web_log.constants.WEBLOG_SERVER = "localhost"
web_log.constants.WEBLOG_PORT = 5254
web_log.constants.WEBLOG_PATH = ""
web_log.constants.WEBLOG_TIMEOUT = 3

OUTPUT = []


class _MockHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        OUTPUT.append(post_data)


def _init_server():
    try:
        OUTPUT.clear()
    except AttributeError:
        del OUTPUT[:]  # Python <3.3

    server = web_log.constants.WEBLOG_SERVER
    port = web_log.constants.WEBLOG_PORT
    return HTTPServer((server, port), _MockHandler)


@contextlib.contextmanager
def serve():
    import threading

    mock = _init_server()
    t = threading.Thread(target=mock.serve_forever)
    t.start()

    try:
        time.sleep(0.5)
        yield
        time.sleep(0.5)
    finally:
        mock.shutdown()

    t.join()
