from threading import Thread
from ndn_receive_handler import Receive_Handler

class NDN_Server(Thread):
    def __init__(self, localhost, port=9999, data_ids={}):
        Thread.__init__(self)
        self.localhost = localhost
        self.port = port
        self.data_ids = data_ids


    def run(self):
        #inicializar pit, fib e cs
        if
        #criar socket server tcp

        #ficar escutando por novas mensagens

        #pra cada mensagem recebida, iniciar a thread ndn_handler com a mensagem
        ndn_handler = Receive_Handler(
            
        )
        pass