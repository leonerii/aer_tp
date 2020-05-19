from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
import json
import time
import socket
import send_tcp

class Interface:

    def __init__(self):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.localhost = '127.0.0.1'
        self.port = 9999

    def ask(self):
        # Tela inicial da interface
        self.win_ask = Tk()

        btn_post = Button(self.win_ask, text='Post a message', command=self.post)
        btn_get = Button(self.win_ask, text='Get messages', command=self.get)

        btn_post.grid()
        btn_get.grid()

        self.win_ask.mainloop()

    def post(self):
        self.win_post = Tk()

        self.combo = Combobox(self.win_post)
        self.combo['values'] = ('A11', 'N14', 'N101', 'N102', 'N103', 'N104')

        lbl1 = Label(self.win_post, text="Road: ").grid(column=0, row=0)
        lbl2 = Label(self.win_post, text="Reference: ").grid(column=0, row=1)
        lbl3 = Label(self.win_post, text="Message: ").grid(column=0, row=2)


        self.rod = self.combo.grid(column=1, row=0)
        self.ref = scrolledtext.ScrolledText(self.win_post,width=20,height=3)#.grid(column=1, row=1)
        self.msg = scrolledtext.ScrolledText(self.win_post,width=20,height=5)#.grid(column=1, row=2)

        self.ref.grid(column=1, row=1)
        self.msg.grid(column=1, row=2)

        self.combo.current()
        btn_post = Button(self.win_post, text='Post a message', command=self.socket_post)
        btn_close = Button(self.win_post, text='Close', command=self.win_post.destroy)
        
        btn_post.grid(column=0, row=3)
        btn_close.grid(column=1, row=3)

        self.win_post.mainloop()

    def socket_post(self):
        dest = '8.8.8.8'
        print(self.combo.get())
        print(self.ref.get(1.0, END))
        print(self.msg.get(1.0, END))

        msg = {
            "road":self.combo.get(),
            "reference":self.ref.get(1.0, END),
            "message":self.msg.get(1.0, END),
            'timestamp':time.time()
        }

        data = {
            'type':'POST',
            'source': self.localhost,
            'dest': dest, 
            'interface': msg,
            'timestamp':time.time()
        }
        print(data)

        self.post_msg = data

        send_tcp.send_message(data)

        """self.socket.connect((self.localhost, self.port))
        self.socket.sendall(self.data.encode("utf-8"))

        received_msg = self.socket.recvfrom(4096)
        print('Preparing to receive back')
        response = received_msg[0].decode()
        print(f'Message Received: {response}')
        """

    def get(self):
        self.win_get = Tk()

        self.combo_get = Combobox(self.win_get)
        self.combo_get['values'] = ('A11', 'N14', 'N101', 'N102', 'N103', 'N104')

        lbl1 = Label(self.win_get, text="Road: ").grid(column=0, row=0)

        self.rod = self.combo_get.grid(column=1, row=0)
        self.combo_get.current()
        
        btn_get = Button(self.win_get, text='Get a message', command=self.socket_get)
        btn_close = Button(self.win_get, text='Close', command=self.win_get.destroy)
        
        btn_get.grid(column=0, row=3)
        btn_close.grid(column=1, row=3)

        self.win_get.mainloop()

    def socket_get(self):
        print(self.combo_get.get())
        x = self.combo_get.get()

        for keys in list(self.post_msg.items()):
            if keys == 'interface':
                for x in keys:
                    print (x)


        #print(self.post_msg['interface']['road' == x])

        # Recebe mensagens e atribui a variável 'data'
        """
        data = {
            'type':'GET',
            'source': 'IP_server',
            'dest': dest, 
            'interface': {
                msg1,
                msg2,
                msg3,
            }
            'timestamp':time.time()
        }
        """
        """
        self.socket.connect((self.localhost, self.port))
        self.socket.sendall(self.data.encode("utf-8"))

        received_msg = self.socket.recvfrom(4096)
        print('Preparing to receive back')
        response = received_msg[0].decode()
        print(f'Message Received: {response}')
        """


def main():
    interf = Interface()
        
    interf.ask()

if __name__ == '__main__':
    main()

