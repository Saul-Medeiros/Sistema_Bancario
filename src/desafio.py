from termcolor import colored

menu = colored('''
=========== Sistema Bancário ===========

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> ''', 'yellow', attrs=['bold'])

saldo = 0
LIMITE = 500
numero_saques = 0
LIMITE_SAQUES = 3
extrato = ''

while True:
    opcao = int(input(menu))
    print()
    
    if opcao == 1:
        deposito = float(input('Informe o valor que deseja depositar: '))
        if deposito > 0:
            extrato += f'Depósito: R$ {deposito:.2f}\n'
            saldo += deposito
            print(colored('\nDepósito realizado com sucesso!', 'green'))
        else:
            print(colored('Operação falhou! O valor informado é inválido.', 'red'))

    elif opcao == 2:
        valor = float(input('Informe o valor que deseja sacar: '))
        
        excedeu_saques = numero_saques >= LIMITE_SAQUES
        excedeu_limite = valor > LIMITE
        excedeu_saldo = valor > saldo
        
        if excedeu_limite:
            print(colored('\nSaque negado!', 'red') +
                    f'\nValor de saque máximo permitido: R$ {LIMITE:.2f}')
        
        elif excedeu_saques:
            print(colored('\nOperação falhou! Número máximo de saques excedido!', 'red'))
        
        elif excedeu_saldo:
            print(colored('Saldo Insuficiente!', 'red') +
                f'\nValor disponível na conta: R$ {saldo:.2f}')
        
        elif valor > 0:
            extrato += f'Saque: R$ {valor:.2f}\n'
            saldo -= valor
            numero_saques += 1
            print(colored('Saque realizado com sucesso!\n', 'green') +
                f'\nValor sacado: R$ {valor:.2f}')
        
        else:
            print(colored('Operação falhou! O valor informado é inválido.', 'red'))

    elif opcao == 3:
        print(colored('----------- EXTRATO -----------', 'cyan', attrs=['bold']),
              colored(('Não foram realizadas movimentações.\n' if not extrato else extrato), 'magenta'),
              colored(f'Saldo: R$ {saldo:.2f}', 'green'),
              colored('-------------------------------', 'cyan', attrs=['bold']), sep='\n')

    elif opcao == 0:
        print(colored('Obrigado por utilizar o nosso sistema.\n' +
              'Tenha um excelente dia!\n', 'yellow') +
              colored(('=' * 40), 'yellow', attrs=['bold']) +
              '\n')
        break

    else:
        print(colored('Operação inválida, por favor selecione novamente a operação desejada.', 'red'))
