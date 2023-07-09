def menu():
    menu = ('\n\n=========== Sistema Bancário ===========\n' +
            '\n[1]\tDepositar' +
            '\n[2]\tSacar' +
            '\n[3]\tExibir Extrato' +
            '\n[4]\tNova Conta' +
            '\n[5]\tListar Contas' +
            '\n[6]\tExcluir Conta' +
            '\n[7]\tNovo Usuário' +
            '\n[8]\tListar Usuários' +
            '\n[9]\tExcluir Usuário'
            '\n[0]\tSair\n' +
            '\n=> ')
    return int(input(menu))


def depositar(saldo: float, extrato, /):
    valor = float(input('Informe o valor que deseja depositar: '))
    
    if valor > 0:
        extrato += f'Depósito:\tR$ {valor:.2f}\n'
        saldo += valor
        print(f'\n=== Depósito realizado com sucesso! ===')
    else:
        print('\n@@@ Operação falhou! O valor informado é inválido.')
    
    return saldo, extrato


def sacar(*, saldo: float, extrato, limite, numero_saques, limite_saques):
    valor = float(input('Informe o valor que deseja sacar: '))
    excedeu_saques = numero_saques >= limite_saques
    excedeu_limite = valor > limite
    excedeu_saldo = valor > saldo
    
    if excedeu_limite:
        print('\n@@@ Operação falhou! O valor solicitado excedeu o limite. @@@' +
              f'\nValor de saque máximo permitido: R$ {limite:.2f}')
    elif excedeu_saques:
        print('\n@@@ Operação falhou! O número máximo de saques foi excedido. @@@')
    elif excedeu_saldo:
        print('\n@@@ Operação falhou! Seu saldo é insuficiente. @@@' +
              f'\nValor disponível na conta: R$ {saldo:.2f}')
    elif valor > 0:
        extrato += f'Saque:\t\tR$ {valor:.2f}\n'
        saldo -= valor
        numero_saques += 1
        print('\n=== Saque realizado com sucesso! ===' +
              f'\nValor sacado: R$ {valor:.2f}')
    else:
        print('\n@@@ Operação falhou! O valor informado é inválido. @@@')
        
    return saldo, extrato, numero_saques


def exibir_extrato(saldo: float, /, *, extrato):
    print('\n----------- EXTRATO -----------\n' +
          ('Não foram realizadas movimentações.\n' if not extrato else extrato) +
          f'\nSaldo:\t\tR$ {saldo:.2f}' +
          '\n-------------------------------')


def criar_conta(agencia, usuarios: list, numero_conta):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print('\n=== Conta criada com sucesso! ===')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    
    print('\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@')


def listar_contas(contas: list):
    if contas:
        print('\n------ LISTAGEM DE CONTAS ------')
        for conta in contas:
            linha = (f'\nAgência:\t{conta["agencia"]}' +
                    f'\nC/C:\t\t{conta["numero_conta"]}' +
                    f'\nTitular:\t{conta["usuario"]["nome"]}')
            print('-----' + linha)
        print('--------------------------------')
    else:
        print('\n@@@ Não há contas para serem listadas! @@@')


def criar_usuario(usuarios: list):
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print('\n@@@ Já existe usuário com esse CPF! @@@')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    
    print('Cadastro de Endereço:')
    endereco = {
        'logradouro': input('Informe o logradouro: '),
        'numero': input('Informe o número: '),
        'bairro': input('Informe o bairro: '),
        'cidade': input('Informe a cidade: '),
        'sigla': input('Informe a sigla do estado: ')
    }
    
    print('\n=== Usuário criado com sucesso! ===')
    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})


def filtrar_usuario(cpf, usuarios: list):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]  # apenas um usuário vai retornar desta lista
    return usuarios_filtrados[0] if usuarios_filtrados else None


def listar_usuarios(usuarios: list):
    if usuarios:
        print('\n----- LISTAGEM DE USUÁRIOS -----')
        for usuario in usuarios:
            endereco = usuario['endereco']
            linha = (f'\nNome: {usuario["nome"]}' +
                    f'\nData de Nascimento: {usuario["data_nascimento"]}' +
                    f'\nCPF: {usuario["cpf"]}' +
                    f'\nEndereço: {endereco["logradouro"]}, {endereco["numero"]} - ' + 
                    f'{endereco["bairro"]} - {endereco["cidade"]}/{endereco["sigla"]}')
            print('-----' + linha)
        print('---------------------------------')
    else:
        print('\n@@@ Não há usuários para serem listados! @@@')


def excluir_conta(contas: list):
    numero_conta = int(input('Informe o número da conta que deseja excluir: '))
    conta = filtrar_conta(numero_conta, contas)
    
    if conta:
        print('\n=== Conta excluída com sucesso ===')
        contas.remove(conta)
        return
    
    print('\n@@@ Esta conta não foi encontrada e por isso ela não pode ser removida! @@@')


def filtrar_conta(numero_conta, contas: list):
    contas_filtradas = [conta for conta in contas if conta['numero_conta'] == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None


def excluir_usuario(usuarios: list, contas: list):
    cpf = input('Informe o CPF do usuário que deseja excluir (somente número): ')
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print('\n=== Usuário excluido com sucesso! ===' +
              '\nTodas as contas deste usuário também foram apagadas.')
        var_aux = contas.copy()
        for conta in var_aux:
            if usuario == conta.get('usuario'):
                contas.remove(conta) 
        usuarios.remove(usuario)
        return
    
    print('\n@@@ O usuário não foi encontrado no banco de dados! @@@')


def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    
    saldo = 0
    LIMITE = 500
    extrato = ''
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()
        
        if opcao == 1:
            saldo, extrato = depositar(saldo, extrato)
        
        elif opcao == 2:
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, 
                extrato=extrato,
                limite=LIMITE,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
            
        elif opcao == 3:
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == 4:
            conta = criar_conta(AGENCIA, usuarios, numero_conta)
            
            if conta:
                contas.append(conta)
                numero_conta += 1
        
        elif opcao == 5:
            listar_contas(contas)
        
        elif opcao == 6:
            excluir_conta(contas)
        
        elif opcao == 7:
            criar_usuario(usuarios)
        
        elif opcao == 8:
            listar_usuarios(usuarios)
        
        elif opcao == 9:
            excluir_usuario(usuarios, contas)
        
        elif opcao == 0:
            print('Obrigado por utilizar o nosso sistema.\n' +
                  'Tenha um excelente dia!\n' +
                  ('=' * 40) + '\n')
            break
        
        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')


main()
