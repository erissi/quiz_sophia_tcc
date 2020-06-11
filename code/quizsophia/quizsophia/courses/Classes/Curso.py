class Curso:

    def __init__(self, nome, adm, alunos):
        self.nome = nome
        self.adm = adm
        self.alunos = alunos

    def set_nome(self, nome):
        self.nome = nome

    def set_adm(self,  adm):
        self.adm = adm

    def set_alunos(self, alunos):
        self.alunos = alunos

    def set_ID(self, id):
        self.id = id

    def get_nome(self):
        return self.nome

    def get_adm(self):
        return self.adm

    def get_alunos(self):
        return self.alunos

    def get_ID(self):
        return self.id