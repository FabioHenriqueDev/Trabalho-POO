# Trabalho POO, faculdade Impacta
# Sistema de Venda de Ingressos de Cinema
# Desenvolvido por: [Fábio Henrique, Gustavo Spilla, Guilherme Santos]

import sqlite3
import sys

class Filme:
    def __init__(self, titulo, genero, duracao, classificacao, sinopse):
        self.titulo = titulo
        self.genero = genero
        self.duracao = duracao
        self.classificacao = classificacao
        self.sinopse = sinopse
        self.atores = []

        if isinstance(self.classificacao, int):
            self.classificacao = classificacao
        
        else:
            print("Erro: Digite um número para a classificação")
            sys.exit(1)


    @property
    def detalhes(self):
        return f'{90 * '--'}\nFilme: {self.titulo}\n{90 * '--'}\nGenero: {self.genero}\n{90 * '--'}\nDuração: {self.duracao}\n{90 * '--'}\nClassificação: {self.classificacao}\n{90 * '--'}\nSinopse: {self.sinopse}\n{90 * '--'}'

    
    def get_titulo(self):
        return self.titulo
    
    @detalhes.setter
    def detalhes(self, titulo, genero, duracao, classificacao, sinopse):
        self.titulo = titulo
        self.genero = genero
        self.duracao = duracao
        self.sinopse = sinopse

    
    def adicionar_ator(self, *atores):
        for ator in atores:   
            if isinstance(ator, str):
                self.atores.append(ator)
                self.atores.sort()
            
            else:
                print("Não tem como adicionar números, digite os nomes dos atores")
    
    def remover_ator(self, *atores):
        for ator in atores:
            self.atores.remove(ator)

    
    def pesquisar_ator(self, ator):
        if ator in self.atores:
            print(f'{ator}, está nesse filme!')

    
    def atualizar_detalhes_do_filme(self, titulo=None, genero=None, classificacao=None, sinopse=None):
        if titulo:
            self.titulo = titulo
        
        if genero:
            self.genero = genero
        
        if classificacao:
            if isinstance(classificacao, int):
                self.classificacao = classificacao
            else:
                print("Erro: Digite um número para a classificação")   
                
        if sinopse:
            self.sinopse = sinopse

    
    def listar_atores(self):
        print(f"Todos os atores do Filme {self.titulo}:")
        contador = 1
        for ator in self.atores:
            print(90 *'--')
            print(f'Ator{contador}: {ator}')
            contador += 1

    
    def buscar_por_genero(self, genero):
        print(90 * '--')
        return self.genero.lower() == genero.lower()
        
    
       



f1 = Filme("Vingadores: Ultimato", 'ação', '2h30', 12, 'Após Thanos eliminar metade das criaturas vivas,\nos Vingadores têm de lidar com a perda de amigos e entes queridos.\nCom Tony Stark vagando perdido no espaço sem água e comida,\nSteve Rogers e Natasha Romanov lideram a resistência contra o titã louco.')
print(f1.detalhes)

f1.adicionar_ator("Robert Downey Jr.", "Chris Evans", "Mark Ruffalo", "Chris Hemsworth", "Scarlett Johansson", "Jeremy Renner", "Don Cheadle", "Paul Rudd", "Brie Larson", "Karen Gillan", "Danai Gurira", "Benedict Wong", "Jon Favreau", "Bradley Cooper", "Gwyneth Paltrow", "Josh Brolin")
# print(f1.atores)

# print(200 * '--')

f1.remover_ator("Robert Downey Jr.", "Chris Evans")
# print(f1.atores)

f1.atualizar_detalhes_do_filme(titulo='Vingadores')
print(f1.titulo)

print(200 * '--')

f1.listar_atores()

print(f1.buscar_por_genero("ação"))





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


