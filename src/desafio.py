menu = '''
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> '''

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3
lista_deposito = list()

while True:
    print(' Sistema Bancário '.center(30, '='))
    opcao = int(input(menu))
    
    if opcao == 1:
        print(' Depósito '.center(20, '-'))
        deposito = float(input('Informe o valor que deseja depositar (R$): '))
        lista_deposito.append(deposito)
        print('--- Depósito realizado com sucesso! ---', end='\n\n')
    elif opcao == 2:
        print(' Saque '.center(20, '-'))
    elif opcao == 3:
        # exibir todos os depositos aqui
        print(' Extrato '.center(20, '-'))
        print(lista_deposito)
    elif opcao == 0:
        print('Obrigado por utilizar o nosso sistema. Tenha um bom dia!\n' + ('=' * 30))
        break
    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')