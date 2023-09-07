import random
import pandas as pd
import os

print("Diretório atual:", os.getcwd())

# Dicionário para armazenar os usuários e senhas
usuarios = {}

# Caminho para o arquivo CSV
caminho_arquivo = 'dados_usuarios.csv'

# Função para carregar os dados dos usuários a partir do arquivo CSV
def carregar_dados_do_csv():
    global usuarios
    if os.path.exists(caminho_arquivo):
        df = pd.read_csv(caminho_arquivo)
        usuarios = df.to_dict(orient='index')

# Função para salvar os dados dos usuários no arquivo CSV
def salvar_dados_em_csv():
    global usuarios
    # Crie um DataFrame Pandas a partir do dicionário de usuários
    df = pd.DataFrame.from_dict(usuarios, orient='index')

    # Remova a coluna de senha do DataFrame
    df.drop(columns=['senha'], inplace=True)

    # Salve o DataFrame em um arquivo CSV
    df.to_csv(caminho_arquivo, index=False)

    # Salve o DataFrame em um arquivo CSV
    df.to_csv('dados_usuarios.csv', index=False)

    carregar_dados_do_csv()

# Função para gerar um código aleatório
def gerar_codigo_aleatorio():
    return random.randint(1000, 9999)


# Função para verificar se existem usuários cadastrados
def existem_usuarios_cadastrados():
    return bool(usuarios)


# Função para cadastrar um novo usuário
def cadastrar_usuario():
    nome = input("Digite seu nome (ou pressione Enter para cancelar): ")

    if not nome:  # Verifica se o nome está vazio (Enter pressionado)
        print("Operação cancelada.")
        return

    senha = input("Digite sua senha (ou pressione Enter para cancelar): ")

    if not senha:  # Verifica se a senha está vazia (Enter pressionado)
        print("Operação cancelada.")
        return

    codigo = gerar_codigo_aleatorio()
    usuarios[codigo] = {"nome": nome, "senha": senha, "saldo": 0, "ganhos_extras": 0, "despesas": {}}
    print(f"Usuário cadastrado com sucesso! Seu código de acesso é: {codigo}")


# Função para fazer login
def fazer_login():
    while True:
        codigo_input = input("Digite seu código de acesso (ou pressione Enter para cancelar): ")

        # Verifique se a entrada está em branco (usuário pressionou Enter)
        if not codigo_input:
            print("Operação cancelada.")
            return None

        try:
            codigo = int(codigo_input)
            senha = input("Digite sua senha (ou pressione Enter para cancelar): ")

            if not senha:  # Verifica se a senha está vazia (Enter pressionado)
                print("Operação cancelada.")
                return None

            if codigo in usuarios and usuarios[codigo]["senha"] == senha:
                return codigo
            else:
                print("Código ou senha incorretos.")
        except ValueError:
            print("Entrada inválida. Digite um número válido como código de acesso.")

        try:
            codigo = int(codigo_input)
            senha = input("Digite sua senha (ou pressione Enter para cancelar): ")

            if not senha:  # Verifica se a senha está vazia (Enter pressionado)
                print("Operação cancelada.")
                return None

            if codigo in usuarios and usuarios[codigo]["senha"] == senha:
                return codigo
            else:
                print("Código ou senha incorretos.")
        except ValueError:
            print("Entrada inválida. Digite um número válido como código de acesso.")


def calcular_saldo(codigo):
    usuario = usuarios[codigo]
    saldo = usuario['saldo'] + usuario['ganhos_extras']

    for mes, despesas in usuario['despesas'].items():
        for despesa in despesas:
            saldo -= despesa['valor']

    usuario['saldo'] = saldo


# Função para modificar o salário mensal
def modificar_salario(codigo):
    salario_input = input("Digite seu salário mensal (ou pressione Enter para cancelar): ")

    if not salario_input:  # Verifica se o salário está vazio (Enter pressionado)
        print("Operação cancelada.")
        return

    salario = float(salario_input)
    usuarios[codigo]["saldo"] = salario
    calcular_saldo(codigo)


