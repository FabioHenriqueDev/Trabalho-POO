# Trabalho POO, faculdade Impacta
# Sistema de Venda de Ingressos de Cinema

import sqlite3
import sys

class Filme:
    def __init__(self, titulo, genero, duracao, classificacao, sinopse):
        self.titulo = titulo
        self.genero = genero
        self.duracao = duracao
        self.classificacao = classificacao
        self.sinopse = sinopse

        if isinstance(self.classificacao, int):
            self.classificacao = classificacao
        
        else:
            print("Erro: Digite um número para a classificação")
            sys.exit(1)


    
    @property
    def detalhes(self):
        return f'{90 * '--'}\nFilme: {self.titulo}\n{90 * '--'}\nGenero: {self.genero}\n{90 * '--'}\nDuração: {self.duracao}\n{90 * '--'}\nClassificação: {self.classificacao}\n{90 * '--'}\nSinopse: {self.sinopse}\n{90 * '--'}'

    @detalhes.setter
    def detalhes(self, titulo, genero, duracao, classificacao, sinopse):
        self.titulo = titulo
        self.genero = genero
        self.duracao = duracao
        self.sinopse = sinopse

    




f1 = Filme("Vingadores: Ultimato", 'ação', '2h30', 12, 'Após Thanos eliminar metade das criaturas vivas,\nos Vingadores têm de lidar com a perda de amigos e entes queridos.\nCom Tony Stark vagando perdido no espaço sem água e comida,\nSteve Rogers e Natasha Romanov lideram a resistência contra o titã louco.')
print(f1.detalhes)







class Sala:
    def __init__(self, numero, capacidade):
        pass
    


class Sessao:
    pass

class Ingresso:
    def __init__(self, numero_sala, qtnd_assentos, tipo_sessao):
        self.numero_sal = numero_sala
        self.qtnd_assentos = qtnd_assentos
        self.tipo_sessao = tipo_sessao


