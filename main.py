import bcrypt
import getpass
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Configuração do banco de dados
engine = create_engine("sqlite:///gestao_financeira.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    rua = Column('rua', String)
    numero = Column('numero', Integer)
    email = Column('email', String)
    _senha = Column('senha', String)
    idade = Column('idade', Integer)
    limite_mensal = Column('limite mensal', Float)
    dinheiro_total = Column('dinheiro total', Float)
    transacoes = relationship("Transacao", back_populates="usuario")

    
    def __init__(self, nome, rua, numero, senha, idade, email, limite_mensal, dinheiro_total):
        self.nome = nome
        self.rua = rua
        self.numero = numero
        self._senha = senha
        self.idade = idade
        self.email = email
        self.limite_mensal = limite_mensal
        self.dinheiro_total = dinheiro_total
      
    
    
    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, senha):
        hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        self._senha = hashed.decode('utf-8')
        print('Senha colocada com sucesso!')

    
    
    def __repr__(self):
        return (f'ID: {self.id}\nNome: {self.nome}\nRua: {self.rua}\nNumero: {self.numero}\n'
                f'Idade: {self.idade}\nEmail: {self.email}\nSenha: {self.senha.setter}Limite Mensal: {self.limite_mensal}\nDinheiro total: {self.dinheiro_total}')


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    valor = Column('valor', Float)
    tipo_pagamento = Column('tipo de pagamento', String)
    data_transacao = Column('data da transação', String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="transacoes")
    produtos = relationship("Produto", back_populates="transacoes")

    
    def __init__(self, valor, tipo_pagamento, data_transacao, usuario_id):

        self.valor = valor
        self.tipo_pagamento = tipo_pagamento
        self.data_transacao = data_transacao
        self.usuario_id = usuario_id
        
    
    @property
    def get_id(self):
        return self.id
        
    
    
    def __repr__(self):
        return (f'ID: {self.id}\nValor: {self.valor}\nTipo de Pagamento: {self.tipo_pagamento}\n'
                f'Data da Transação: {self.data_transacao}\n')


class Produto(Base):
    __tablename__ = "produtos"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    valor_produto = Column('valor do produto', Integer)
    nome_produto = Column('nome do produto', String)
    quantidade = Column('quantidade', Integer)
    usuario_id = Column(ForeignKey('usuarios.id'))
    transacao_id = Column(ForeignKey('transacoes.id'))
    transacoes = relationship("Transacao", back_populates="produtos")# Relação muitos-para-muitos com Transacao

    def __init__(self, valor_produto, nome_produto, quantidade, transacoes_id, usuario_id):

        self.valor_produto = valor_produto
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.transacoes_id = transacoes_id
        self.usuario_id = usuario_id
    
    
    def __repr__(self):
        return f'ID: {self.id}\n Valor do Produto: {self.valor_produto}\nQuantidade: {self.quantidade}'


Base.metadata.create_all(engine)# Criação das tabelas no banco de dados

# u1 = Usuario(nome='Fábio', rua='Rua Penha', numero=12, senha='senha123', idade=19, email='fabio.gmail.com', limite_mensal=18000)
# session.add(u1)
# session.commit()



def adicionar_usuario():
    
    print(25 * '-')
    print('| CADASTRO DE USUÁRIOS  |')  
    print(25 * '-')


    
    try:
        
        nome = input('Digite seu nome completo: ')
        print(90 * '--')
        rua = input('Digite sua rua: ')
        print(90 * '--')

        
        try:
            numero = int(input('Digite o seu número do seu endereço: '))
            print(90 * '--')
        except ValueError:
            print('Erro: Digite um número válido para o número da rua.')
            sys.exit()  

        
        email = input('Digite o email: ').lower()
        print(90 * '--')
        senha = getpass.getpass("Digite sua senha: ")
        print(90 * '--')

       
        try:
            idade = int(input("Digite sua idade: "))
            print(90 * '--')
            if idade < 18:
                print('Você não pode ser cadastrado, porque é menor de idade :(')
                sys.exit()
        except ValueError:
            print('Erro: Digite um número válido para a idade.')
            sys.exit()

       
        try:
            limite_mensal = int(input("Digite seu limite mensal: "))
            print(90 * '--')
        except ValueError:
            print('Erro: Digite um número válido para o limite mensal.')
            sys.exit()

        try:
            dinheiro_total = float(input("Digite seu dinheiro total: "))
            print(90 * '--')
        
        except ValueError:
            print('Erro: Digite números válidos')

        
        usuario = Usuario(
            nome=nome,
            rua=rua,
            numero=numero,
            email=email,
            senha=senha,
            idade=idade,
            limite_mensal=limite_mensal,
            dinheiro_total = dinheiro_total
        )

        
        usuario.senha = senha
        session.add(usuario)
        session.commit()
        print("Usuário adicionado com sucesso!")

    finally:
        print('Fim da execução.')
        print(90 * '--')
    
    


    def adicionar_transacao():
        
        

        pergunta = input("Você quer fazer alguma transação? S/N ").upper()

        if pergunta.startswith('S'):
            pass

        elif pergunta.startswith('N'):
            print('Ok, acabando a execução do programa.')
            sys.exit()

        else:
            print('Você não selecionou nenhuma das opções válidas. Parando a execução do programa.')
            sys.exit()

        
        
        try:
            valor = float(input("Digite o valor da transação: "))
            print(90 * '--')
        
        except ValueError:
            print('Digite um número válido.')
            sys.exit()

        if usuario.dinheiro_total >= valor:
            usuario.dinheiro_total -= valor
        
        else:
            print('Você não tem dinheiro o suficiente para fazer essa compra')
            sys.exit()
        
        tipo_pagamento = input('Digite o tipo de pagamento(pix, cartao, boleto, etc): ')
        print(90 * '--')
        data_transacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        dono = usuario.id

        
        
        
        transacao = Transacao(
            
            valor=valor,
            tipo_pagamento = tipo_pagamento,
            data_transacao = data_transacao,
            usuario_id = dono

        )

        
        session.add(transacao)
        session.flush()
        print('Transação adicionada com sucesso')

        
        

        def adicionar_produtos():
                dono_transacao = transacao.id
                nome_produto = input("Digite o nome do produto: ")
                    
                try:
                    valor_produto = float(input("Digite o valor do produto por unidade: "))
                    print(90 * '--')
                    
                except ValueError:
                    print("Digite números válidos para o valor do produto")
                    sys.exit()
                    
                try:
                    quantidade = int(input("Digite a quantidade do produto que você comprou: "))
                    print(90 * '--')

                    if quantidade > 1:
                        valor_produto = valor_produto * quantidade

                except ValueError:
                    print('Digite um número válido para a quantidade de produtos')

                    
                produtos = Produto(
                    nome_produto = nome_produto,
                    valor_produto = valor_produto,
                    quantidade = quantidade,
                    transacoes_id = dono_transacao,
                    usuario_id = dono

                        
                )

                session.add(produtos)
                    
                session.commit()
                
                if quantidade > 1:
                    print('Produtos cadastrados com sucesso!')
                    
                elif quantidade == 1:
                    print("Produto cadastrado com sucesso!")
            
        
        adicionar_produtos()
            
            


    adicionar_transacao()
    

adicionar_usuario()













