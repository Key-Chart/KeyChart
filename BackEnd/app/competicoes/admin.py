from django.contrib import admin
from .models import Competicao, Categoria, Academia, Arbitro, ResultadoKata

@admin.register(Arbitro)
class ArbitroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_criacao')
    search_fields = ('nome', 'email')
    list_filter = ('data_criacao',)
    ordering = ('nome',)

@admin.register(Competicao)
class CompeticaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modalidade', 'data_inicio', 'local', 'status', 'inscricoes_abertas')
    search_fields = ('nome', 'local', 'modalidade')
    list_filter = ('status', 'modalidade', 'inscricoes_abertas', 'data_inicio')
    filter_horizontal = ('arbitros',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'modalidade', 'data_inicio', 'horario', 'local', 'regras_especificas', 'status')
        }),
        ('Árbitros', {
            'fields': ('arbitros',)
        }),
        ('Configurações de Inscrições', {
            'fields': ('inscricoes_abertas', 'inscricoes_status', 'inscricoes_data_limite', 
                      'inscricoes_valor', 'inscricoes_taxa', 'inscricoes_desconto')
        }),
        ('Métodos de Pagamento', {
            'fields': ('inscricoes_pagamento_pix', 'inscricoes_pagamento_cartao', 'inscricoes_pagamento_boleto')
        }),
        ('Configurações de Exibição', {
            'fields': ('inscricoes_mostrar_valor', 'inscricoes_mostrar_vagas', 'inscricoes_mensagem')
        }),
    )
    readonly_fields = ('data_criacao', 'data_atualizacao')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'competicao', 'sexo', 'tipo')
    search_fields = ('nome', 'competicao__nome')
    list_filter = ('sexo', 'tipo', 'competicao')

@admin.register(Academia)
class AcademiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado', 'competicao')
    search_fields = ('nome', 'cidade')
    list_filter = ('estado', 'competicao')

@admin.register(ResultadoKata)
class ResultadoKataAdmin(admin.ModelAdmin):
    list_display = ('atleta', 'categoria', 'competicao', 'total', 'data_criacao')
    search_fields = ('atleta__nome', 'categoria__nome', 'competicao__nome')
    list_filter = ('competicao', 'categoria', 'data_criacao')
    readonly_fields = ('total', 'data_criacao', 'data_atualizacao')
