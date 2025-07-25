# Generated by Django 5.2 on 2025-06-27 12:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competicoes', '0009_resultadokata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arbitro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Árbitro',
                'verbose_name_plural': 'Árbitros',
            },
        ),
        migrations.AlterModelOptions(
            name='competicao',
            options={'ordering': ['-data_inicio'], 'verbose_name': 'Competição', 'verbose_name_plural': 'Competições'},
        ),
        migrations.AddField(
            model_name='competicao',
            name='data_atualizacao',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='competicao',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_data_limite',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_desconto',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_mensagem',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_mostrar_vagas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_mostrar_valor',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_pagamento_boleto',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_pagamento_cartao',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_pagamento_pix',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_status',
            field=models.CharField(choices=[('abertas', 'Abertas'), ('fechadas', 'Fechadas'), ('em-breve', 'Em breve')], default='abertas', max_length=10),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_taxa',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='competicao',
            name='inscricoes_valor',
            field=models.DecimalField(decimal_places=2, default=120.0, max_digits=10),
        ),
        migrations.RemoveField(
            model_name='competicao',
            name='arbitros',
        ),
        migrations.AlterField(
            model_name='competicao',
            name='data_inicio',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='competicao',
            name='horario',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='competicao',
            name='status',
            field=models.CharField(choices=[('Ativa', 'Ativa'), ('Finalizada', 'Finalizada'), ('Em breve', 'Em breve')], default='Ativa', max_length=20),
        ),
        migrations.AddField(
            model_name='competicao',
            name='arbitros',
            field=models.ManyToManyField(blank=True, related_name='competicoes', to='competicoes.arbitro'),
        ),
    ]
