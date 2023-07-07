from termcolor import colored
from time import sleep

menu = colored('''
======== Sistema Bancário ========

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> ''', 'yellow', attrs=['bold'])

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
        print(colored(' DEPÓSITO '.center(20, '-'), 'cyan', attrs=['bold']))
        deposito = float(input('Informe o valor que deseja depositar: '))
        lista_deposito.append(deposito)
        saldo += deposito
        sleep(2)
        print(colored('\nDepósito realizado com sucesso!', 'green'))

    elif opcao == 2:
        print(colored(' SAQUE '.center(20, '-'), 'cyan', attrs=['bold']))
        if numero_saques < LIMITE_SAQUES:
            valor_saque = float(input('Informe o valor que deseja sacar: '))
            print()
            if valor_saque <= LIMITE:
                if valor_saque <= saldo:
                    lista_saques.append(valor_saque)
                    saldo -= valor_saque
                    numero_saques += 1
                    sleep(2)
                    print(colored('Saque realizado com sucesso!\n', 'green') +
                          f'\nValor sacado: R$ {valor_saque:.2f}' +
                          '\nRetire o valor na boca do caixa!')
                else:
                    print(colored('Saldo Insuficiente!', 'red') +
                        f'\nValor disponível na conta: R$ {saldo:.2f}')
            else:
                print(colored('Saque negado!\n', 'red') +
                        f'\nValor de saque máximo permitido: R$ {LIMITE:.2f}')
        else:
            print(colored('\nMáximo de saques diários efetuados!' +
                  '\nVolte outro dia e tente novamente.', 'orange'))
            sleep(2)

    elif opcao == 3:
        print(colored(' EXTRATO '.center(20, '-'), 'cyan', attrs=['bold']))
        
        if lista_deposito or lista_saques:
            print(colored('Depósitos realizados:', 'green'))
            for i, deposito in enumerate(lista_deposito):
                print(f'{i + 1}º depósito: R${deposito:.2f}')
            print(colored(f'Valor total depositado: R${sum(lista_deposito):.2f}', 'green'))
            
            print(colored('\nSaques realizados:', 'magenta'))
            for i, saque in enumerate(lista_saques):
                print(f'{i + 1}º saque: R$ {saque:.2f}')
            print(colored(f'Valor total sacado: R$ {sum(lista_saques):.2f}', 'magenta'))
        else:
            print('Não foram realizadas movimentações.')
        
        print(f'\nSaldo atual da conta: R$ {saldo:.2f}')

    elif opcao == 0:
        print(colored('Obrigado por utilizar o nosso sistema.\n' +
              'Tenha um excelente dia!\n', 'yellow') +
              colored('==================================\n', 'yellow', attrs=['bold']))
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
