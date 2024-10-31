import sqlite3
import bcrypt
import getpass
import sys
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Configuração do banco de dados
engine = create_engine("sqlite:///gestao_financeira.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Tabela de associação para a relação muitos-para-muitos entre Transacao e Produto
transacao_produto_associacao = Table(
    'transacao_produto', Base.metadata,
    Column('transacao_id', Integer, ForeignKey('transacoes.id'), primary_key=True),
    Column('produto_id', Integer, ForeignKey('produtos.id'), primary_key=True)
)

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
    produtos = relationship("Produto", secondary=transacao_produto_associacao, back_populates="transacoes")# Relação muitos-para-muitos com Produto

    
    def __init__(self, valor, tipo_pagamento, data_transacao, usuario_id):

        self.valor = valor
        self.tipo_pagamento = tipo_pagamento
        self.data_transacao = data_transacao
        self.usuario_id = usuario_id
        
    
    
    def __repr__(self):
        return (f'ID: {self.id}\nValor: {self.valor}\nTipo de Pagamento: {self.tipo_pagamento}\n'
                f'Data da Transação: {self.data_transacao}\n')


class Produto(Base):
    __tablename__ = "produtos"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    valor_produto = Column('valor do produto', Integer)
    nome_produto = Column('nome do produto', String)
    quantidade = Column('quantidade', Integer)
    transacoes = relationship("Transacao", secondary=transacao_produto_associacao, back_populates="produtos")# Relação muitos-para-muitos com Transacao

    def __init__(self, valor_produto, nome_produto, quantidade, transacoes):

        self.valor_produto = valor_produto
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.transacoes = transacoes
    
    
    def __repr__(self):
        return f'ID: {self.id}\n Valor do Produto: {self.valor_produto}\nQuantidade: {self.quantidade}'


Base.metadata.create_all(engine)# Criação das tabelas no banco de dados

# u1 = Usuario(nome='Fábio', rua='Rua Penha', numero=12, senha='senha123', idade=19, email='fabio.gmail.com', limite_mensal=18000)
# session.add(u1)
# session.commit()



def adicionar_usuario():
    try:
        
        nome = input('Digite seu nome: ')
        print(90 * '--')
        rua = input('Digite sua rua: ')
        print(90 * '--')

        
        try:
            numero = int(input('Digite o seu número: '))
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
            dinheiro_total = int(input("Digite seu dinheiro total: "))
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

adicionar_usuario()




        











# def adicionar_usuário(id, nome, rua, numero, senha, idade, email, limite_mensal):
      
#     usuario = session.query(Usuario).filter_by(id=id, nome=nome, rua=rua, numero=numero, senha=senha, idade=idade, email=email, limite_mensal=limite_mensal).first()
#     usuario.senha = senha
#     session.add(usuario)
#     session.commit()
        
# def adicionar_transacao(id, valor, tipo_pagamento, data_transacao, usuario_id, produtos):
    
#     transacao = session.query(Transacao).filter_by(id=id, valor=valor, tipo_pagamento=tipo_pagamento, data_transacao=data_transacao, usuario_id=usuario_id, produtos=produtos).first()
#     session.add(transacao)
#     session.commit()


