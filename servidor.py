import socket
import threading

# Simula um banco de dados com os funcionários registrados no sistema, pertencem ao papel de funcionarios
list_funcionario = ["joao", "pedro", "ana"]

# Simula um banco de dados com os gerentes registrados no sistema, pertencem ao papel de gerentes
list_gerente = ["maria", "jose", "carlos"]

rotas = ["funcionario", "gerente"]

# Função para verificar se o usuário tem acesso à rota
def verificar_acesso(usuario, rota):
    
    if rota == "funcionario":
        return usuario in list_funcionario # Verifica se o usuário está na lista de funcionários
    
    elif rota == "gerente":
        return usuario in list_gerente # Verifica se o usuário está na lista de gerentes
    
    else:
        return False


# Função para lidar com uma conexão individual
def handle_connection(conn, addr):
    print('Conectado por', addr)
    while True:
        # Recebe os dados do cliente
        data = conn.recv(1024).decode()
        
        # Se não houver mais dados, encerra a conexão
        if not data:
            break
        usuario, rota = data.split(",")
        
        # Verifica se a rota é válida
        if rota not in rotas:
            conn.sendall("Rota inválida!\n")
            continue
        
        # Verifica se o usuário tem acesso à rota
        if verificar_acesso(usuario, rota):
            conn.sendall(b"status 200. Acesso permitido.\n") # Envia uma resposta 200 ao cliente
        else:
            conn.sendall(b"status 403. Acesso negado!\n") # Envia uma resposta 403 ao cliente
    conn.close()


# Configurações de rede
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta usada pelo servidor

# Criação do socket do servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.bind((HOST, PORT)) # Associa o socket a um endereço e porta
    s.listen() # Aguarda por conexões
    
    print("Aguardando conexão...")

    try:
        while True:
            conn, addr = s.accept()
            # Iniciar um novo thread para lidar com a conexão
            threading.Thread(target=handle_connection, args=(conn, addr)).start()
            
    # Encerra o servidor quando o usuário pressiona Ctrl+C
    except KeyboardInterrupt:
        print("Servidor encerrado.")
        s.close()