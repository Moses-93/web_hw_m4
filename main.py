import socket
import json
import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from datetime import datetime
from threading import Thread

class HttpHandler(BaseHTTPRequestHandler):
    """
    A custom HTTP request handler for handling HTTP requests.

    Attributes:
    - self.rfile: A file-like object for reading request data.
    - self.wfile: A file-like object for writing response data.
    - self.headers: A dictionary-like object containing request headers.
    - self.path: The requested path.
    """

    def do_POST(self):
        """
        Handles POST requests.

        Reads the request data, connects to a socket server and sends the data.
        """
        data = self.rfile.read(int(self.headers['Content-Length']))
        soc_client = socket.socket()
        soc_client.connect(("0.0.0.0", 3000))
        soc_client.sendall(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        """
        Handles GET requests.

        Parses the requested path, serves static files or HTML templates based on the path.
        """
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('front-init/index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('front-init/message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('front-init/error.html', 404)

    def send_html_file(self, filename, status=200):
        """
        Sends an HTML file as a response.

        Args:
        - filename: The name of the HTML file to send.
        - status: The HTTP status code for the response (default is 200).
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        """
        Sends a static file as a response.

        Determines the content type based on the file extension and sends the file.
        """
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    """
    Runs the HTTP server.

    Args:
    - server_class: The class for the HTTP server (default is HTTPServer).
    - handler_class: The class for the HTTP request handler (default is HttpHandler).
    """
    server_address = ('0.0.0.0', 5000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


HOST = ("0.0.0.0", 3000)

def socket_server():
    """
    Runs a socket server that listens for incoming connections and processes data.

    Creates a socket object, binds it to the specified host and port, listens for incoming connections,
    receives data, parses it, and stores it in a JSON file.
    """
    # Create a socket object 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(HOST)
    server_socket.listen(1)

    while True:
        client_soc, client_adrs = server_socket.accept()
        data = client_soc.recv(1024)
        print(f"Отримано запит: {client_adrs}")
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)

        file_path = pathlib.Path("front-init/storage/data.json")
        if not file_path.is_file():
            with open(file_path, "w") as file:
                json.dump({}, file, indent=2)
        
        with open(file_path, "r") as file:
            new_data = json.load(file)
        
        timeshtamp = datetime.now().isoformat()

        new_data[timeshtamp] = data_dict
        with open(file_path, "w") as file:
            json.dump(new_data, file, indent=2)
        client_soc.close()
        
        
def main():
    server = Thread(target=run)
    my_socket = Thread(target=socket_server)
    my_socket.start()
    server.start()
    print("Server started...")


if __name__ == "__main__":
    main()
    

    
    