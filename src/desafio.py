from abc import ABC, abstractmethod
from datetime import datetime
import functools

class ContaIterador:
    def __init__(self, contas) -> None:
        self.contas = contas
        self.contador = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return (f"----- {conta.__str__()}" +
                    f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        except IndexError:
            print('--------------------------------')
            raise StopIteration


class Cliente:
    def __init__(self, endereco) -> None:
        self._endereco = ""
        self.endereco = endereco
        self._contas = []
     
    @property
    def endereco(self):
        return self._endereco
       
    @endereco.setter
    def endereco(self, endereco:dict):
        """Converte o dicionário em string"""
        for key, values in endereco.items():
            self._endereco += f"{key}:{values}\n"
            
    @property
    def contas(self):
        return self._contas
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento) -> None:
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(endereco)
        
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def idade(self):
        _ano_nascimento = int(self._data_nascimento.split("-")[-1])
        _ano_atual = int(datetime.now().year)
        return _ano_atual - _ano_nascimento
    

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor    
    
    def registrar(self, conta):
        _transacao_realizada = conta.depositar(self._valor)
        if _transacao_realizada:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor    
    
    def registrar(self, conta):
        _transacao_realizada = conta.sacar(self._valor)
        if _transacao_realizada:
            conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, numero:int = 0, cliente:Cliente = None) -> None:
        self._agencia = "0001"
        self._saldo = 0
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()
       
    @property 
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3) -> None:
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["Tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("\nOperação falhou! Número de saques excedido.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self) -> str:
        return (
            f'\nAgência:\t{self.agencia}' +
            f'\nC/C:\t\t{self.numero}' +
            f'\nTitular:\t{self.cliente.nome}'
        )


class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "Data": datetime.now().strftime("%d/%m/%Y | %H:%M"),
            }
        )
        
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self.transacoes:
            if tipo_transacao == 's' or tipo_transacao == 'd':
                x = 'Saque' if tipo_transacao == 's' else 'Deposito'
                if transacao['Tipo'] == x:
                    yield transacao
            else:
                yield transacao
        


def menu():
    menu = ('\n\n=========== Sistema Bancário ===========\n' +
            '\n[d]\tDepositar' +
            '\n[s]\tSacar' +
            '\n[e]\tExtrato' +
            '\n[nc]\tNova Conta' +
            '\n[lc]\tListar Contas' +
            '\n[nu]\tNovo Usuário' +
            '\n[q]\tSair\n' +
            '\n=> ')
    return input(menu)


def log_transacao(func):
    @functools.wraps(func)
    def decorador(*args, **kwargs):
        func(*args, **kwargs)
        print(f"Realizada função '{func.__name__.upper()}' --- {datetime.now().strftime('%H:%M | %d/%m/%Y')}")
    return decorador


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return
    valor = float(input('Informe o valor que deseja depositar: '))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return
    valor = float(input('Informe o valor que deseja sacar: '))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    tipo_transacao = input('Informe o tipo de transação que deseja consultar\n[s] Saque\n[d] Depósito\n[↵] Todos os movimentos: ')
    print("\n=============== EXTRATO ===============")
    extrato = ""
    transacoes = conta.historico.gerar_relatorio(tipo_transacao)
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += (
                f"\n{transacao['Tipo']} realizado em {transacao['Data']}.\nValor: R$ {transacao['Valor']:.2f}"
            )
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=======================================")


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


@log_transacao
def criar_conta(contas, clientes, numero_conta):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@')
        return
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('\n=== Conta criada com sucesso! ===')


def listar_contas(contas):
    if contas:
        print('\n------ LISTAGEM DE CONTAS ------')
        # TODO: alterar implementação, para utilizar a classe ContaIterador
        for conta in ContaIterador(contas):
            print(conta)
    else:
        print('\n@@@ Não há contas para serem listadas! @@@')


@log_transacao
def criar_cliente(clientes):
    cpf = input('Informe o CPF (somente número): ')
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print('\n@@@ Já existe cliente com esse CPF! @@@')
        return
    nome = input('Informe o nome completo: ').capitalize()
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    print('- Cadastro de Endereço -')
    endereco = {
        'Logradouro': input('Informe o logradouro: ').upper(),
        'Número': input('Informe o número: '),
        'Bairro': input('Informe o bairro: ').capitalize(),
        'Cidade': input('Informe a cidade: ').capitalize(),
        'Sigla': input('Informe a sigla do estado: ').upper()
    }
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print('\n=== Usuário criado com sucesso! ===')


def filtrar_cliente(cpf, clientes) -> Cliente:
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            conta = criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(contas, clientes, numero_conta)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print('Obrigado por utilizar o nosso sistema.\n' +
                  'Tenha um excelente dia!\n' +
                  ('=' * 40) + '\n')
            break
        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')


main()
