import socket
import ssl
import json
import select
import logging
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

logging.basicConfig(filename="log.txt", filemode='a', format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)
log = logging.getLogger(__name__)


class Client():
    def __init__(self):
        self.methods = {
            "a": self.chat
        }
        self.curr_id = 0
        self.context = ssl.create_default_context()
        self.hostname = '<my server>'
        self.main()
    def menu(self):
        self.username = self.input_box.text()
        choice = "something i dunno"
        while choice.lower() != "q":
            choice = str(input('''Choose something to do!
            a) Chat with someone random!
            Type the letter of the choice or press q to quit'''))
            try:
                self.methods[choice.lower()]
            except:
                continue
        self.secure_sock.close()

    def genJSONRPC(self, method, params, id):
        return json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": id
        })

    def chat(self):
        self.sock = socket.create_connection((self.hostname, 8080))
        self.secure_sock = self.context.wrap_socket(self.sock, server_hostname=self.hostname)
        self.curr_id += 1
        self.secure_sock.send((genJSONRPC(self, "new_chat", {"username": self.username}, self.curr_id) + "\n").encode("utf-8"))
        self.secure_sock.settimeout(30)
        print("Finding a person to chat with!")
        # assume if the server didn't respond there isn't a chat available
        try:
            response = json.loads(self.secure_sock.recv(4096).decode("utf-8"))
        except:
            print("There's no one to chat with right now :(. Try again later!")
            self.secure_sock.close()
            return
        if response["params"] and response["id"] == self.curr_id:
            print("Say hi to " + response["params"]["username"] + "!")
            print("Type in anything and send it to " + response["params"]["username"] + " or press q to quit.")
        message = ""
        cached_message = ""
        while message != "q":
            print("ak")

    def main(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setGeometry(20,20,500,800) # sets the windows x, y, width, height
        self.window.setWindowTitle("Random Chat") # setting the window title
        self.input_box = QLineEdit()
        self.input_box.setMaxLength(20)
        self.input_box.setAlignment(Qt.AlignRight)
        self.input_box.setFont(QFont("resources/Modenine-2OPd.ttf",20))
        self.input_box.editingFinished.connect(self.menu)

        flo = QFormLayout()
        flo.addRow("Enter your username", self.input_box)
        self.window.setLayout(flo)
        self.window.show()
        #QLineEdit('Enter the username you want to use! Length must be less than 20. ')
        sys.exit(self.app.exec_())


Client()