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
lista_saques = list()

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
                    lista_saques.append(valor_saque)
                    saldo -= valor_saque
                    numero_saques += 1
                    print('--- Saque realizado com sucesso ---\n' +
                          f'\nValor sacado: R$ {valor_saque:.2f}' +
                          '\nRetire o valor na boca do caixa!')                    
                else:
                    print('--- Saque negado ---\n' +
                          f'\nValor de saque máximo permitido: R$ {LIMITE:.2f}')
            else:
                print('--- Saldo Insuficiente ---' +
                      f'\nValor disponível na conta: R$ {saldo:.2f}')
        else:
            print('\nMáximo de saques diários efetuados!' +
                  '\nVolte outro dia e tente novamente.')

    elif opcao == 3:
        print(' Extrato '.center(20, '-'))
        
        if lista_deposito or lista_saques:
            print('Depósitos realizados:')
            for i, deposito in enumerate(lista_deposito):
                print(f'{i + 1}º depósito: R${deposito:.2f}')
            print(f'Valor total depositado: R${sum(lista_deposito):.2f}')
            
            print('\nSaques realizados:')
            for i, saque in enumerate(lista_saques):
                print(f'{i + 1}º saque: R$ {saque:.2f}')
            print(f'Valor total sacado: R$ {sum(lista_saques):.2f}')
        else:
            print('Não foram realizadas movimentações.')
        
        print(f'\nSaldo atual da conta: R$ {saldo:.2f}')

    elif opcao == 0:
        print('Obrigado por utilizar o nosso sistema.\n' +
              'Tenha um excelente dia!\n' +
              '==============================\n')
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
