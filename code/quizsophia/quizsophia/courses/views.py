from django.shortcuts import render
from pymongo import MongoClient
from datetime import datetime
from .forms import CriarAtividade, CriarQuestao, EditarQuestao, EditarAtividade, EditarQuestaoAtividade, CriarQuestaoAtividade, Criar_Alternativa_ME, Criar_Alternativa_VF, Criar_Alternativa_L, Alternativas_Resposta, Login
from .Classes.Atividade import Atividade
from .Classes.QuestaoEstatistica import QuestaoEstatistica
from .Classes.QuestaoSessao import QuestaoSessao
from .Classes.AtividadeSessao import AtividadeSessao
from .Classes.Usuario import Usuario
from .Classes.Curso import Curso
from .Classes.ItemRanking import ItemRanking
from .Classes.Ranking import Ranking
from .Classes.Questao import Questao

import json
import random

banco = MongoClient("mongodb+srv://sardinha12:sardinha12@cluster0-6llki.mongodb.net/quiz?retryWrites=true&w=majority")


def get_next_sequence_value(sequenceName):
    #client = MongoClient("localhost", 27017)
    #banco = client.quiz
    seqDocument = banco.contadores.find_and_modify({"id": sequenceName}, {"$inc": {"sequence_value": 1}}, True)
    return seqDocument['sequence_value']


def get_objeto_curso(curso, objeto_adm, id_curso):
    dados_curso = json.dumps({
        "id": id_curso,
        "nome": curso.get_nome(),
        "adm": objeto_adm,
        "alunos": []
    })
    objeto_curso = json.loads(dados_curso)
    return objeto_curso


def get_objeto_curso_existente(curso):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    doc = banco.disciplina.find_one({'nome': curso.get_nome(), 'adm.nome': curso.get_adm().get_nome()})
    alunos = doc['alunos']
    dados_curso = json.dumps({
        "id": doc['id'],
        "nome": doc['nome'],
        "adm": doc['adm'],
        "alunos": alunos
    })
    objeto_curso = json.loads(dados_curso)
    return objeto_curso


def get_objeto_alternativas(primeira_alt, segunda_alt, terceira_alt, quarta_alt, quinta_alt):
    dados = json.dumps({
        "primeira_alternativa": primeira_alt,
        "segunda_alternativa": segunda_alt,
        "terceira_alternativa": terceira_alt,
        "quarta_alternativa": quarta_alt,
        "quinta_alternativa": quinta_alt
    })
    objeto = json.loads(dados)
    return objeto


def get_objeto_alternativas_vf():
    dados = json.dumps({
        "primeira_alternativa": 'Verdadeiro',
        "segunda_alternativa": 'Falso'
    })
    objeto = json.loads(dados)
    return objeto


def get_objeto_usuario(usuario, id_usuario):
    dados_usuario = json.dumps({
        "id": id_usuario,
        "nome": usuario.get_nome(),
        "email": usuario.get_email(),
    })
    objeto_usuario = json.loads(dados_usuario)
    return objeto_usuario


def listaDeAtividades(request):
    if request.session.has_key('usuario_corrente'):
        #client = MongoClient("localhost", 27017)
        #banco = client.quiz
        template_name = 'courses/index.html'
        context = {}
        id_disciplina = request.session['id_disciplina']
        usuario_corrente = request.session['usuario_corrente']
        atividades = banco.disciplina_atividade.find({'curso.id': int(id_disciplina)})
        dados = get_dados_arquivo(request)
        professor = dados['professor']
        professor_dados = banco.disciplina.find_one({'id': int(id_disciplina), 'adm.email': professor['email']},
                                                       {'adm'})
        adm = professor_dados['adm']
        id_adm = adm['id']
        context['id_professor'] = id_adm
        context['usuario'] = usuario_corrente['id']
        context['atividades'] = atividades
        return render(request, template_name, context)

    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def criaratividade(request):
    if request.session.has_key('usuario_corrente'):
        context = {}
        context['is_valid'] = False
        usuario_corrente = request.session['usuario_corrente']
        if request.method == 'POST':
            form = CriarAtividade(request.POST)
            if form.is_valid():
                context['is_valid'] = True
                objid_atividade = get_next_sequence_value("atividade")
                objeto_usuario_corrente = verifica_usuarios_json(usuario_corrente['nome'], usuario_corrente['email'])
                dados = request.session['dados_json']
                professor = dados['professor']
                curso = Curso(dados['nome_disciplina'], Usuario(professor['nome'], professor['email']), dados['alunos'])
                objeto_curso = verifica_curso_e_adiciona(curso, curso.get_adm())
                atividade = Atividade(objid_atividade, form.cleaned_data['nome'], form.cleaned_data['descricao'],
                                      form.cleaned_data['aleatoria'],
                                      form.cleaned_data['exibicao_resp_corretas'],
                                      form.cleaned_data['data_inicial'].isoformat(),
                                      form.cleaned_data['data_final'].isoformat(),
                                      form.cleaned_data.get('perc_trof_ouro'), form.cleaned_data.get('perc_trof_prata'),
                                      form.cleaned_data.get('perc_trof_bronze'))
                atividade.salvar(objeto_usuario_corrente, objeto_curso)
                request.session['id_atividade'] = json.dumps({"id": objid_atividade})
                form = CriarAtividade()
        else:
            form = CriarAtividade()
        context['form'] = form
        template_name = 'courses/criaratividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def editaratividade(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        atividade = banco.disciplina_atividade.find_one({'id': int(id)})
        context['atividade'] = atividade
        if request.method == 'POST':
            form = EditarAtividade(request.POST)
            if form.is_valid():
                context['is_valid'] = True
                atividade = Atividade(form.cleaned_data['nome'], form.cleaned_data['descricao'],
                                      form.cleaned_data['aleatoria'],
                                      form.cleaned_data['exibicao_resp_corretas'],
                                      form.cleaned_data['data_inicial'].isoformat(),
                                      form.cleaned_data['data_final'].isoformat(),
                                      form.cleaned_data.get('perc_trof_ouro'), form.cleaned_data.get('perc_trof_prata'),
                                      form.cleaned_data.get('perc_trof_bronze'))
                atividade.editar(id)
                form = EditarAtividade()
        else:
            form = EditarAtividade()
            form.initial = {'nome': atividade['nome'], 'descricao': atividade['descricao'],
                            'aleatoria': atividade['aleatoria'],
                            'exibicao_resp_corretas': atividade['exibicao_resp_corretas'],
                            'data_inicial': atividade['data_inicial'], 'data_final': atividade['data_final'],
                            'perc_trof_ouro': atividade['perc_trof_ouro'],
                            'perc_trof_prata': atividade['perc_trof_prata'],
                            'perc_trof_bronze': atividade['perc_trof_bronze']}
        context['form'] = form
        template_name = 'courses/editaratividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def detalhesatividadesessao(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        request.session['id_atividade_sessao'] = json.dumps({"id": id})
        id_usuario = request.session['usuario_corrente']
        context['usuario'] = id_usuario['id']
        context['is_valid'] = False
        atividade = banco.disciplina_atividade_sessao.find_one({'id': int(id), 'tentativa': 1})
        context['atividade'] = atividade
        cursor = banco.disciplina_atividade_sessao.find({'id': int(id), 'tentativa': 1}, {'questoes'})
        questoes_da_atividade = cursor.next()
        context['questoes'] = questoes_da_atividade['questoes']
        template_name = 'courses/detalheatividadesessao.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)



