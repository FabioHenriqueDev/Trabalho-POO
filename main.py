import bcrypt
import sys
from datetime import datetime
import smtplib
import email.message 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


engine = create_engine("sqlite:///gestao_financeira.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    cpf = Column('cpf', Integer)
    email = Column('email', String)
    _senha = Column('senha', String)
    idade = Column('idade', Integer)
    limite_mensal = Column('limite mensal', Float)
    dinheiro_total = Column('dinheiro total', Float)
    transacoes = relationship("Transacao", back_populates="usuario")

    
    def __init__(self, nome, cpf, senha, idade, email, limite_mensal, dinheiro_total):
        self.nome = nome
        self.cpf = cpf
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
    nome_produto = Column('nome do produto', String)
    quantidade = Column('quantidade', Integer)
    usuario_id = Column(ForeignKey('usuarios.id'))
    transacao_id = Column(ForeignKey('transacoes.id'))
    transacoes = relationship("Transacao", back_populates="produtos")

    def __init__(self, nome_produto, quantidade, transacao_id, usuario_id):

        
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.transacao_id = transacao_id
        self.usuario_id = usuario_id
    
    
    def __repr__(self):
        return f'ID: {self.id}\n Valor do Produto: {self.valor_produto}\nQuantidade: {self.quantidade}'


Base.metadata.create_all(engine)# Criação das tabelas no banco de dados





def adicionar_usuario():
    
    while True:   
        pergunta_menu = input("1.Cadastro e Login\n2.Sair\nDigite uma dessas opções: ")

        if pergunta_menu == '1':
           pass
           break

        elif pergunta_menu == '2':
            print('Saindo...')
            sys.exit()

        else:
            print(90 * '--')
            print("Erro: Selecione uma das opções(1 ou 2).")
            print(90 * '--')
        

    

    print(25 * '-')
    print('| CADASTRO DE USUÁRIOS  |')  
    print(25 * '-')

    
        
    nome = input('Digite seu nome completo: ')
    print(90 * '--')
    
    try:
        cpf = input('Digite seu cpf: ')

        if len(cpf) != 11:
            print("Digite a quantidade correta de digitos de um cpf que é de 11.")
            sys.exit()

        if int(cpf) < 0:
            print('Não é possível adicionar valores negativos.')
            sys.exit()
        
    except ValueError:
        print('Digite números válidos no cpf.')
        sys.exit()
        
    print(90 * '--')

        
      
    email = input('Digite o email: ').lower()
        
    if '@' not in email:
        print('Erro: Email inválido, deve sempre conter @')
        sys.exit()
        
    elif '.' not in email:
        print("Erro: Email deve conter o .")
        sys.exit()
        
        
    print(90 * '--')
    senha = input("Digite sua senha: ")
    confirme_senha = input("Confirme sua senha: ")
    if senha == confirme_senha:
        print('senha adicionada com sucesso.')
        pass
        
    else:
        print("As senhas nao se coincidem.")
        sys.exit()

    print(90 * '--')

       
    try:
        idade = int(input("Digite sua idade: "))
            
        if idade < 0:
            print('Não é possível adicionar valores negativos.')
            sys.exit()
            
        print(90 * '--')
            
        if idade < 18:
            print('Você não pode ser cadastrado, porque é menor de idade :(')
            sys.exit()
        
    except ValueError:
        print('Erro: Digite um número válido para a idade.')
        sys.exit()

       
    try:
        limite_mensal = int(input("Digite seu limite mensal: "))
            
        if limite_mensal < 0:
            print('Não é possível adicionar valores negativos.')
            sys.exit()
            
        print(90 * '--')
    except ValueError:
         print('Erro: Digite um número válido para o limite mensal.')
         sys.exit()

    try:
        dinheiro_total = float(input("Digite seu dinheiro total: "))
            
        if dinheiro_total < 0:
            print('Não é possível adicionar valores negativos.')
            sys.exit()
            
        print(90 * '--')
        
    except ValueError:
        print('Erro: Digite números válidos')

        
    usuario = Usuario(
        nome=nome,
        cpf=cpf,
        email=email,
        senha=senha,
        idade=idade,
        limite_mensal=limite_mensal,
        dinheiro_total=dinheiro_total
    )

        
    usuario.senha = senha
    session.add(usuario)
    session.commit()
    print("Usuário adicionado com sucesso!")

    remetente = usuario.email
    senha_remetente = 'rwwwrfybejqwgies'
    destinatario = usuario.email
    print('Pegando dados do email...\nIsso pode demorar alguns instantes')
        
    #criação da mensagem de email
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = "Confirmação de email"

    #corpo do email
    corpo_email = f'''
        <p>Prezados,</p>

        <p>Obrigado por se cadastrar no nosso sistema!</p>
        {usuario.nome}
            '''
        
    mensagem.attach(MIMEText(corpo_email, "html"))
    try:
        #Conexão com servidor smtp
            with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
                servidor.starttls() #Ativa a segurança TLS
                servidor.login(remetente, senha_remetente)
                servidor.sendmail(remetente, destinatario, mensagem.as_string())#Enviando email
                print(f'{usuario.nome}, um email foi enviado para o endereço: {usuario.email}.')
        
    except Exception as e:
        print(f"Erro ao enviar o email {e}")

        
 

    
    
    def login():
        print(25 * '-')
        print('| LOGIN DE USUÁRIO      |')
        print(25 * '-')

        email = input("Digite seu email: ").strip().lower()
        senha = input("Digite sua senha: ")

        
        if '@' not in email or '.' not in email:
            print("Erro: Email inválido. Deve conter '@' e '.'.")
            return

        try:
            
            usuario = session.query(Usuario).filter_by(email=email).first()

            if not usuario:
                print("Erro: Usuário não encontrado.")
                return

            
            if bcrypt.checkpw(senha.encode('utf-8'), usuario._senha.encode('utf-8')):
                print("Usuário autorizado!")
                print(f"Bem-vindo, {usuario.nome} (ID: {usuario.id})")
                print(90 * '--')
                informacao_usuario = print(f'Informações de cadastro\n\nID: {usuario.id}\n\nNome: {usuario.nome}\n\nCPF: {usuario.cpf}\n\nEmail: {usuario.email}\n\nSenha Criptografada: {usuario.senha}\n\nIdade: {usuario.idade}\n\nLimite Mensal: {usuario.limite_mensal}\n\nDinheiro Total: {usuario.dinheiro_total}')
                print(90 * '--')
                adicionar_transacao()
                return usuario  
            
            else:
                print("Erro: Senha incorreta.")
                return

        except Exception as e:
            print(f"Ocorreu um erro durante o login: {e}")
            return

    
    
    def adicionar_transacao():
        pergunta = input("Você quer fazer alguma transação? S/N ").upper()
        gastos_usuario = 0

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
            
            if valor < 0:
                print('Não é possível adicionar valores negativos.')
                sys.exit()
            

            if gastos_usuario + valor >= usuario.limite_mensal:
                pergunta = input("Essa transação vai passar do seu limite mensal, você tem certeza que quer executala? S/N: ").upper()
                
                if pergunta == 'S':
                    pass

                elif pergunta == 'N':
                    print('Transação cancelada com sucesso.')
                    sys.exit()

            print(90 * '--')
        
        except ValueError:
            print('Digite um número válido.')
            sys.exit()

        if usuario.dinheiro_total >= valor:
            usuario.dinheiro_total -= valor
        
        else:
            print('Você não tem dinheiro o suficiente para fazer essa compra')
            sys.exit()
        
        tipo_pagamento = input('Qual foi seu tipo de pagamento?\n\n1.Pix\n2.Cartão de débito\n3.Cartão de crédito\n4.Transferência\n5.Outro\nDigite uma das opções: ')

        if tipo_pagamento == '1':
            tipo_pagamento = 'Pix'
        
        elif tipo_pagamento == '2':
            tipo_pagamento = 'Cartão de débito'
        
        elif tipo_pagamento == '3':
            tipo_pagamento = 'Cartão de crédito'
        
        elif tipo_pagamento == '4':
            tipo_pagamento = 'Transferência'

        elif tipo_pagamento == '5':
            digite_forma_pagamento = input("Digite outra forma de pagamento: ")
            tipo_pagamento = digite_forma_pagamento
        
        else:
            print('Você não digitou nenhuma das opções parando a execução do programa.')
            sys.exit()

        print(90 * '--')
        data_transacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        dono = usuario.id

        transacao = Transacao(
            valor=valor,
            tipo_pagamento=tipo_pagamento,
            data_transacao=data_transacao,
            usuario_id=dono
        )

        
        session.add(transacao)
        session.flush()
        session.commit()

        

        def adicionar_produtos():
            nome_produto = input("Digite o nome do produto: ")
            print(90 * '--')
                
            try:
                quantidade = int(input("Digite a quantidade do produto que você comprou: "))
                
                if quantidade < 0:
                    print('Não é possível adicionar valores negativos.')
                    sys.exit()
                
                print(90 * '--')

            except ValueError:
                print('Digite um número válido para a quantidade de produtos')
                  
            produtos = Produto(
                nome_produto=nome_produto,
                quantidade=quantidade,
                transacao_id=transacao.id,
                usuario_id=dono
            )

            session.add(produtos)
            session.commit()
            
            print('Transação adicionada com sucesso')
            
            if quantidade > 1:
                print('Produtos cadastrados com sucesso!')
                
            elif quantidade == 1:
                print("Produto cadastrado com sucesso!")
        
        adicionar_produtos()
            
    adicionar_transacao()
    login()




adicionar_usuario()













