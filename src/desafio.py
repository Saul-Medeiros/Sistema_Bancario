menu = '''
====== Sistema Bancário ======

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> '''

saldo = 0
LIMITE = 500
numero_saques = 0
LIMITE_SAQUES = 3
lista_deposito = list()

while True:
    opcao = int(input(menu))
    print()
    
    if opcao == 1:
        print(' Depósito '.center(20, '-'))
        deposito = float(input('Informe o valor que deseja depositar: '))
        lista_deposito.append(deposito)
        saldo += deposito
        print('\n--- Depósito realizado com sucesso! ---')   
    elif opcao == 2:
        print(' Saque '.center(20, '-'))
        if numero_saques < LIMITE_SAQUES:
            valor_saque = float(input('Informe o valor que deseja sacar: '))
            print()
            if valor_saque <= saldo:
                if valor_saque <= LIMITE:
                    saldo -= valor_saque
                    numero_saques += 1
                    print('--- Saque realizado com sucesso ---\n',
                          f'Valor sacado: R${valor_saque:.2f}',
                          'Retire o valor na boca do caixa!',
                          sep='\n', end='\n')                    
                else:
                    print('--- Saque negado ---',
                          f'Valor de saque máximo permitido: R$ {LIMITE:.2f}',
                          sep='\n\n', end='\n')
            else:
                print('--- Saldo Insuficiente ---',
                      f'Valor disponível na conta: R$ {saldo:.2f}',
                      sep='\n', end='\n')
        else:
            print('\n--- Máximo de saques diários efetuados! ---',
                  'Volte outro dia e tente novamente.',
                  sep='\n', end='\n') 
    elif opcao == 3:
        # exibir todos os depositos aqui
        print(' Extrato '.center(20, '-'))
        print(lista_deposito)
    elif opcao == 0:
        print('Obrigado por utilizar o nosso sistema.\n',
              'Tenha um excelente dia!\n',
              '==============================')
        break
    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
