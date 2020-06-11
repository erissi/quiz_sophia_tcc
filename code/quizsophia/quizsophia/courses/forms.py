from django import forms
from django.forms import SelectDateWidget, renderers, renderers

ALTERNATIVAS = [('Sim', 'Sim'), ('Não', 'Não'), ]
EXIBICAO_RESP_INICIO = [('A cada questão respondida', 'A cada questão respondida'),
                        ('Ao final da atividade', 'Somente ao final da atividade'), ]

VF = [('Verdadeiro', 'Verdadeiro'), ('Falso', 'Falso'), ]

ALTERNATIVA_CORRETA = [('1° Alternativa', '1° Alternativa'), ('2° Alternativa', '2° Alternativa'), ('3° Alternativa', '3° Alternativa'), ('4° Alternativa', '4° Alternativa'), ('5° Alternativa', '5° Alternativa'),]
VF_CORRETA = [('Verdadeiro', 'Verdadeiro'), ('Falso', 'Falso'),]

TIPO_ = (
        ('Lacunas', 'Lacunas'),
        ('Múltipla Escolha', 'Múltipla Escolha'),
        ('Verdadeiro ou Falso', 'Verdadeiro ou Falso'),
)

TEMPO_ = (
        ('30 segundos', '30 segundos'),
        ('60 segundos', '60 segundos (1 minuto)'),
        ('90 segundos', '90 segundos (1 minuto  e 30 segundos)'),
        ('Ilimitado', 'Ilimitado'),
)

PONTUACAO_ = (
        ('10', '10 pontos'),
        ('20', '20 pontos'),
        ('30', '30 pontos'),
)

NIVEL_DIFICULDADE = (
        ('Fácil', 'Fácil'),
        ('Moderado', 'Moderado'),
        ('Difícil', 'Difícil'),
)

NIVEL_APRENDIZADO = (
        ('Recordação', 'Recordação'),
        ('Compreensão', 'Compreensão'),
        ('Aplicação', 'Aplicação'),
        ('Análise', 'Análise'),
        ('Sintese', 'Sintese'),
        ('Criação', 'Criação'),
)

VISIBILIDADE = [
        ('Pública', 'Pública'),
        ('Privada', 'Privada'),
]


class CriarAtividade(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, required=True)
    descricao = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={"rows": 5, "cols": 50}), required=True)
    aleatoria = forms.ChoiceField(label='Questões aleatórias?', widget=forms.RadioSelect, choices=ALTERNATIVAS, required=True)
    exibicao_resp_corretas = forms.ChoiceField(label='Mostrar respostas corretas', widget=forms.RadioSelect,
                                               choices=EXIBICAO_RESP_INICIO, required=True)
    data_inicial = forms.DateField(widget=SelectDateWidget(empty_label=("Ano", "Mês", "Dia")), required=True)
    data_final = forms.DateField(widget=SelectDateWidget(empty_label=("Ano", "Mês", "Dia")), required=True)
    # premiacao
    perc_trof_ouro = forms.IntegerField(min_value=1, max_value=100, label='Percentual para o Troféu de Ouro', required=True)
    perc_trof_prata = forms.IntegerField(min_value=1, max_value=100, label='Percentual para o Troféu de Prata', required=True)
    perc_trof_bronze = forms.IntegerField(min_value=1, max_value=100, label='Percentual para o Troféu de Bronze', required=True)


