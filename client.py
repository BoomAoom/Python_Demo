import socket

cli = socket.socket()
cli.connect(("127.0.0.1", 8001))

news_bytes = cli.recv(1024)
print(str(news_bytes, encoding='utf-8'))
chosse = input('Please input chosse![1 to login,2 to register] >>\n').strip()
cli.sendall(bytes(chosse, encoding='utf-8'))

while True:
    if chosse == "2":
        username = input('Please Creation User Name! >>\n').strip()
        passwd = input('Please Creation Password! >>\n').strip()
        cli.sendall(bytes(username + '/' + passwd, encoding='utf-8'))
        news_bytes = cli.recv(1024)
        print(str(news_bytes, encoding='utf-8'))
        break
    elif chosse == "1":
        username = input('Please Input User Name! >>\n').strip()
        passwd = input('Please Input Password! >>\n').strip()
        cli.sendall(bytes(username + '/' + passwd, encoding='utf-8'))
        news_str = str(cli.recv(1024), encoding='utf-8')
        if news_str == '100':
            print('NO UserName:' + '[' + username + ']')
            continue
        elif news_str == "102":
            print('Welcome Back')
        else:
            print('Wrong password')
    else:
        break
