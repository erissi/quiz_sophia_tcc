# Generated by Django 2.2.4 on 2020-02-26 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20200221_1530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questao',
            old_name='nivel_de_dificuldade',
            new_name='nivel_dificuldade',
        ),
        migrations.RemoveField(
            model_name='questao',
            name='explicacao_resposta',
        ),
        migrations.RemoveField(
            model_name='questao',
            name='pergunta',
        ),
        migrations.RemoveField(
            model_name='questao',
            name='resposta',
        ),
        migrations.AddField(
            model_name='atividade',
            name='data_final',
            field=models.DateField(default=']01.01.01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividade',
            name='data_inicial',
            field=models.DateField(default='01.01.01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questao',
            name='feedback',
            field=models.TextField(default='Vazio', verbose_name='Feedback'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questao',
            name='nivel_aprendizado',
            field=models.CharField(default='1', max_length=100, verbose_name='Nivel de Aprendizado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questao',
            name='sentenca',
            field=models.TextField(default='Vazio', verbose_name='Sentenca'),
            preserve_default=False,
        ),
    ]
