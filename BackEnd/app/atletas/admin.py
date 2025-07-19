from django.contrib import admin
from .models import Atleta, CertificadoAtleta, EstatisticaAtleta, HistoricoCompeticao

@admin.register(Atleta)
class AtletaAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'email', 'faixa', 'data_inscricao']
    list_filter = ['faixa', 'data_inscricao', 'sexo', 'estado']
    search_fields = ['nome_completo', 'cpf', 'email']
    readonly_fields = ['data_inscricao']

@admin.register(CertificadoAtleta)
class CertificadoAtletaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'atleta', 'data_emissao', 'status']
    list_filter = ['status', 'data_emissao']
    search_fields = ['titulo', 'atleta__nome']

@admin.register(EstatisticaAtleta)
class EstatisticaAtletaAdmin(admin.ModelAdmin):
    list_display = ['atleta', 'total_lutas', 'vitorias', 'derrotas', 'total_medalhas']
    search_fields = ['atleta__nome']
    readonly_fields = ['data_atualizacao']

@admin.register(HistoricoCompeticao)
class HistoricoCompeticaoAdmin(admin.ModelAdmin):
    list_display = ['atleta', 'competicao', 'data_participacao', 'resultado']
    list_filter = ['resultado', 'data_participacao']
    search_fields = ['atleta__nome_completo', 'competicao__nome']
