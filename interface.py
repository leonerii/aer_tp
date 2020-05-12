from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
import json
import time


class GUI():
    def __init__(self):
        
        self.window_ask = Tk()
        self.window_ask.title("Choose a option")
        self.window_ask.geometry('280x110')

        def get():
            #pass
            mensagens = [
                {
                "Type":"Client_msg",
                "Road":"104",
                "Reference":"perto da UM",
                "Message":"acidente"
                },
                {
                "Type":"Client_msg",
                "Road":"104",
                "Reference":"perto da UM",
                "Message":"acidente"
                }]
            
            mensg = json.dumps(mensagens)
            mensg = json.loads(mensg)
            print (mensg[0]["Road"])
            self.window_get = Tk()
            self.window_get.title("Consulta")
            self.window_get.geometry('350x210')
            lbl1 = Label(self.window_get, text="Road: ")
            result1 = Label(self.window_get, text=mensg[0]["Road"])
            lbl2 = Label(self.window_get, text="Referência: ")
            result2 = Label(self.window_get, text=mensg[0]["Reference"])
            lbl3 = Label(self.window_get, text="Message: 4")
            result3 = Label(self.window_get, text=mensg[0]["Message"])

            lbl1.grid(column=0, row=0)
            result1.grid(column=1, row=0)
            lbl2.grid(column=0, row=1)
            result2.grid(column=1, row=1)
            lbl3.grid(column=0, row=2)
            result3.grid(column=1, row=2)


        def open_win_post():
            self.window_ask.destroy()
            
            self.window_post = Tk()
            self.window_post.title("Message")
            self.window_post.geometry('300x230')

            self.combo = Combobox(self.window_post)

            lbl1 = Label(self.window_post, text="Road: ")
            lbl2 = Label(self.window_post, text="Reference: ")
            lbl3 = Label(self.window_post, text="Message: ")
            self.combo['values'] = ('A11', 'N14', 'N101', 'N102', 'N103', 'N104')

            lbl1.grid(column=0, row=0)
            lbl2.grid(column=0, row=1)
            lbl3.grid(column=0, row=2)

            self.rod = self.combo.grid(column=2, row=0)
            self.ref = scrolledtext.ScrolledText(self.window_post,width=20,height=3)
            self.msg = scrolledtext.ScrolledText(self.window_post,width=20,height=5)

            self.ref.grid(column=2, row=1)
            self.msg.grid(column=2, row=2)

            self.combo.current() #set the selected item 
            btn_send = Button(self.window_post, text="Post a message", command=post)
            btn_send.grid(column=2, row=5)

            self.window_post.mainloop() 

        def post():
            print(self.combo.get())
            print(self.ref.get(1.0, END))
            print(self.msg.get(1.0, END))
            
            mensagem = {
                "type":"POST",
                "road":self.combo.get(),
                "reference":self.ref.get(1.0, END),
                "message":self.msg.get(1.0, END),
                "timestamp":time.time()
            }
            print(mensagem)
            print("aqui")

            self.win_close = Tk()
            self.win_close.title("")
            self.win_close.geometry('280x110')

            lbl1 = Label(self.win_close, text="Your message was sent")
            btn_close = Button(self.win_close, text="Close", command=close)
            btn_close.grid(column=2, row=2)
   
        def close():
            self.window_post.destroy()
            self.win_close.destroy()
        
           
        btn_1 = Button(self.window_ask, text="Post a Message", command=open_win_post)
        btn_1.grid(column=0, row=5)
        btn_2 = Button(self.window_ask, text="Get Notifications", command=get)
        btn_2.grid(column=4, row=5)

        #btn_ask = Button(self.window_ask, text="Consultar", command=win_check)
        #btn_check = Button(self.window_get, text="Enviar Mensagem", command=check)
        


        self.window_ask.mainloop() 
        
        #self.window_post.mainloop() 

def main():
    gui = GUI()
    

if __name__ == '__main__':
    main()

