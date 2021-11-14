import socket
import hashlib


def getUser(ip):
    my_file = open("list_ip.txt", "r")
    for line in my_file:
        ip_name = line.split()
        if ip == ip_name[0]:
            return ip_name[1]
    return ''


def writeLogs(write_log):
    log_file = open("list_logs.txt", "a")
    log_file.write(f'{write_log}\n')
    log_file.close()


def getPass(ip):
    my_file = open("list_ip.txt", "r")
    for line in my_file:
        ip_name = line.split()
        if ip == ip_name[0]:
            return ip_name[2]
    return ''


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

add = ('localhost', port)

sock = socket.socket()

try:
    sock.bind(add)
except OSError:
    for anyPort in range(1024, 65536):
        try:
            add = ('localhost', anyPort)
            sock.bind(add)
            break
        except OSError:
            pass

writeLogs(f'Запуск сервера, {add}')
print(f"Connection is established, port: {add[1]}")

sock.listen()

writeLogs(f'Начало прослушивания порта {add[1]}')


isDisconnect = True
while True:
    if isDisconnect:
        conn, addr = sock.accept()
        isDisconnect = False
        writeLogs(f'Подключение клиента {addr}')
        noNameForNewUser = False
        noPassForNewUser = False
        isAuth = False
        ipSrv = addr[0]
        usr = getUser(ipSrv)
        if usr == '':
            noNameForNewUser = True
            noPassForNewUser = True
            sendSocket(conn, "Input name")
        else:

            sendSocket(conn, f"Hello {usr}! Enter password:")
            isAuth = True

    message = recvSocket(conn)
    if message is None:
        conn.close()
        writeLogs(f'Отключение клиента {addr[0]}')
        isDisconnect = True
        continue

    if noNameForNewUser and noPassForNewUser:
        nameNewUser = message
        noNameForNewUser = False

        sendSocket(conn, "Input password")
        continue

    if not noNameForNewUser and noPassForNewUser:
        passNewUser = hashlib.sha224(message.encode()).hexdigest()

        my_file = open("list_ip.txt", "a")
        my_file.write(f"{addr[0]} {nameNewUser} {passNewUser}\n")
        my_file.close()

        sendSocket(conn, "Registration OK")
        noPassForNewUser = False
        continue

    if isAuth:
        if getPass(ipSrv) == hashlib.sha224(message.encode()).hexdigest():
            sendSocket(conn, f"Hello {usr}! Authentication succeeded!")
            isAuth = False
        else:

            sendSocket(conn, f"Hello {usr}! Authentication error! Enter password:")
        continue
    print(f'Прием данных {message} от клиента {usr}')
    try:
        if message == "exit":
            continue
    except ConnectionResetError:
        print("Выход из системы")
    sendSocket(conn, message)
    print(f'Отправка данных {message} клиенту {usr}')
    open('list_logs.txt', 'w').close()


