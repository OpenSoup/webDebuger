from socket import *
from threading import *


def chat(conn: socket):
    global stop
    stop = False

    def repeat_send_message():
        global stop
        while True:
            message = input()
            if message == '':
                stop = True
                conn.close()
                break
            conn.send(eval(f"b'{message}'"))
    repeat_send_message_t = Thread(target=repeat_send_message)
    repeat_send_message_t.start()
    while True:
        try:
            recv = conn.recv(2048)
            if recv == b'' or stop:
                print("Connect closed. If the program do not close, press enter")
                break
            print(recv)
        except BlockingIOError as BIOE:
            repr(BIOE)
        except BaseException as BE:
            print(f'failed because: {repr(BE)}')
            break


if __name__ == '__main__':
    l_or_c = None
    while l_or_c not in ['l', 'c']:
        l_or_c = input('listen(l) or connect(c):')
    if l_or_c == 'l':
        ip, port = input('ip:'), int(input('port:'))
        server = socket(AF_INET, SOCK_STREAM)
        server.setblocking(True)
        server.bind((ip, port))
        print('listening connection...')
        server.listen(5)
        conn, addr = server.accept()
        conn.setblocking(False)
        print('connect success!')
        chat(conn)
    else:
        conn = socket()
        ip, port = input('ip:'), int(input('port:'))
        print()
        try:
            conn.connect((ip, port))
            conn.setblocking(False)
            print('connect success!')
            chat(conn)
        except BaseException as BE:
            print(f'failed because: {repr(BE)}')
