import socket
import ssl
import json
import select
import logging
import pygame
from pygame.locals import *

logging.basicConfig(filename="log.txt", filemode='a', format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)
log = logging.getLogger(__name__)


class Client:
    def __init__(self):
        self.methods = {
            "a": self.chat
        }
        self.curr_id = 0
        self.context = ssl.create_default_context()
        self.hostname = '<my server>'
        self.main()
    def menu(self):
        input_box = pygame.Rect(100, 400, 140, 32)
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
        pygame.init()
        self.screen = pygame.display.set_mode( (1000,1000) )
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Random Chat')
        favicon = pygame.image.load('resources/favicon.png')
        pygame.display.set_icon(favicon)
        self.font = pygame.font.Font('resources/Modenine-2OPd.ttf', 16)
        self.screen.fill((0, 0, 0))

        username = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        prompt = self.font.render('Enter the username you want to use! Length must be less than 20. ', False, (255, 255, 255))
        input_box = pygame.Rect(100, 100, 140, 32)
        while len(username) > 20:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.screen.blit(favicon, (200,100))

            self.screen.fill((0, 0, 0))
            self.screen.blit(prompt, (0, 500))
            pygame.display.update()  # Or pygame.display.flip()
            
            #username = str(input("Enter the username you want to use! Length must be less than 20. "))
        #self.menu()
Client()