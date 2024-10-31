import sqlite3
import bcrypt
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

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    rua = Column(String)
    numero = Column(Integer)
    _senha = Column(String)
    idade = Column(Integer)
    email = Column(String)
    limite_mensal = Column(Integer)
    transacoes = relationship("Transacao", back_populates="usuario")

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
                f'Idade: {self.idade}\nEmail: {self.email}\nSenha : {self.senha.setter}Limite Mensal: {self.limite_mensal}')


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    tipo_pagamento = Column(String)
    data_transacao = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="transacoes")
    produtos = relationship("Produto", secondary=transacao_produto_associacao, back_populates="transacoes")# Relação muitos-para-muitos com Produto

    def __repr__(self):
        return (f'ID: {self.id}\nValor: {self.valor}\nTipo de Pagamento: {self.tipo_pagamento}\n'
                f'Data da Transação: {self.data_transacao}\n')


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    valor_produto = Column(Integer)
    nome_produto = Column(String)
    quantidade = Column(Integer)
    transacoes = relationship("Transacao", secondary=transacao_produto_associacao, back_populates="produtos")# Relação muitos-para-muitos com Transacao

    def __repr__(self):
        return f'ID: {self.id}\n Valor do Produto: {self.valor_produto}\nQuantidade: {self.quantidade}'


Base.metadata.create_all(engine)# Criação das tabelas no banco de dados

def adicionar_usuário(id, nome, rua, numero, senha, idade, email, limite_mensal):
      
    usuario = session.query(Usuario).filter_by(id=id, nome=nome, rua=rua, numero=numero, senha=senha, idade=idade, email=email, limite_mensal=limite_mensal).first()
    usuario.senha = senha
    session.add(usuario)
    session.commit()
        
def adicionar_transacao(id, valor, tipo_pagamento, data_transacao, usuario_id, produtos):
    
    
    
    
    transacao = session.query(Transacao).filter_by(id=id, valor=valor, tipo_pagamento=tipo_pagamento, data_transacao=data_transacao, usuario_id=usuario_id, produtos=produtos).first()
    session.add(transacao)
    session.commit()


