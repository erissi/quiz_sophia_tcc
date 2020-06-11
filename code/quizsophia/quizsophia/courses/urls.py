from idlelib.textview import view_file

from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('listadeatividades/', views.listaDeAtividades, name='atividades'),

    path('meuperfil/', views.meuperfil, name='meuperfil'),

    path('listadeatividades/criaratividade', views.criaratividade, name='criaratividade'),
    path('listadeatividades/<id>/editaratividade', views.editaratividade, name='editaratividade'),
    path('listadeatividades/<id>/detalheatividade', views.detalhesatividade, name='detalhesatividade'),
    path('listadeatividades/<id>/excluiratividade', views.excluiratividade, name='excluiratividade'),

    path('listadeatividades/<id>/iniciar', views.iniciar, name='iniciar'),
    path('<id>/respondendo', views.respondendo, name='respondendo'),
    path('listadeatividades/respondendo/<id>/resultado', views.resultado, name='resultado'),

    path('repositorio/criarquestao/', views.criarquestao, name='criarquestao'),
    path('repositorio/<id>/editarquestao', views.editarquestaorepositorio, name='editarquestaorepositorio'),
    path('repositorio/<id>/detalhequestao', views.detalhesquestao, name='detalhesquestao'),
    path('repositorio/<id>/excluirquestao', views.excluirquestao, name='excluirquestao'),
    path('repositorio/<id>/clonarquestao', views.clonarquestao, name='clonarquestao'),



    path('listadeatividades/<id_atividade>/detalhequestao/<id_questao>', views.detalhesquestaoatividade, name='detalhesquestaoatividade'),
    path('listadeatividades/<id_atividade>/editarquestao/<id_questao>', views.editarquestaoatividade, name='editarquestaoatividade'),
    path('listadeatividades/<id_atividade>/excluirquestao/<id_questao>', views.excluirquestaoatividade, name='excluirquestaoatividade'),
    path('listadeatividades/criarquestaoatividade', views.criarquestaoatividade, name='criarquestaoatividade'),

    #path('paginainicial/', views.home, name='home'),
    path('repositorio', views.repositorio, name='repositorio'),
    path('', views.home, name='home'),
    path('sair', views.sair, name='sair'),

    path('estatisticas', views.estatisticas, name='estatisticas'),
    path('estatisticas/<id>/analisequestoes', views.analise_questoes, name='analise_questoes'),
    path('estatisticas/<id_atividade>/analisequestoes/<id_questao>/analisealternativas', views.analise_alternativas, name= 'analise_alternativas'),

    path('listadeatividades/<id>/ranking', views.ranking, name='ranking'),

    path('meuperfil/<id>/detalheatividadesessao', views.detalhesatividadesessao, name='detalhesatividadesessao')
]
