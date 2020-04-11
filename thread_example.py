from threading import Thread, RLock

"""
As classes que irão "virar" threads devem no mínimo receber a tabela de
roteamente e um objeto lock como argumento.
Esses dois objetos serão criado no código do Igor.
"""


class MyThread(Thread):
    def __init__(self, route_table, lock):

        Thread.__init__(self)
        self.route_table = route_table
        self.lock = lock

    """
    Essa função vai ser executada quando a thread for iniciada,
    toda a logica da thread deve ficar dentro desta função.
    
    Claro, podemos fazer função adicionais para usar dentro desta.
    """
    def run(self):
        try:
            """
            Execução bloqueia até a thread conseguir adquirir o lock.
            Depois de adquirido só esta thread poderá acessar a tabela de rotas.

            É boa prática ficar o menor tempo possível segurando o lock,
            então se tiver outras coisas pra fazer que não precise da tabela de
            rotas faça antes de adquirir o lock.
            """
            self.lock.acquire()

            """
            Fazer aqui o que tiver que fazer
            """

        except Exception as e:
            """
            Tratar os erros
            """
            pass

        finally:
            """
            Por último tem que soltar o lock para outras threads poderem usar a
            tabela de rotas.
            Ao colocar isto no bloco finally garante que mesmo que aconteça
            algum erro durante a execução da thread o lock seja solto.
            """
            self.lock.release()

    
    def aux_func1(self):
        pass

    def aux_func2(self):
        pass
