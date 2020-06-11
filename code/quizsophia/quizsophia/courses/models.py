from django.db import models
from djongo import models


# not usable
class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )


# not usable
class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    #slug = models.SlugField(name=name, max_length=120)
    description = models.TextField('Descrição', blank=True)
    #start_date = models.DateField('Data de Início', null=True, blank=True)
    #image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True)

    #created_at = models.DateTimeField('Criado em', auto_now_add=True)
    #updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        #verbose_name_plural = 'Cursos'
        ordering = ['name']





class Usuario(models.Model):
    id = models.IntegerField('id', primary_key=True)
    nome = models.CharField('Nome', max_length=100)
    email = models.CharField('Email', max_length=100)

class Curso(models.Model):
    nome = models.CharField('Nome', max_length=100)
    adm = models.CharField('Adm', max_length=100)
    alunos = models.ArrayModelField(model_container=Usuario,)

class Atividade(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    aleatoria = models.CharField('Questões aleatórias?', max_length=100)
    exibicao_resp_corretas = models.CharField('Respostas Corretas:', max_length=100)
    data_inicial = models.DateField()
    data_final = models.DateField()
    perc_trof_bronze = models.IntegerField('Troféu de Bronze:')
    perc_trof_prata = models.IntegerField('Troféu de Prata:')
    perc_trof_ouro = models.IntegerField('Troféu de Ouro:')
    #autor = models.CharField('Autor:', max_length=100)
    #turma = models.CharField('Turma:', max_length=100)
    #autor = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #curso = models.OneToOneField(Curso, on_delete=models.CASCADE)
    #questoes = models.ListField('Questao')


class Questao_Verdadeiro_Falso(models.Model):
    tipo = models.CharField('Tipo', max_length=100)
    pergunta = models.TextField('Pergunta')
    resposta = models.TextField('Resposta')
    pontuacao = models.CharField('Pontuação', max_length=100)
    visibilidade = models.CharField('Visibilidade', max_length=100)
    nivel_de_dificuldade = models.CharField('Nivel de Dificuldade', max_length=100)
    tempo_resposta = models.CharField('Tempo de Resposta', max_length=100)
    explicacao_resposta = models.TextField('Explicação da Resposta', blank=True)


class Questao_Multipla_Escolha(models.Model):
    tipo = models.CharField('Tipo', max_length=100)
    pergunta = models.TextField('Pergunta')
    resposta = models.TextField('Resposta')
    pontuacao = models.IntegerField('Pontuação')
    visibilidade = models.CharField('Visibilidade', max_length=100)
    nivel_de_dificuldade = models.CharField('Nivel de Dificuldade', max_length=100)
    tempo_resposta = models.CharField('Tempo de Resposta', max_length=100)
    explicacao_resposta = models.TextField('Explicação da Resposta', blank=True)


class Questao(models.Model):
    TIPO_ = (
        ('L', 'Lacunas'),
        ('ME', 'Múltipla Escolha'),
        ('VF', 'Verdadeiro ou Falso'),
    )
    tipo = models.CharField('Tipo', max_length=100, choices = TIPO_)
    sentenca = models.TextField('Sentenca')
    feedback = models.TextField('Feedback')
    #resposta = models.ListField('Resposta')
    #resposta = models.ListCharField()
    pontuacao = models.CharField('Pontuação', max_length=100)
    visibilidade = models.CharField('Visibilidade', max_length=100)
    nivel_dificuldade = models.CharField('Nivel de Dificuldade', max_length=100)
    tempo_resposta = models.CharField('Tempo de Resposta', max_length=100)
    #explicacao_resposta = models.TextField('Explicação da Resposta', blank=True)
    nivel_aprendizado = models.CharField('Nivel de Aprendizado', max_length=100)
    #autor = models.CharField('Autor:', max_length=100)