from pymongo import MongoClient
import json

import pymongo
banco = pymongo.MongoClient("mongodb+srv://sardinha12:sardinha12@cluster0-6llki.mongodb.net/quiz?retryWrites=true&w=majority")


class AtividadeSessao:

    def __init__(self, id_atividade, id_proprio, nome, concluida, data_inicio, qtd_acertos, perc_acertos, qtd_questoes, pontuacao_aluno, pontuacao_geral):
        self.id_atividade = int(id_atividade)
        self.id = id_proprio
        self.nome = nome
        self.concluida = concluida
        self.data_inicio = data_inicio
        self.qtd_acertos = qtd_acertos
        self.perc_acertos = perc_acertos
        self.qtd_questoes = qtd_questoes
        self.pontuacao_aluno = pontuacao_aluno
        self.pontuacao_geral = pontuacao_geral
        self.questoes = []
        self.tentativa = 0
        self.premiacao = None

    def set_id(self, id):
        self.id_atividade = id

    def set_id_proprio(self, id):
        self.id_proprio = id

    def set_nome(self, nome):
        self.nome = nome

    def set_concluida(self, concluida):
        self.concluida = concluida

    def set_data_inicio(self, data_inicio):
        self.data_inicio = data_inicio

    def set_qtd_acertos(self, qtd_acertos):
        self.qtd_acertos = qtd_acertos

    def set_perc_acertos(self, perc_acertos):
        self.perc_acertos = perc_acertos

    def set_qtd_questoes(self, qtd_questoes):
        self.qtd_questoes = qtd_questoes

    def set_pontuacao_aluno(self, pontuacao_aluno):
        self.pontuacao_aluno = pontuacao_aluno

    def set_pontuacao_geral(self, pontuacao_geral):
        self.pontuacao_geral = pontuacao_geral

    def set_tentativa(self, tentativa):
        self.tentativa = tentativa

    def get_id(self):
        return self.id_atividade

    def get_id_proprio(self):
        return self.id_proprio

    def get_nome(self):
        return self.nome

    def get_concluida(self):
         return self.concluida

    def get_data_inicio(self):
        return self.data_inicio

    def get_qtd_acertos(self):
        return self.qtd_acertos

    def get_perc_acertos(self):
        return self.perc_acertos

    def get_qtd_questoes(self):
        return self.qtd_questoes

    def get_pontuacao_aluno(self):
        return self.pontuacao_aluno

    def get_pontuacao_geral(self):
        return self.pontuacao_geral

    def get_tentativa(self):
        return self.tentativa

    def add_questao(self, questao):
        self.questoes.append(questao)

    def get_qtd_tentativas(self, id_atividade, id_usuario, id_curso):
        qtd_tentativas = banco.disciplina_atividade_sessao.count_documents({'id_atividade': int(id_atividade), 'usuario.id': int(id_usuario), 'curso.id': int(id_curso)})
        self.tentativa = qtd_tentativas+1
        return self.tentativa


    def salvar(self, objeto_usuario, objeto_curso):
        dados_atividade = json.dumps({
            "id_atividade": self.id_atividade,
            "id": self.id,
            "nome": self.nome,
            "concluida": self.concluida,
            "data_inicio": self.data_inicio,
            "qtd_acertos": self.qtd_acertos,
            "perc_acertos": self.perc_acertos,
            "qtd_questoes": self.qtd_questoes,
            "pontuacao_aluno": self.pontuacao_aluno,
            "pontuacao_geral": self.pontuacao_geral,
            "questoes": [],
            "usuario": objeto_usuario,
            "curso": objeto_curso,
            "tentativa": self.tentativa
        })
        objeto_atividade = json.loads(dados_atividade)
        banco.disciplina_atividade_sessao.insert_one(objeto_atividade)