# Função para adicionar ganhos extras
def adicionar_ganhos_extras(codigo):
    ganhos_extras_input = input("Digite o valor dos ganhos extras (ou pressione Enter para cancelar): ")

    if not ganhos_extras_input:  # Verifica se os ganhos extras estão vazios (Enter pressionado)
        print("Operação cancelada.")
        return

    ganhos_extras = float(ganhos_extras_input)
    usuarios[codigo]["ganhos_extras"] = ganhos_extras
    calcular_saldo(codigo)


# Função para adicionar despesas mensais
def adicionar_despesas(codigo, mes):
    nome_despesa = input("Digite o nome da despesa (ou pressione Enter para cancelar): ")

    if not nome_despesa:  # Verifica se o nome da despesa está vazio (Enter pressionado)
        print("Operação cancelada.")
        return

    valor_despesa_input = input("Digite o valor da despesa (ou pressione Enter para cancelar): ")

    if not valor_despesa_input:  # Verifica se o valor da despesa está vazio (Enter pressionado)
        print("Operação cancelada.")
        return

    valor_despesa = float(valor_despesa_input)

    if mes not in usuarios[codigo]["despesas"]:
        usuarios[codigo]["despesas"][mes] = []

    usuarios[codigo]["despesas"][mes].append({"nome": nome_despesa, "valor": valor_despesa})

    calcular_saldo(codigo)


# Função para exibir informações financeiras
def exibir_informacoes(codigo):
    usuario = usuarios[codigo]

    # Crie um DataFrame com os dados financeiros do usuário
    df = pd.DataFrame({
        'Nome': [usuario['nome']],
        'Saldo': [usuario['saldo']],
        'Ganhos Extras': [usuario['ganhos_extras']]
    })

    # Exiba o DataFrame
    print("\nInformações Financeiras:")
    print(df)

    # Verifique se há despesas e exiba-as em um DataFrame separado
    if usuario['despesas']:
        print("\nDespesas:")
        for mes, despesas in usuario['despesas'].items():
            df_despesas = pd.DataFrame(despesas)
            print(f"Mês: {mes}")
            print(df_despesas)


# Função para exibir a lista de usuários cadastrados
def listar_usuarios_cadastrados():
    # Crie um DataFrame Pandas a partir do dicionário de usuários
    df = pd.DataFrame.from_dict(usuarios, orient='index')

    # Exiba o DataFrame
    print("Lista de Usuários Cadastrados:")
    print(df)


# Loop principal
print("Bem vindo ao sistema de organização financeira pessoal OrSys 0.1 Alpha")

while True:
    print("\n1. Cadastrar usuário")
    print("2. Fazer login")
    print("3. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        listar_usuarios_cadastrados()
        codigo = fazer_login()
        if codigo is not None:
            while True:
                print("\n1. Modificar salário mensal")
                print("2. Adicionar ganhos extras")
                print("3. Adicionar despesas mensais")
                print("4. Exibir informações financeiras")
                print("5. Sair")

                opcao_usuario = input("Escolha uma opção: ")

                if opcao_usuario == "1":
                    modificar_salario(codigo)
                elif opcao_usuario == "2":
                    adicionar_ganhos_extras(codigo)
                elif opcao_usuario == "3":
                    mes = input("Digite o mês da despesa: ")
                    adicionar_despesas(codigo, mes)
                elif opcao_usuario == "4":
                    exibir_informacoes(codigo)
                elif opcao_usuario == "5":
                    # Salve os dados em CSV antes de sair
                    salvar_dados_em_csv()
                    break
                else:
                    print("Opção inválida.")
    elif opcao == "3":
        # Salve os dados em CSV antes de sair
        salvar_dados_em_csv()
        break
    else:
        print("Opção inválida.")