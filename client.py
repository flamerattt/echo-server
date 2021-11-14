import socket


def sendSocket(conn, strMessage):
    bytes = strMessage.encode()

    if len(bytes) == 0:
        return False
    lenMsg = len(bytes)
    sendBytes = []
    sendBytes.append(lenMsg // 256)
    sendBytes.append(lenMsg % 256)
    for it in bytes:
        sendBytes.append(it)
    conn.send(bytearray(sendBytes))
    return True


def recvSocket(conn):
    data = conn.recv(1024)
    if not data:
        return None
    length = data[0] * 256 + data[1]
    bytes = []
    for i in range(2, len(data)):
        bytes.append(data[i])
    return bytearray(bytes).decode()


print('Input port number:')
port = int(input())

print('Input host name (Enter = localhost):')
host = input()
if not host:
    host = 'localhost'
add = (host, port)

sock = socket.socket()

try:
    sock.connect(add)
except BaseException:
    print(f"Error {host}:{port}")
    exit(1)

print('Соединение с сервером', add)

data_dec = recvSocket(sock)

print(data_dec)

while True:
    while True:
        msg = ""
        inp = ""
        while True:
            inp = input()
            if inp == "send":
                msg = msg[0:-1]
                break
            msg += inp + "\n"

        if sendSocket(sock, msg):
            break
        else:
            print("Repeat input data:")

    if msg == 'exit':
        break


    print(f'Отправка данных {msg} серверу', add)
    data_dec = recvSocket(sock)
    print(f'Прием данных {data_dec} от сервера', add)
    print(data_dec)

sock.close()
print('Разрыв соединения с сервером', add)