class EditarAtividade(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, required=True)
    descricao = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={"rows": 5, "cols": 80}), required=True)
    aleatoria = forms.ChoiceField(label='Questões aleatórias?', widget=forms.RadioSelect, choices=ALTERNATIVAS, required=True)
    exibicao_resp_corretas = forms.ChoiceField(label='Mostrar respostas corretas', widget=forms.RadioSelect,
                                               choices=EXIBICAO_RESP_INICIO, required=True)
    data_inicial = forms.DateField(widget=SelectDateWidget(empty_label=("Ano", "Mês", "Dia")), required=True)
    data_final = forms.DateField(widget=SelectDateWidget(empty_label=("Ano", "Mês", "Dia")), required=True)
    # premiacao
    perc_trof_ouro = forms.IntegerField(min_value=1, max_value=100, label='Percentual para o Troféu de Ouro', required=True)
    perc_trof_prata = forms.IntegerField(min_value=1, max_value=100, label='Percentual para o Troféu de Prata', required=True)
    perc_trof_bronze = forms.IntegerField(min_value=1, max_value=100, label='Percentual para o Troféu de Bronze', required=True)


class CriarQuestao(forms.Form):
    nivel_dificuldade = forms.ChoiceField(label='Nível de Dificuldade ', widget=forms.Select, choices=NIVEL_DIFICULDADE, required=True)
    nivel_aprendizado = forms.ChoiceField(label='Nível de Aprendizado ', widget=forms.Select, choices=NIVEL_APRENDIZADO, required=True)
    tempo_resposta = forms.ChoiceField(label='Tempo para responder:  ', widget=forms.Select, choices=TEMPO_, required=True)
    pontuacao = forms.ChoiceField(label='Pontuação ', widget=forms.Select, choices=PONTUACAO_, required=True)
    tipo = forms.ChoiceField(label='Tipo', widget=forms.Select(attrs={'onchange': 'alternar_divs()'}), choices=TIPO_, required=True)
    sentenca = forms.CharField(label='Sentença', widget=forms.Textarea(attrs={"rows": 5, "cols": 50}), required=True)
    feedback = forms.CharField(label='Explicação da Resposta ', widget=forms.Textarea(attrs={"rows": 5, "cols": 50}), required=True)


