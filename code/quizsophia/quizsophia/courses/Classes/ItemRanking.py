

class ItemRanking:

    def __init__(self, posicao, nome, pontos, premio):
        self.posicao = posicao
        self.nome = nome
        self.pontos = pontos
        self.premio = premio

    def set_posicao(self, posicao):
        self.posicao = posicao

    def set_nome(self, nome):
        self.nome = nome

    def set_pontos(self, pontos):
        self.pontos = pontos

    def set_premio(self, premio):
        self.premio = premio

    def get_posicao(self):
        return self.posicao

    def get_nome(self):
        return self.nome

    def get_pontos(self):
        return self.pontos

    def get_premio(self):
        return self.premio
