from .RequisitoTrofeu import RequisitoTrofeu
from pymongo import MongoClient

import pymongo
banco = pymongo.MongoClient("mongodb+srv://sardinha12:sardinha12@cluster0-6llki.mongodb.net/quiz?retryWrites=true&w=majority")


import json

class Atividade:

    def __init__(self, id, nome, descricao, aleatoria, exibicao_resp_corretas, data_inicial, data_final, ouro, prata, bronze):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.aleatoria = aleatoria
        self.exibicao_resp_corretas = exibicao_resp_corretas
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.requisitoTrofeu = RequisitoTrofeu(ouro, prata, bronze)
        self.questoes = []
        self.ranking = []
        self.autor = None
        self.curso = None
        self.numero_questoes = 0

    def set_id(self, id):
        self.id = id

    def set_nome(self, nome):
        self.nome = nome

    def set_descricao(self, descricao):
        self.descricao = descricao

    def set_aleatoria(self, aleatoria):
        self.aleatoria = aleatoria

    def set_exibicao_resp_corretas(self, exibicao_resp_corretas):
        self.exibicao_resp_corretas = exibicao_resp_corretas

    def set_data_inicial(self, data_inicial):
        self.data_inicial = data_inicial

    def set_data_final(self, data_final):
        self.data_final = data_final

    def set_requisito_trofeu_ouro(self, ouro):
        self.requisitoTrofeu.set_perc_ouro(ouro)

    def set_requisito_trofeu_prata(self, prata):
        self.requisitoTrofeu.set_perc_prata(prata)


    def set_requisito_trofeu_bronze(self, bronze):
        self.requisitoTrofeu.set_perc_bronze(bronze)

    def set_numero_de_questoes(self, numero):
        self.numero_questoes = numero

    def addListaQuestoes(self, lista_questoes):
        self.lista_de_questoes = lista_questoes

    def addQuestaoNaLista(self, questao):
        self.lista_de_questoes.append(questao)

    def removeQuestaoDaLista(self, questao):
        self.lista_de_questoes.remove(questao)

    def removeQuestaoPeloIndice(self, indice):
        self.lista_de_questoes.pop(indice)

    def retorna_questao_pelo_indice(self, indice):
        return self.lista_de_questoes[indice]

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_descricao(self):
        return self.descricao

    def get_aleatoria(self):
        return self.aleatoria

    def get_exibicao_resp_corretas(self):
        return self.exibicao_resp_corretas

    def get_data_inicial(self):
        return self.data_inicial

    def get_data_final(self):
        return self.data_final

    def get_requisito_trofeu_ouro(self):
        return self.requisitoTrofeu.get_perc_ouro()

    def get_requisito_trofeu_prata(self):
        return self.requisitoTrofeu.get_perc_prata()

    def get_requisito_trofeu_bronze(self):
        return self.requisitoTrofeu.get_perc_bronze()

    def get_numero_questoes(self):
        return self.numero_questoes

    def salvar(self, objeto_usuario_corrente, objeto_curso):

        dados_atividade = json.dumps({
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "aleatoria": self.aleatoria,
            "exibicao_resp_corretas": self.exibicao_resp_corretas,
            "data_inicial": self.data_inicial,
            "data_final": self.data_final,
            "perc_trof_ouro": self.requisitoTrofeu.get_perc_ouro(),
            "perc_trof_prata": self.requisitoTrofeu.get_perc_prata(),
            "perc_trof_bronze": self.requisitoTrofeu.get_perc_bronze(),
            "questoes": [],
            "ranking": [],
            "autor": objeto_usuario_corrente,
            "curso": objeto_curso
        })
        objeto_atividade = json.loads(dados_atividade)
        banco.disciplina_atividade.insert_one(objeto_atividade)

    def editar(self, id):

        dados_atividade = json.dumps({
            "nome": self.nome,
            "descricao": self.descricao,
            "aleatoria": self.aleatoria,
            "exibicao_resp_corretas": self.exibicao_resp_corretas,
            "data_inicial": self.data_inicial,
            "data_final": self.data_final,
            "perc_trof_ouro": self.requisitoTrofeu.get_perc_ouro(),
            "perc_trof_prata": self.requisitoTrofeu.get_perc_prata(),
            "perc_trof_bronze": self.requisitoTrofeu.get_perc_bronze()
        })
        objeto_atividade = json.loads(dados_atividade)
        banco.disciplina_atividade.update_one({"id": int(id)}, {"$set": objeto_atividade})