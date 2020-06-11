from pymongo import MongoClient
import json

import pymongo
banco = pymongo.MongoClient("mongodb+srv://sardinha12:sardinha12@cluster0-6llki.mongodb.net/quiz?retryWrites=true&w=majority")


class Ranking:

    def __init__(self):
        self.lista = []

    def add_item_ranking(self, item_ranking):
        self.lista.append(item_ranking)

    def get_item_ranking_por_posicao(self, posicao):
        self.lista.pop(posicao)

    def get_lista(self):
        return self.lista

    def salvar(self, id_atividade, objeto_ranking):
        banco.disciplina_atividade.update_one({"id": int(id_atividade)},
                                           {"$set": {'ranking': objeto_ranking}})