def detalhesatividade(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        request.session['id_atividade'] = json.dumps({"id": id})
        id_usuario = request.session['usuario_corrente']
        context['usuario'] = id_usuario['id']
        context['is_valid'] = False
        atividade = banco.disciplina_atividade.find_one({'id': int(id)})
        context['atividade'] = atividade
        cursor = banco.disciplina_atividade.find({'id': int(id)}, {'questoes'})
        questoes_da_atividade = cursor.next()
        context['questoes'] = questoes_da_atividade['questoes']
        template_name = 'courses/detalheatividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def excluiratividade(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        atividade = banco.disciplina_atividade.find_one({'id': int(id)})
        context['atividade'] = atividade
        print(context['is_valid'])
        if request.method == 'POST':
            form = request.POST['enviar_']
            if form == 'enviar':
                context['is_valid'] = True
                banco.disciplina_atividade.delete_one({'id': int(id)})
        template_name = 'courses/excluiratividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)



def criarquestao(request):
    if request.session.has_key('usuario_corrente'):
        context = {}
        context['is_valid'] = False
        if request.method == 'POST':
            usuario_corrente = request.session['usuario_corrente']
            form = CriarQuestao(request.POST)
            form_alt = Criar_Alternativa_ME(request.POST)
            form_vf = Criar_Alternativa_VF(request.POST)
            form_l = Criar_Alternativa_L(request.POST)
            envio_ok = request.POST['enviar_']
            if envio_ok == 'enviar':
                if form.is_valid():
                    context['is_valid'] = True
                    objeto_usuario_corrente = verifica_usuarios_json(usuario_corrente['nome'], usuario_corrente['email'])
                    tipo = form.cleaned_data['tipo']
                    objeto_alternativas, objeto_resposta = retorna_objeto_alternativas_e_resposta(tipo, form_alt,
                                                                                                  form_l, form_vf)
                    id = get_next_sequence_value("questao")
                    questao = Questao(id, form.cleaned_data['tipo'], form.cleaned_data['sentenca'], form.cleaned_data['feedback'], form.cleaned_data['pontuacao'],
                                  form.cleaned_data['tempo_resposta'], form.cleaned_data['nivel_aprendizado'], form.cleaned_data['nivel_dificuldade'], 'Pública')
                    questao.salvar_no_repositorio(objeto_usuario_corrente, objeto_alternativas, objeto_resposta)
                    form = CriarQuestao()
                    form_alt = Criar_Alternativa_ME()
                    form_vf = Criar_Alternativa_VF()
                    form_l = Criar_Alternativa_L()
        else:
            form = CriarQuestao()
            form_alt = Criar_Alternativa_ME()
            form_vf = Criar_Alternativa_VF()
            form_l = Criar_Alternativa_L()
            form.initial = {'tipo': 'Múltipla Escolha', }
        context['form'] = form
        context['form_alt'] = form_alt
        context['form_vf'] = form_vf
        context['form_l'] = form_l
        template_name = 'courses/criarquestaorepositorio.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def objeto_alternativas_ME(form):
    dados = json.dumps({
        "primeira_alternativa": form.cleaned_data['primeira_alternativa'],
        "segunda_alternativa": form.cleaned_data['segunda_alternativa'],
        "terceira_alternativa": form.cleaned_data['terceira_alternativa'],
        "quarta_alternativa": form.cleaned_data['quarta_alternativa'],
        "quinta_alternativa": form.cleaned_data['quinta_alternativa']
    })
    objeto_alternativas = json.loads(dados)
    return objeto_alternativas


def objeto_alternativas_L(form):
    dados = json.dumps({
        "primeira_alternativa": form.cleaned_data['primeira_alternativa_l'],
        "segunda_alternativa": form.cleaned_data['segunda_alternativa_l'],
        "terceira_alternativa": form.cleaned_data['terceira_alternativa_l'],
        "quarta_alternativa": form.cleaned_data['quarta_alternativa_l'],
        "quinta_alternativa": form.cleaned_data['quinta_alternativa_l']
    })
    objeto_alternativas = json.loads(dados)
    return objeto_alternativas


def objeto_alternativas_VF():
    dados = json.dumps({
        "primeira_alternativa": 'Verdadeiro',
        "segunda_alternativa": 'Falso'
    })
    objeto_alternativas = json.loads(dados)
    return objeto_alternativas


def objeto_resposta_correta_ME(form):
    if form.cleaned_data['correta'] == '1° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['primeira_alternativa']})
    elif form.cleaned_data['correta'] == '2° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['segunda_alternativa']})
    elif form.cleaned_data['correta'] == '3° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['terceira_alternativa']})
    elif form.cleaned_data['correta'] == '4° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['quarta_alternativa']})
    elif form.cleaned_data['correta'] == '5° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['quinta_alternativa']})
    objeto_resposta = json.loads(dados_resposta)
    return objeto_resposta


def objeto_resposta_correta_L(form):
    if form.cleaned_data['correta_l'] == '1° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['primeira_alternativa_l']})
    elif form.cleaned_data['correta_l'] == '2° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['segunda_alternativa_l']})
    elif form.cleaned_data['correta_l'] == '3° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['terceira_alternativa_l']})
    elif form.cleaned_data['correta_l'] == '4° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['quarta_alternativa_l']})
    elif form.cleaned_data['correta_l'] == '5° Alternativa':
        dados_resposta = json.dumps({"correta": form.cleaned_data['quinta_alternativa_l']})
    objeto_resposta = json.loads(dados_resposta)
    return objeto_resposta


def editarquestaorepositorio(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        questao_selecionada = banco.disciplina_repositorio_questao.find_one({'id': int(id)})
        context['questao'] = questao_selecionada
        if request.method == 'POST':
            usuario_corrente = request.session['usuario_corrente']
            form = EditarQuestao(request.POST)
            form_alt = Criar_Alternativa_ME(request.POST)
            form_vf = Criar_Alternativa_VF(request.POST)
            form_l = Criar_Alternativa_L(request.POST)
            if form.is_valid():
                context['is_valid'] = True
                objeto_usuario_corrente = verifica_usuarios_json(usuario_corrente['nome'], usuario_corrente['email'])
                tipo = questao_selecionada['tipo']
                objeto_alternativas, objeto_resposta = retorna_objeto_alternativas_e_resposta(tipo, form_alt, form_l, form_vf)
                questao = Questao(int(id), form.cleaned_data['tipo'], form.cleaned_data['sentenca'],form.cleaned_data['feedback']
                                  , form.cleaned_data['pontuacao'], form.cleaned_data['tempo_resposta'], form.cleaned_data['nivel_aprendizado'],
                                  form.cleaned_data['nivel_dificuldade'], form.cleaned_data['visibilidade'])
                questao.atualizar_questao_no_repositorio(objeto_usuario_corrente, objeto_alternativas, objeto_resposta)
                form = EditarQuestao()
                form_alt = Criar_Alternativa_ME()
                form_vf = Criar_Alternativa_VF()
                form_l = Criar_Alternativa_L()
        else:
            form = EditarQuestao()
            form_alt = Criar_Alternativa_ME()
            form_vf = Criar_Alternativa_VF()
            form_l = Criar_Alternativa_L()
            form = form_inicializar(form, questao_selecionada)
            alternativas = questao_selecionada['alternativas']
            resposta = questao_selecionada['resposta']
            if questao_selecionada['tipo'] == 'Múltipla Escolha':
                form_alt = form_alt_inicializar(form_alt, alternativas, resposta)
            elif questao_selecionada['tipo'] == 'Lacunas':
                form_l = form_l_inicializar(form_l, alternativas, resposta)
            elif questao_selecionada['tipo'] == 'Verdadeiro ou Falso':
                form_vf.initial = {'correta_vf': resposta['correta'],}
        context['form'] = form
        context['form_alt'] = form_alt
        context['form_vf'] = form_vf
        context['form_l'] = form_l
        template_name = 'courses/editarquestao.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def retorna_objeto_alternativas_e_resposta(tipo, form_alt, form_l, form_vf):
    if tipo == 'Múltipla Escolha':
        if form_alt.is_valid():
            objeto_alternativas = objeto_alternativas_ME(form_alt)
            objeto_resposta = objeto_resposta_correta_ME(form_alt)
    elif tipo == 'Lacunas':
        if form_l.is_valid():
            objeto_alternativas = objeto_alternativas_L(form_l)
            objeto_resposta = objeto_resposta_correta_L(form_l)
    elif tipo == 'Verdadeiro ou Falso':
        if form_vf.is_valid():
            objeto_alternativas = objeto_alternativas_VF()
            dados_resposta = json.dumps({"correta": form_vf.cleaned_data['correta_vf']})
            objeto_resposta = json.loads(dados_resposta)
    return objeto_alternativas, objeto_resposta


def form_inicializar(form, questao_selecionada):
    form.initial = {'tipo': questao_selecionada['tipo'], 'sentenca': questao_selecionada['sentenca'],
                    'feedback': questao_selecionada['feedback'],
                    'pontuacao': questao_selecionada['pontuacao'],
                    'tempo_resposta': questao_selecionada['tempo_resposta'],
                    'nivel_aprendizado': questao_selecionada['nivel_aprendizado'],
                    'visibilidade': questao_selecionada['visibilidade'],
                    'nivel_dificuldade': questao_selecionada['nivel_dificuldade'],
                    }
    return form


def form_alt_inicializar(form, alternativas, resposta):
    form.initial = {
        'primeira_alternativa': alternativas['primeira_alternativa'],
        'segunda_alternativa': alternativas['segunda_alternativa'],
        'terceira_alternativa': alternativas['terceira_alternativa'],
        'quarta_alternativa': alternativas['quarta_alternativa'],
        'quinta_alternativa': alternativas['quinta_alternativa'],
        'correta': resposta['correta'],
    }
    return form


def form_l_inicializar(form, alternativas, resposta):
    form.initial = {
        'primeira_alternativa_l': alternativas['primeira_alternativa'],
        'segunda_alternativa_l': alternativas['segunda_alternativa'],
        'terceira_alternativa_l': alternativas['terceira_alternativa'],
        'quarta_alternativa_l': alternativas['quarta_alternativa'],
        'quinta_alternativa_l': alternativas['quinta_alternativa'],
        'correta_l': resposta['correta'],
    }
    return form


def detalhesquestao(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        questao = banco.disciplina_repositorio_questao.find_one({'id': int(id)})
        context['questao'] = questao
        template_name = 'courses/detalhequestao.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def excluirquestao(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        questao = banco.disciplina_repositorio_questao.find_one({'id': int(id)})
        context['questao'] = questao
        if request.method == 'POST':
            form = request.POST['enviar_']
            if form == 'enviar':
                context['is_valid'] = True
                banco.disciplina_repositorio_questao.delete_one({'id': int(id)})
        template_name = 'courses/excluirquestao.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def clonarquestao(request, id):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        questao = banco.disciplina_repositorio_questao.find_one({'id': int(id)})
        context['questao'] = questao
        atividades = banco.disciplina_atividade.find({'curso.id': int(request.session['id_disciplina'])})
        context['atividades'] = atividades
        if request.method == 'POST':
            context['is_valid'] = True
            id_atividade = request.POST['atividades']
            objeto_questao = questao
            novo_id = get_next_sequence_value('questao')
            objeto_questao['id'] = novo_id
            del objeto_questao['_id']
            banco.disciplina_atividade.update_one({"id": int(id_atividade)}, {"$push": {"questoes": objeto_questao}})
        template_name = 'courses/clonarquestao.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def detalhesquestaoatividade(request, id_atividade, id_questao):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        questao_selecionada = ''
        context['is_valid'] = False
        atividade = banco.disciplina_atividade.find_one({'id': int(id_atividade)})
        context['atividade'] = atividade
        cursor = banco.disciplina_atividade.find({'id': int(id_atividade)}, {'questoes': int(id_questao)})
        questoes_da_atividade = cursor.next()
        lista_questoes = questoes_da_atividade['questoes']
        for questao in lista_questoes:
            if int(questao['id']) == int(id_questao):
                questao_selecionada = questao
        context['questao'] = questao_selecionada
        template_name = 'courses/detalhesquestaoatividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def criarquestaoatividade(request):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        if request.session.has_key('id_atividade'):
            id_atividade = json.loads(request.session['id_atividade'])
        atividade = banco.disciplina_atividade.find_one({'id': int(id_atividade['id'])})
        context['atividade'] = atividade
        if request.method == 'POST':
            usuario_corrente = request.session['usuario_corrente']
            form = CriarQuestaoAtividade(request.POST)
            form_alt = Criar_Alternativa_ME(request.POST)
            form_vf = Criar_Alternativa_VF(request.POST)
            form_l = Criar_Alternativa_L(request.POST)
            if form.is_valid():
                context['is_valid'] = True
                objeto_usuario_corrente = verifica_usuarios_json(usuario_corrente['nome'], usuario_corrente['email'])
                tipo = form.cleaned_data['tipo']
                objeto_alternativas, objeto_resposta = retorna_objeto_alternativas_e_resposta(tipo, form_alt, form_l, form_vf)
                id = get_next_sequence_value("questao")
                questao = Questao(id, form.cleaned_data['tipo'], form.cleaned_data['sentenca'], form.cleaned_data['feedback'],
                                  form.cleaned_data['pontuacao'], form.cleaned_data['tempo_resposta'],
                                  form.cleaned_data['nivel_aprendizado'], form.cleaned_data['nivel_dificuldade'], form.cleaned_data['visibilidade'])
                print('+++++++++  OBJETO RESPOSTA ++++++++++++++')
                print(objeto_resposta)
                questao.salvar_na_atividade(id_atividade, objeto_usuario_corrente, objeto_alternativas, objeto_resposta)
                if form.cleaned_data.get('visibilidade') == 'Pública':
                    questao.salvar_no_repositorio(objeto_usuario_corrente, objeto_alternativas, objeto_resposta)
                form = CriarQuestaoAtividade()
                form_alt = Criar_Alternativa_ME()
                form_vf = Criar_Alternativa_VF()
                form_l = Criar_Alternativa_L()
        else:
            form = CriarQuestaoAtividade()
            form.initial = {'tipo': 'Múltipla Escolha', }
            form_alt = Criar_Alternativa_ME()
            form_vf = Criar_Alternativa_VF()
            form_l = Criar_Alternativa_L()
        context['form'] = form
        context['form_alt'] = form_alt
        context['form_vf'] = form_vf
        context['form_l'] = form_l
        template_name = 'courses/criarquestaoatividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def editarquestaoatividade(request, id_atividade, id_questao):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        atividade = banco.disciplina_atividade.find_one({'id': int(id_atividade)})
        context['atividade'] = atividade
        cursor = banco.disciplina_atividade.find({'id': int(id_atividade)}, {'questoes': int(id_questao)})
        questoes_da_atividade = cursor.next()
        lista_questoes = questoes_da_atividade['questoes']
        for questao in lista_questoes:
            if int(questao['id']) == int(id_questao):
                questao_selecionada = questao
        context['questao'] = questao_selecionada
        if request.method == 'POST':
            usuario_corrente = request.session['usuario_corrente']
            form = EditarQuestaoAtividade(request.POST)
            form_alt = Criar_Alternativa_ME(request.POST)
            form_vf = Criar_Alternativa_VF(request.POST)
            form_l = Criar_Alternativa_L(request.POST)
            if form.is_valid():
                context['is_valid'] = True
                objeto_usuario_corrente = verifica_usuarios_json(usuario_corrente['nome'], usuario_corrente['email'])
                tipo = questao_selecionada['tipo']
                objeto_alternativas, objeto_resposta = retorna_objeto_alternativas_e_resposta(tipo, form_alt,
                                                                                              form_l, form_vf)
                questao = Questao(int(id_questao), questao_selecionada['tipo'], form.cleaned_data['sentenca'], form.cleaned_data['feedback'],
                                  form.cleaned_data['pontuacao'], form.cleaned_data['tempo_resposta'], form.cleaned_data['nivel_aprendizado'],
                                  form.cleaned_data['nivel_dificuldade'], form.cleaned_data['visibilidade'])
                questao.editar_na_atividade(id_atividade, objeto_usuario_corrente, objeto_alternativas, objeto_resposta)
                form = EditarQuestaoAtividade()
                form_alt = Criar_Alternativa_ME()
                form_vf = Criar_Alternativa_VF()
                form_l = Criar_Alternativa_L()
        else:
            form = EditarQuestaoAtividade()
            form_alt = Criar_Alternativa_ME()
            form_vf = Criar_Alternativa_VF()
            form_l = Criar_Alternativa_L()
            form = form_inicializar(form, questao_selecionada)
            alternativas = questao_selecionada['alternativas']
            resposta = questao_selecionada['resposta']
            if questao_selecionada['tipo'] == 'Múltipla Escolha':
                form_alt = form_alt_inicializar(form_alt, alternativas, resposta)
            elif questao_selecionada['tipo'] == 'Lacunas':
                form_l = form_l_inicializar(form_l, alternativas, resposta)
            elif questao_selecionada['tipo'] == 'Verdadeiro ou Falso':
                form_vf.initial = {'correta_vf': resposta['correta'], }
        context['form'] = form
        context['form_alt'] = form_alt
        context['form_vf'] = form_vf
        context['form_l'] = form_l
        template_name = 'courses/editarquestaoatividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def excluirquestaoatividade(request, id_atividade, id_questao):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        context['is_valid'] = False
        atividade = banco.disciplina_atividade.find_one({'id': int(id_atividade)})
        context['atividade'] = atividade
        cursor = banco.disciplina_atividade.find({'id': int(id_atividade)}, {'questoes': int(id_questao)})
        questoes_da_atividade = cursor.next()
        lista_questoes = questoes_da_atividade['questoes']
        for questao in lista_questoes:
            if int(questao['id']) == int(id_questao):
                questao_selecionada = questao
                context['questao'] = questao_selecionada
        if request.method == 'POST':
            form = request.POST['enviar_']
            if form == 'enviar':
                context['is_valid'] = True
                banco.disciplina_atividade.update_one({'id': int(id_atividade)},
                                                   {'$pull': {'questoes': {'id': int(id_questao)}}})
        template_name = 'courses/excluirquestaoatividade.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def repositorio(request):
    context = {}
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        template_name = 'courses/repositorio.html'
        questoes = banco.disciplina_repositorio_questao.find()
        usuario_corrente = request.session['usuario_corrente']
        dados = get_dados_arquivo(request)
        id_disciplina = request.session['id_disciplina']
        professor = dados['professor']
        professor_dados = banco.disciplina.find_one({'id': int(id_disciplina), 'adm.email': professor['email']}, {'adm'})
        adm = professor_dados['adm']
        id_adm = adm['id']
        context['id_professor'] = id_adm
        context['usuario'] = usuario_corrente['id']
        context['questoes'] = questoes
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def iniciar(request, id):
    questoes = []
    context = {}
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context['is_valid'] = False
        atividade = banco.disciplina_atividade.find_one({'id': int(id)})
        context['atividade'] = atividade
        template_name = 'courses/diretrizes.html'
        objeto_atividade = Atividade(id, atividade['nome'], atividade['descricao'], atividade['data_inicial'],
                                     atividade['data_final'],
                                     atividade['exibicao_resp_corretas'], atividade['aleatoria'],
                                     atividade['perc_trof_ouro'],
                                     atividade['perc_trof_prata'], atividade['perc_trof_bronze'])
        cursor = banco.disciplina_atividade.find({'id': int(id)}, {'questoes'})
        questoes_da_atividade = cursor.next()
        for questao in questoes_da_atividade['questoes']:
            questoes.append(questao)
        if objeto_atividade.aleatoria == "Sim":
            random.shuffle(questoes)
        objeto_atividade.addListaQuestoes(questoes)
        objeto_atividade.set_numero_de_questoes(len(questoes))
        request.session['num_questoes'] = objeto_atividade.get_numero_questoes()
        request.session['questoes'] = questoes
        request.session['id_atividade'] = atividade['id']
        request.session['nome_atividade'] = atividade['nome']
        request.session['contador'] = 0
        request.session['pontos_usuario'] = 0
        request.session['qtd_acertos'] = 0
        context['numero_de_questoes'] = objeto_atividade.get_numero_questoes()
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def respondendo(request, id):
    if request.session.has_key('usuario_corrente'):
        context = {}
        num_questoes = request.session['num_questoes']
        dados_questoes = json.dumps(request.session['questoes'])
        atividade = request.session['id_atividade']
        qtd_acertos = request.session['qtd_acertos']
        questoes = json.loads(dados_questoes)
        context['num_questoes'] = num_questoes
        context['atividade'] = atividade
        if questoes != []:
            eh_correta = False
            contador = request.session['contador']
            questao = questoes[0]
            alternativas = questao['alternativas']
            alternativas_list = alternativas.items
            resposta = questao['resposta']
            texto_resposta_correta = resposta['correta']
            tempo_resposta = formata_tempo_resposta(questao)
            context['tempo_resposta'] = tempo_resposta
            if request.method == 'POST':
                if questao['tipo'] == 'Múltipla Escolha':
                    form_me = Alternativas_Resposta(request.POST, my_choices=alternativas_list)
                    if form_me.is_valid():
                        context['pontuacao_questao'], context['contador'], context[
                            'pontos_usuario'], eh_correta = verifica_resposta_e_atualiza(form_me, alternativas,
                                                                                         texto_resposta_correta,
                                                                                         request, questao, context)
                elif questao['tipo'] == 'Verdadeiro ou Falso':
                    form_vf = Alternativas_Resposta(request.POST, my_choices=alternativas_list)
                    if form_vf.is_valid():
                        context['pontuacao_questao'], context['contador'], context[
                            'pontos_usuario'], eh_correta = verifica_resposta_e_atualiza(form_vf, alternativas,
                                                                                         texto_resposta_correta,
                                                                                         request, questao, context)
                elif questao['tipo'] == 'Lacunas':
                    form_l = Alternativas_Resposta(request.POST, my_choices=alternativas_list)
                    if form_l.is_valid():
                        context['pontuacao_questao'], context['contador'], context[
                            'pontos_usuario'], eh_correta = verifica_resposta_e_atualiza(form_l, alternativas,
                                                                                         texto_resposta_correta,
                                                                                         request, questao, context)
                context['questao'] = questao
                context['eh_correta'] = eh_correta
                context['texto_resposta_correta'] = texto_resposta_correta
                template_name = 'courses/verifica_resposta.html'
                return render(request, template_name, context)
            else:
                if contador == 0:
                    id_proprio = get_next_sequence_value('atividade')
                    pontuacao_geral_atividade = 0
                    usuario_corrente = request.session['usuario_corrente']
                    id_disciplina = request.session['id_disciplina']
                    nome_atividade = request.session['nome_atividade']
                    for questao_ in questoes:
                        pontuacao_geral_atividade += int(questao_['pontuacao'])
                    atividade_sessao = AtividadeSessao(id, id_proprio, nome_atividade, False,
                                                       datetime.now().strftime('%d/%m/%Y %H:%M'), 0, 0, num_questoes, 0,
                                                       pontuacao_geral_atividade)
                    request.session['qtd_tentativas'] = atividade_sessao.get_qtd_tentativas(id, usuario_corrente['id'],
                                                                                            int(id_disciplina))
                    dados_json = request.session['dados_json']
                    professor = dados_json['professor']
                    lista_alunos = dados_json['alunos']
                    alunos = []
                    for aluno in lista_alunos:
                        aluno = Usuario(aluno['nome'], aluno['email'])
                        alunos.append(aluno)
                    curso = Curso(dados_json['nome_disciplina'], Usuario(professor['nome'], professor['email']), alunos)
                    objeto_curso = get_objeto_curso_existente(curso)
                    objeto_usuario = verifica_usuarios_json(usuario_corrente['nome'], usuario_corrente['email'])
                    atividade_sessao.salvar(objeto_usuario, objeto_curso)
                    request.session['id_atividade_sessao'] = id_proprio
                if questao['tipo'] == 'Múltipla Escolha':
                    context['questao'] = questao
                    form_me = Alternativas_Resposta(my_choices=alternativas_list)
                    context['form_me'] = form_me
                elif questao['tipo'] == 'Verdadeiro ou Falso':
                    context['questao'] = questao
                    form_vf = Alternativas_Resposta(my_choices=alternativas_list)
                    context['form_vf'] = form_vf
                elif questao['tipo'] == 'Lacunas':
                    context['questao'] = questao
                    form_l = Alternativas_Resposta(my_choices=alternativas_list)
                    context['form_l'] = form_l
            context['pontos_usuario'] = request.session['pontos_usuario']
            request.session['contador'] = contador + 1
            context['contador'] = request.session['contador']
        if num_questoes != 0 and questoes == []:
            return resultado(request, id)
        template_name = 'courses/respondendo_quiz.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def resultado(request, id):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    context = {}
    num_questoes = request.session['num_questoes']
    qtd_acertos = request.session['qtd_acertos']
    perc_acertos = round((qtd_acertos / num_questoes) * 100, 2)
    context['perc_acertos'] = perc_acertos
    banco.disciplina_atividade_sessao.update_one({"id": int(request.session['id_atividade_sessao'])}, {'$set': {'perc_acertos': perc_acertos, 'concluida': True}})
    atividade_s = banco.disciplina_atividade_sessao.find_one({'id': int(request.session['id_atividade_sessao'])})
    questoes_atividade_sessao = banco.disciplina_atividade_sessao.find_one({'id': int(request.session['id_atividade_sessao'])}, {'questoes'})
    if request.session['qtd_tentativas'] == 1:
        premio = verificapremiacao(int(id), perc_acertos)
        banco.disciplina_atividade_sessao.update_one({"id": int(request.session['id_atividade_sessao'])},
                                          {'$set': {'premiacao': premio}})
        lista = recalcula_ranking(int(id))
        context['premio'] = premio
    context['atividade_s'] = atividade_s
    context['questoes_atividade_sessao'] = questoes_atividade_sessao['questoes']
    context['qtd_acertos'] = qtd_acertos
    context['num_questoes'] = num_questoes
    context['qtd_tentativas'] = request.session['qtd_tentativas']
    template_name = 'courses/resultado_quiz.html'
    return render(request, template_name, context)


def verifica_resposta_e_atualiza(form, alternativas, texto_resposta_correta, request, questao, context):
    questoes = request.session['questoes']
    eh_correta = False
    resposta_aluno = form.cleaned_data['Alternativas']
    if resposta_aluno != '':
        texto_resposta_aluno = alternativas[resposta_aluno]
    else:
        texto_resposta_aluno = ''
    questao_sessao = QuestaoSessao(questao['id'], questao['sentenca'], questao['feedback'],
                                   texto_resposta_correta, texto_resposta_aluno)
    questao_sessao.salvar(request.session['id_atividade_sessao'])
    if questao_sessao.acertou == True:
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        request.session['qtd_acertos'] = request.session['qtd_acertos'] + 1
        request.session['pontos_usuario'] = request.session['pontos_usuario'] + int(questao['pontuacao'])
        eh_correta = True
        banco.disciplina_atividade_sessao.update_one({"id": int(request.session['id_atividade_sessao'])},
                                          {'$set': {'qtd_acertos': request.session['qtd_acertos'],
                                                    'pontuacao_aluno': request.session['pontos_usuario']}})
    del questoes[0]
    request.session['questoes'] = questoes
    context['pontuacao_questao'] = questao['pontuacao']
    context['contador'] = request.session['contador']
    context['pontos_usuario'] = request.session['pontos_usuario']
    return context['pontuacao_questao'], context['contador'], context['pontos_usuario'], eh_correta


def verificapremiacao(id_atividade, perc_acertos_aluno):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    obj_atividade = banco.disciplina_atividade.find_one({'id': int(id_atividade)})
    ativ_ = Atividade(obj_atividade['id'], obj_atividade['nome'], obj_atividade['descricao'], obj_atividade['data_inicial'], obj_atividade['data_final'],
                           obj_atividade['exibicao_resp_corretas'], obj_atividade['aleatoria'], obj_atividade['perc_trof_ouro'], obj_atividade['perc_trof_prata'], obj_atividade['perc_trof_bronze'])
    perc_acertos_atividade_ouro = ativ_.get_requisito_trofeu_ouro()
    perc_acertos_atividade_prata = ativ_.get_requisito_trofeu_prata()
    perc_acertos_atividade_bronze = ativ_.get_requisito_trofeu_bronze()
    if perc_acertos_aluno >= perc_acertos_atividade_ouro:
        premiacao = 'Trofeu de Ouro'
    elif perc_acertos_aluno >= perc_acertos_atividade_prata:
        premiacao = 'Trofeu de Prata'
    elif perc_acertos_aluno >= perc_acertos_atividade_bronze:
        premiacao = 'Trofeu de Bronze'
    else:
        premiacao = 'Medalha de Participação'
    return premiacao


def formata_tempo_resposta(questao):
    if questao['tempo_resposta'] == '30 segundos':
        tempo_resposta = 30
    elif questao['tempo_resposta'] == '60 segundos':
        tempo_resposta = 60
    elif questao['tempo_resposta'] == '90 segundos':
        tempo_resposta = 90
    elif questao['tempo_resposta'] == 'Ilimitado':
        tempo_resposta = 'Ilimitado'
    return tempo_resposta


def estatisticas(request):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        id_disciplina = request.session['id_disciplina']
        usuario_corrente = request.session['usuario_corrente']
        atividades = banco.disciplina_atividade.find({'curso.id': id_disciplina})
        context = {'atividades': atividades}
        dados = get_dados_arquivo(request)
        professor = dados['professor']
        professor_dados = banco.disciplina.find_one({'id': int(id_disciplina), 'adm.email': professor['email']},
                                                       {'adm'})
        adm = professor_dados['adm']
        id_adm = adm['id']
        context['id_professor'] = id_adm
        context['usuario'] = usuario_corrente['id']
        template_name = 'courses/estatisticas.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def analise_questoes(request, id):
    context = {}
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        atividade = banco.disciplina_atividade.find_one({'id': int(id)})
        questoes_atividade = atividade['questoes']
        lista_de_questoes = []
        for questao in questoes_atividade:
            questao_estatistica = QuestaoEstatistica(questao['id'], questao['tipo'], questao['tempo_resposta'],
                                                     questao['pontuacao'], questao['nivel_dificuldade'],
                                                     questao['nivel_aprendizado'], questao['sentenca']);
            total_questoes_respondidas = banco.disciplina_atividade_sessao.count_documents(
                {'id_atividade': int(id), 'questoes.id': questao['id'], 'tentativa': 1})
            total_questoes_corretas = banco.disciplina_atividade_sessao.count_documents(
                {'id_atividade': int(id), 'tentativa': 1,
                 'questoes': {'$elemMatch': {'id': questao['id'], 'acertou': True}}
                 })
            if total_questoes_respondidas != 0:
                percentual_acertos_questao = round((total_questoes_corretas / total_questoes_respondidas) * 100, 2)
            else:
                percentual_acertos_questao = 0
            questao_estatistica.set_percentual(percentual_acertos_questao)
            lista_de_questoes.append(questao_estatistica.__dict__)
        context['atividade'] = atividade
        context['questoes'] = lista_de_questoes
        template_name = 'courses/analisequestoes.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def analise_alternativas(request, id_atividade, id_questao):
    context = {}
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        questao_selecionada = ''
        lista_alternativas = []
        atividade = banco.disciplina_atividade.find_one({'id': int(id_atividade)}, {'questoes', 'nome'})
        questoes_atividade = atividade['questoes']
        for questao in questoes_atividade:
            if questao['id'] == int(id_questao):
                questao_selecionada = questao
                alternativas = questao['alternativas']
        total_questoes_respondidas = banco.disciplina_atividade_sessao.count_documents(
            {'id_atividade': int(id_atividade), 'questoes.id': int(id_questao), 'tentativa': 1})
        qtd_primeira_alternativa = banco.disciplina_atividade_sessao.count_documents({'id_atividade': int(id_atividade),
                                                                           'questoes': {
                                                                               '$elemMatch': {'id': int(id_questao),
                                                                                              'resposta_aluno':
                                                                                                  alternativas[
                                                                                                      'primeira_alternativa']}},
                                                                           'tentativa': 1})
        qtd_segunda_alternativa = banco.disciplina_atividade_sessao.count_documents({'id_atividade': int(id_atividade),
                                                                          'questoes': {
                                                                              '$elemMatch': {'id': int(id_questao),
                                                                                             'resposta_aluno':
                                                                                                 alternativas[
                                                                                                     'segunda_alternativa']}},
                                                                          'tentativa': 1})
        if total_questoes_respondidas != 0:
            perc_primeira_alt = round((qtd_primeira_alternativa / total_questoes_respondidas) * 100, 2)
            perc_segunda_alt = round((qtd_segunda_alternativa / total_questoes_respondidas) * 100, 2)
            lista_alternativas.append((alternativas['primeira_alternativa'], perc_primeira_alt))
            lista_alternativas.append((alternativas['segunda_alternativa'], perc_segunda_alt))
        else:
            perc_primeira_alt = 0
            perc_segunda_alt = 0
            lista_alternativas.append((alternativas['primeira_alternativa'], perc_primeira_alt))
            lista_alternativas.append((alternativas['segunda_alternativa'], perc_segunda_alt))
        if questao_selecionada['tipo'] == 'Múltipla Escolha' or questao_selecionada['tipo'] == 'Lacunas':
            qtd_terceira_alternativa = banco.disciplina_atividade_sessao.count_documents({'id_atividade': int(id_atividade),
                                                                               'questoes': {
                                                                                   '$elemMatch': {'id': int(id_questao),
                                                                                                  'resposta_aluno':
                                                                                                      alternativas[
                                                                                                          'terceira_alternativa']}},
                                                                               'tentativa': 1})
            qtd_quarta_alternativa = banco.disciplina_atividade_sessao.count_documents({'id_atividade': int(id_atividade),
                                                                             'questoes': {
                                                                                 '$elemMatch': {'id': int(id_questao),
                                                                                                'resposta_aluno':
                                                                                                    alternativas[
                                                                                                        'quarta_alternativa']}},
                                                                             'tentativa': 1})
            qtd_quinta_alternativa = banco.disciplina_atividade_sessao.count_documents({'id_atividade': int(id_atividade),
                                                                                        'questoes': {
                                                                                            '$elemMatch': {'id': int(id_questao),'resposta_aluno':
                                                                                                alternativas[
                                                                                            'quinta_alternativa']}},
                                                                                            'tentativa': 1})
            if total_questoes_respondidas != 0:
                perc_terceira_alt = round((qtd_terceira_alternativa / total_questoes_respondidas) * 100, 2)
                perc_quarta_alt = round((qtd_quarta_alternativa / total_questoes_respondidas) * 100, 2)
                perc_quinta_alt = round((qtd_quinta_alternativa / total_questoes_respondidas) * 100, 2)
                lista_alternativas.append((alternativas['terceira_alternativa'], perc_terceira_alt))
                lista_alternativas.append((alternativas['quarta_alternativa'], perc_quarta_alt))
                lista_alternativas.append((alternativas['quinta_alternativa'], perc_quinta_alt))
            else:
                perc_terceira_alt = 0
                perc_quarta_alt = 0
                perc_quinta_alt = 0
                lista_alternativas.append((alternativas['terceira_alternativa'], perc_terceira_alt))
                lista_alternativas.append((alternativas['quarta_alternativa'], perc_quarta_alt))
                lista_alternativas.append((alternativas['quinta_alternativa'], perc_quinta_alt))
        context['atividade'] = atividade
        context['questao'] = questao_selecionada
        print('Alternativa | Percentual')
        print(lista_alternativas)
        context['alternativas'] = lista_alternativas
        template_name = 'courses/analisealternativas.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def meuperfil(request):
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        context = {}
        usuario = request.session['usuario_corrente']
        id_disciplina = request.session['id_disciplina']
        dados_usuario = banco.disciplina_usuario.find_one({'email': usuario['email']})
        if dados_usuario == None:
            dados = get_dados_arquivo(request)
            request.session['curso'] = dados['nome_disciplina']
            return sair(request)
        context['nome_usuario'] = dados_usuario['nome']
        context['email_usuario'] = dados_usuario['email']
        qtd_trofeus = banco.disciplina_atividade_sessao.count_documents(
            {'usuario.id': int(usuario['id']), 'curso.id': int(id_disciplina), 'tentativa': 1})
        if qtd_trofeus > 0:
            atividades = banco.disciplina_atividade_sessao.find(
                {'usuario.id': int(dados_usuario['id']), 'curso.id': int(id_disciplina), 'tentativa': 1})
            context['atividades'] = atividades
        context['qtd_trofeus'] = qtd_trofeus
        template_name = 'courses/meuperfil.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def ranking(request, id):
    context = {}
    if request.session.has_key('usuario_corrente'):
        client = MongoClient("localhost", 27017)
        banco = client.quiz
        atividade = banco.disciplina_atividade.find_one({'id': int(id)})
        lista = recalcula_ranking(int(id))
        context['atividade'] = atividade
        context['ranking'] = lista
        template_name = 'courses/ranking.html'
        return render(request, template_name, context)
    else:
        dados = get_dados_arquivo(request)
        request.session['curso'] = dados['nome_disciplina']
        return sair(request)


def recalcula_ranking(id):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    atividades_sessao = banco.disciplina_atividade_sessao.find({'id_atividade': int(id), 'tentativa': 1})
    atividades_sessao.sort([('pontuacao_aluno', -1)]).limit(10)
    posicao = 1
    ranking = Ranking()
    for atividade_sessao in atividades_sessao:
        usuario = atividade_sessao['usuario']
        usuario_nome = usuario['nome']
        pontos = atividade_sessao['pontuacao_aluno']
        premio = atividade_sessao['premiacao']
        item_ranking = ItemRanking(posicao, usuario_nome, pontos, premio)
        item = item_ranking.__dict__
        ranking.add_item_ranking(item)
        posicao += 1
    lista = ranking.get_lista()
    ranking.salvar(int(id), lista)
    return lista


def home(request):
    context = {}
    dados = get_dados_arquivo(request)
    if request.session.has_key('usuario_corrente'):
        continua_aqui = 1
    else:
        request.session['curso'] = dados['nome_disciplina']
        return login(request)
    dados = request.session['dados_json']
    context['disciplina'] = dados['nome_disciplina']
    template_name = 'courses/home.html'
    return render(request, template_name, context)


def login(request):
    context = {}
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email_usuario_corrente = form.cleaned_data['email']
            id_nome_usuario = busca_aluno_entre_usuarios_no_bd(email_usuario_corrente)
            if id_nome_usuario != None:
                encontrado = busca_aluno_no_curso_no_bd(request.session['curso'], id_nome_usuario['id'])
                eh_professor = verifica_se_usuario_eh_professor(request.session['curso'], id_nome_usuario['id'])
                if encontrado != 0 or eh_professor != 0:
                    id = id_nome_usuario['id']
                    usuario = Usuario(id_nome_usuario['nome'], email_usuario_corrente)
                    objeto_usuario = get_objeto_usuario(usuario, id)
                    usuario.set_ID(id)
                    request.session['usuario_corrente'] = objeto_usuario
                    return home(request)
                else:
                    context['msg'] = 'Usuário não encontrado na lista de alunos da disciplina'
            else:
                context['msg'] = 'Usuário não encontrado na lista de usuários existentes'
        form = Login()
    else:
        form = Login()
    context['form'] = form
    template_name = 'courses/login.html'
    return render(request, template_name, context)


def sair(request):
    request.session.flush()
    dados = get_dados_arquivo(request)
    request.session['curso'] = dados['nome_disciplina']
    return login(request)


def get_dados_arquivo(request):
    arquivo = open('quizsophia/courses/templates/arquivo/dados.json', 'r')
    dados = json.load(arquivo)
    lista_alunos = dados['alunos']
    dados_professor = dados['professor']
    alunos_curso = []
    for aluno in lista_alunos:
        obj_aluno = verifica_usuarios_json(aluno['nome'], aluno['email'])
        aluno_curso = Usuario(aluno['nome'], aluno['email'])
        aluno_curso.set_ID(obj_aluno['id'])
        alunos_curso.append(aluno_curso)
    curso = Curso(dados['nome_disciplina'], Usuario(dados_professor['nome'], dados_professor['email']), alunos_curso)
    inicializa_valores_teste(curso)
    request.session['id_disciplina'] = curso.get_ID()
    request.session['professor'] = dados_professor
    request.session['dados_json'] = dados
    request.session.Modified = True
    return dados


def inicializa_valores_teste(curso):
    verifica_curso_e_adiciona(curso, curso.get_adm())
    id_curso = busca_curso_no_bd(curso)
    curso.set_ID(id_curso['id'])
    verifica_alunos_e_adiciona(curso)


def verifica_curso_e_adiciona(curso_recebido_ws, adm):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    if busca_curso_no_bd(curso_recebido_ws) == None:
        obj_id_curso = get_next_sequence_value("curso")
        objeto_adm = verifica_usuarios_json(adm.get_nome(), adm.get_email())
        objeto_curso = get_objeto_curso(curso_recebido_ws, objeto_adm, obj_id_curso)
        banco.disciplina.insert_one(objeto_curso)
    else:
        objeto_curso = get_objeto_curso_existente(curso_recebido_ws)
    return objeto_curso


def verifica_alunos_e_adiciona(curso):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    lista_alunos = curso.get_alunos()
    for aluno in lista_alunos:
        objeto_aluno = verifica_usuarios_json(aluno.get_nome(), aluno.get_email())
        id_aluno = objeto_aluno['id']
        if busca_aluno_no_curso_no_bd(curso.get_nome(), id_aluno) == 0:
            banco.disciplina.update_one({"id": curso.get_ID()}, {"$push": {"alunos": objeto_aluno}})


def busca_aluno_no_curso_no_bd(nome_curso_atual, id_usuario_selecionado):
    encontrado = 0
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    documento_retornado = banco.disciplina.find_one({"nome": nome_curso_atual}, {'alunos'})
    for aluno in documento_retornado['alunos']:
        if id_usuario_selecionado == aluno['id']:
            encontrado = 1
    return encontrado


def verifica_se_usuario_eh_professor(nome_curso_atual, id_usuario_selecionado):
    eh_professor = 0
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    documento_retornado = banco.disciplina.find_one({"nome": nome_curso_atual}, {'adm'})
    adm = documento_retornado['adm']
    if id_usuario_selecionado == adm['id']:
        eh_professor = 1
    return eh_professor


def busca_curso_no_bd(curso_atual):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    documento_retornado = banco.disciplina.find_one({"nome": curso_atual.get_nome()}, {'id'})
    return documento_retornado


def busca_aluno_entre_usuarios_no_bd(usuario_selecionado):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    documento_retornado = banco.disciplina_usuario.find_one({"email": usuario_selecionado}, {'id', 'nome'})
    return documento_retornado


def verifica_usuarios_json(nome, email):
    client = MongoClient("localhost", 27017)
    banco = client.quiz
    id_nome_usuario = busca_aluno_entre_usuarios_no_bd(email)
    if (id_nome_usuario != None):
        id = id_nome_usuario['id']
        usuario = Usuario(nome, email)
        objeto_usuario = get_objeto_usuario(usuario, id)
        usuario.set_ID(id)
    else:
        id = get_next_sequence_value('usuario')
        usuario = Usuario(nome, email)
        usuario.set_ID(id)
        objeto_usuario = get_objeto_usuario(usuario, id)
        banco.disciplina_usuario.insert_one(objeto_usuario)
    return objeto_usuario