#from pymongo import MongoClient
import json
import pymongo
banco = pymongo.MongoClient("mongodb+srv://sardinha12:sardinha12@cluster0-6llki.mongodb.net/quiz?retryWrites=true&w=majority")

class Questao():

    def __init__(self, id, tipo, sentenca, feedback, pontuacao, tempo_resposta, nivel_aprend, nivel_de_dificul, visibilidade):
        self.id = id
        self.tipo = tipo
        self.sentenca = sentenca
        self.feedback = feedback
        self.pontuacao = pontuacao
        self.tempo_resposta = tempo_resposta
        self.nivel_aprendizado = nivel_aprend
        self.nivel_dificuldade = nivel_de_dificul
        self.visibilidade = visibilidade

    def set_id(self, id):
        self.id = id

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_sentenca(self, sentenca):
        self.sentenca = sentenca

    def set_feedback(self,  feedback):
        self.feedback = feedback

    def set_pontuacao(self, pontuacao):
        self.pontuacao = pontuacao

    def set_tempo_resposta(self, tempo):
        self.tempo_resposta = tempo

    def set_nivel_aprendizado(self, nivel):
        self.nivel_aprendizado = nivel

    def set_nivel_dificuldade(self, nivel_dificuldade):
        self.nivel_dificuldade = nivel_dificuldade

    def set_visibilidade(self, visibilidade):
        self.visibilidade = visibilidade

    def get_id(self):
        return self.id

    def get_tipo(self):
        return self.tipo

    def get_sentenca(self):
        return self.sentenca

    def get_feedback(self):
        return self.feedback

    def get_pontuacao(self):
        return self.pontuacao

    def get_tempo_resposta(self):
        return self.tempo_resposta

    def get_nivel_aprendizado(self):
        return self.nivel_aprendizado

    def get_nivel_dificuldade(self):
        return self.nivel_dificuldade

    def get_visibilidade(self):
        return self.visibilidade

    def salvar_no_repositorio(self, objeto_usuario_corrente, objeto_alternativas, objeto_resposta):
        dados_questao = json.dumps({"id": self.id,
                                    "tipo": self.tipo,
                                    "sentenca": self.sentenca,
                                    "feedback": self.feedback,
                                    "pontuacao": self.pontuacao,
                                    "tempo_resposta": self.tempo_resposta,
                                    "nivel_aprendizado": self.nivel_aprendizado,
                                    "nivel_dificuldade": self.nivel_dificuldade,
                                    "visibilidade": 'Pública',
                                    "autor": objeto_usuario_corrente,
                                    "alternativas": objeto_alternativas,
                                    "resposta": objeto_resposta
                                    })
        collection_questao = banco.disciplina_repositorio_questao
        objeto_questao = json.loads(dados_questao)
        collection_questao.insert_one(objeto_questao)

    def atualizar_questao_no_repositorio(self, objeto_usuario_corrente, objeto_alternativas, objeto_resposta):
        dados_questao = json.dumps({
            "tipo": self.tipo,
            "sentenca": self.sentenca,
            "feedback": self.feedback,
            "pontuacao": self.pontuacao,
            "tempo_resposta": self.tempo_resposta,
            "nivel_dificuldade": self.nivel_dificuldade,
            "nivel_aprendizado": self.nivel_aprendizado,
            "autor": objeto_usuario_corrente,
            "alternativas": objeto_alternativas,
            "resposta": objeto_resposta
        })
        objeto_questao = json.loads(dados_questao)
        banco.disciplina_repositorio_questao.update_one({"id": int(self.id)}, {"$set": objeto_questao})


    def salvar_na_atividade(self, id_atividade, objeto_usuario_corrente, objeto_alternativas, objeto_resposta):
        dados_questao = json.dumps({"id": self.id,
                                    "tipo": self.tipo,
                                    "sentenca": self.sentenca,
                                    "feedback": self.feedback,
                                    "pontuacao": self.pontuacao,
                                    "tempo_resposta": self.tempo_resposta,
                                    "visibilidade": self.visibilidade,
                                    "nivel_aprendizado": self.nivel_aprendizado,
                                    "nivel_dificuldade": self.nivel_dificuldade,
                                    "autor": objeto_usuario_corrente,
                                    "alternativas": objeto_alternativas,
                                    "resposta": objeto_resposta
                                    })
        objeto_questao = json.loads(dados_questao)
        banco.disciplina_atividade.update_one({"id": int(id_atividade['id'])},
                                           {"$push": {"questoes": objeto_questao}})

    def editar_na_atividade(self, id_atividade, objeto_usuario_corrente, objeto_alternativas, objeto_resposta):
        dados_questao = json.dumps({
            "id": self.id,
            "tipo": self.tipo,
            "sentenca": self.sentenca,
            "feedback": self.feedback,
            "pontuacao": self.pontuacao,
            "tempo_resposta": self.tempo_resposta,
            "nivel_dificuldade": self.nivel_dificuldade,
            "visibilidade": self.visibilidade,
            "nivel_aprendizado": self.nivel_aprendizado,
            "autor": objeto_usuario_corrente,
            "alternativas": objeto_alternativas,
            "resposta": objeto_resposta
        })
        objeto_questao = json.loads(dados_questao)
        banco.disciplina_atividade.update_one({"id": int(id_atividade), "questoes.id": self.id},
                                           {"$set": {'questoes.$': objeto_questao}})
