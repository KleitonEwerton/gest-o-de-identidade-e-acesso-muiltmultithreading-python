import socket

# Dados do usuário e rota desejada
print("Digite o usuário:")
usuario = input() # Nome do usuário que deseja entrar

print("Digite a rota desejada:")
rota = input() # Rota desejada, para verificar se o papel desse usuario tem permição de acesso

# Configurações de rede
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta usada pelo servidor

# Conexão com o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f"{usuario},{rota}".encode())
    data = s.recv(1024).decode()

print('Resposta do servidor:', data)
