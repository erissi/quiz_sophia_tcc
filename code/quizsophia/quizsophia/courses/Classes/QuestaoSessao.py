from pymongo import MongoClient
import json

import pymongo
banco = pymongo.MongoClient("mongodb+srv://sardinha12:sardinha12@cluster0-6llki.mongodb.net/quiz?retryWrites=true&w=majority")


class QuestaoSessao:

    def __init__(self, id_questao, sentenca, feedback, resposta_correta, resposta_aluno):
        self.id_questao = id_questao
        self.sentenca = sentenca
        self.feedback = feedback
        self.resposta_correta = resposta_correta
        self.resposta_aluno = resposta_aluno
        self.acertou = self.verifica_resposta(resposta_correta, resposta_aluno)

    def set_id(self, id):
        self.id_questao = id

    def set_sentenca(self, descricao):
        self.sentenca = descricao

    def set_feedback(self, feedback):
        self.feedback = feedback

    def set_resposta_correta(self, resposta_correta):
        self.resposta_correta = resposta_correta

    def set_resposta_aluno(self, resposta_aluno):
        self.resposta_aluno = resposta_aluno

    def get_id(self):
        return self.id_questao

    def get_sentenca(self):
        return self.sentenca

    def get_feedback(self):
        return self.feedback

    def get_resposta_correta(self):
        return self.resposta_correta

    def get_resposta_aluno(self):
        return self.resposta_aluno

    def set_acertou(self, resp):
        self.acertou = resp

    def get_acertou(self):
        return self.acertou

    def verifica_resposta(self, resposta_correta, resposta_aluno):
        if resposta_aluno == resposta_correta:
            acertou = True
        else:
            acertou = False
        return acertou

    def salvar(self, id_atividade):

        dados_questao = json.dumps({
            "id": self.id_questao,
            "sentenca": self.sentenca,
            "feedback": self.feedback,
            "resposta_correta": self.resposta_correta,
            "resposta_aluno": self.resposta_aluno,
            "acertou": self.acertou
        })
        objeto_questao = json.loads(dados_questao)
        banco.disciplina_atividade_sessao.update_one({"id": int(id_atividade)}, {"$push": {"questoes": objeto_questao}})

    def recupera(self, id_atividade):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        questao_bd = banco.disciplina_atividade.find({'id': int(id_atividade)}, {'questoes': int(self.id_questao)})
        return questao_bd
