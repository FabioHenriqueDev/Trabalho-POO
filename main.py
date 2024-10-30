# Trabalho POO, faculdade Impacta
# Sistema de Venda de Ingressos de Cinema
# Desenvolvido_por = ['Fábio Henrique', 'Gustavo Spilla', 'Guilherme Santos', 'Helena Andreassi']

import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base



engine = create_engine("sqlite:///gestao_financeira.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    rua = Column(String)
    numero = Column(Integer)
    __senha = Column(String)
    idade = Column(Integer)
    email = Column(String)
    limite_mensal = Column(Integer)
    
    
    def __repr__(self):
        return f'ID: {self.id}\nNome: {self.nome}\n Rua: {self.rua}\nNumero: {self.numero}\nIdade: {self.idade}\nEmail: {self.email}\nLimite Mensal: {self.limite_mensal}'


class Transacao(Base):
    __tablename__ = "transações"
    
    id = Column(Integer, primary_key=True)
    valor = Column(float)
    tipo_pagamento = Column(String)
    data_transacao = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Transacao", back_populates="usuario")



class Produto(Base):
    __tablename__ = "transações"
    