class Criar_Alternativa_ME(forms.Form):
    primeira_alternativa = forms.CharField(label='1° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}), required=False)
    segunda_alternativa = forms.CharField(label='2° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}), required=False)
    terceira_alternativa = forms.CharField(label='3° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}), required=False)
    quarta_alternativa = forms.CharField(label='4° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}), required=False)
    quinta_alternativa = forms.CharField(label='5° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}), required=False)
    correta = forms.ChoiceField(label='Alternativa Correta:', widget=forms.Select, choices=ALTERNATIVA_CORRETA, required=False)


class Criar_Alternativa_L(forms.Form):
    primeira_alternativa_l = forms.CharField(label='1° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}),
                                           help_text='Exemplo: "palavra 1, palavra 2, palavra 3, palavra 4"', required=False)
    segunda_alternativa_l = forms.CharField(label='2° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}),
                                  help_text='Exemplo: "palavra 4, palavra 3, palavra 2, palavra 1"', required=False)
    terceira_alternativa_l = forms.CharField(label='3° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}),
                                  help_text='Exemplo: "palavra 1, palavra 3, palavra 4, palavra 2"', required=False)
    quarta_alternativa_l = forms.CharField(label='4° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}),
                                  help_text='Exemplo: "palavra 1, palavra 2, palavra 4, palavra 3"', required=False)
    quinta_alternativa_l = forms.CharField(label='5° Alternativa', widget=forms.Textarea(attrs={"rows": 1, "cols": 50}),
                                           help_text='Exemplo: "palavra 1, palavra 2, palavra 4, palavra 3"',
                                           required=False)
    correta_l = forms.ChoiceField(label='Alternativa Correta:', widget=forms.Select, choices=ALTERNATIVA_CORRETA, required=False)


class Criar_Alternativa_VF(forms.Form):
    correta_vf = forms.ChoiceField(label='Resposta Correta', widget=forms.RadioSelect, choices=VF, required=False)


class EditarQuestao(forms.Form):
    nivel_dificuldade = forms.ChoiceField(label='Nível de Dificuldade ', widget=forms.Select, choices=NIVEL_DIFICULDADE, required=True)
    nivel_aprendizado = forms.ChoiceField(label='Nível de Aprendizado ', widget=forms.Select, choices=NIVEL_APRENDIZADO, required=True)
    tempo_resposta = forms.ChoiceField(label='Tempo para responder:  ', widget=forms.Select, choices=TEMPO_, required=True)
    pontuacao = forms.ChoiceField(label='Pontuação ', widget=forms.Select, choices=PONTUACAO_, required=True)
    tipo = forms.ChoiceField(label='Tipo ', widget=forms.Select, disabled=True,  required=False, choices=TIPO_)
    sentenca = forms.CharField(label='Sentença ', widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), required=True)
    feedback = forms.CharField(label='Explicação da Resposta ', widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), required=True)


class CriarQuestaoAtividade(forms.Form):
    nivel_dificuldade = forms.ChoiceField(label='Nível de Dificuldade', widget=forms.Select, choices=NIVEL_DIFICULDADE, required=True)
    visibilidade = forms.ChoiceField(label='Visibilidade', widget=forms.RadioSelect, choices=VISIBILIDADE, required=True)
    nivel_aprendizado = forms.ChoiceField(label='Nível de Aprendizado', widget=forms.Select, choices=NIVEL_APRENDIZADO, required=True)
    tempo_resposta = forms.ChoiceField(label='Tempo para responder: ', widget=forms.Select, choices=TEMPO_, required=True)
    pontuacao = forms.ChoiceField(label='Pontuação', widget=forms.Select, choices=PONTUACAO_, required=True)
    tipo = forms.ChoiceField(label='Tipo', widget=forms.Select(attrs={'onchange': 'alternar_divs()'}), choices=TIPO_, required=True)
    sentenca = forms.CharField(label='Sentença', widget=forms.Textarea(attrs={"rows": 5, "cols": 50}), required=True)
    feedback = forms.CharField(label='Explicação da Resposta', widget=forms.Textarea(attrs={"rows": 5, "cols": 50}), required=True)


class EditarQuestaoAtividade(forms.Form):
    nivel_dificuldade = forms.ChoiceField(label='Nível de Dificuldade ', widget=forms.Select, choices=NIVEL_DIFICULDADE, required=True)
    visibilidade = forms.ChoiceField(label='Visibilidade ', widget=forms.RadioSelect, choices=VISIBILIDADE, required=True)
    nivel_aprendizado = forms.ChoiceField(label='Nível de Aprendizado ', widget=forms.Select, choices=NIVEL_APRENDIZADO, required=True)
    tempo_resposta = forms.ChoiceField(label='Tempo para responder:  ', widget=forms.Select, choices=TEMPO_, required=True)
    pontuacao = forms.ChoiceField(label='Pontuação ', widget=forms.Select, choices=PONTUACAO_, required=True)
    tipo = forms.ChoiceField(label='Tipo ', widget=forms.Select, choices=TIPO_, disabled=True, required=False)
    sentenca = forms.CharField(label='Sentença ', widget=forms.Textarea(attrs={"rows": 5, "cols": 50}), required=True)
    feedback = forms.CharField(label='Explicação da Resposta', widget=forms.Textarea(attrs={"rows": 5, "cols": 50}), required=True)


class RespondendoVF(forms.Form):
    alternativas = forms.ChoiceField(widget=forms.RadioSelect, required=False)


class RespondendoLacunas(forms.Form):
    alternativas = forms.ChoiceField(label='Alternativas', widget=forms.RadioSelect, required=False)


class RespondendoME(forms.Form):
    alternativas = forms.ChoiceField(label='Alternativas', widget=forms.RadioSelect, required=False)


class Login(forms.Form):
    email = forms.EmailField(label='E-mail', required=True)


class Alternativas_Resposta(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        choices = kwargs.pop('my_choices')
        super(Alternativas_Resposta, self).__init__(*args, **kwargs)
        self.fields["Alternativas"] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=False)