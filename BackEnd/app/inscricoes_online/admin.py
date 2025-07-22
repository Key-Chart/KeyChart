from django.contrib import admin
from .models import InscricaoOnline, LogInscricao

@admin.register(InscricaoOnline)
class InscricaoOnlineAdmin(admin.ModelAdmin):
    list_display = (
        'numero_inscricao', 'nome_completo', 'competicao', 'categoria', 
        'status', 'valor_inscricao', 'data_inscricao'
    )
    list_filter = (
        'status', 'competicao', 'categoria', 'forma_pagamento', 
        'faixa', 'sexo', 'data_inscricao'
    )
    search_fields = (
        'numero_inscricao', 'nome_completo', 'email', 'telefone', 
        'academia_nome', 'cpf'
    )
    readonly_fields = (
        'uuid', 'numero_inscricao', 'senha_atleta', 'data_inscricao', 
        'data_atualizacao', 'ip_inscricao'
    )
    
    fieldsets = (
        ('Identificação', {
            'fields': ('uuid', 'numero_inscricao', 'status')
        }),
        ('Competição', {
            'fields': ('competicao', 'categoria', 'academia')
        }),
        ('Dados Pessoais', {
            'fields': (
                'nome_completo', 'data_nascimento', 'sexo', 'cpf', 'rg',
                'email', 'telefone', 'cidade', 'estado'
            )
        }),
        ('Dados Esportivos', {
            'fields': ('faixa', 'peso', 'altura', 'foto')
        }),
        ('Academia', {
            'fields': ('academia_nome', 'academia_cidade', 'academia_estado')
        }),
        ('Pagamento', {
            'fields': ('forma_pagamento', 'valor_inscricao')
        }),
        ('Acesso do Atleta', {
            'fields': ('senha_atleta', 'senha_enviada')
        }),
        ('Metadados', {
            'fields': ('data_inscricao', 'data_atualizacao', 'ip_inscricao'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'competicao', 'categoria', 'academia'
        )
    
    actions = ['marcar_como_pago', 'marcar_como_confirmado', 'reenviar_email']
    
    def marcar_como_pago(self, request, queryset):
        updated = queryset.update(status='pago')
        self.message_user(request, f'{updated} inscrições marcadas como pagas.')
    marcar_como_pago.short_description = "Marcar como pago"
    
    def marcar_como_confirmado(self, request, queryset):
        updated = queryset.update(status='confirmado')
        self.message_user(request, f'{updated} inscrições confirmadas.')
    marcar_como_confirmado.short_description = "Confirmar inscrições"
    
    def reenviar_email(self, request, queryset):
        # Implementar reenvio de email
        count = 0
        for inscricao in queryset:
            # Chamar função de envio de email
            count += 1
        self.message_user(request, f'Email reenviado para {count} inscrições.')
    reenviar_email.short_description = "Reenviar email de confirmação"


@admin.register(LogInscricao)
class LogInscricaoAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'acao', 'data', 'ip')
    list_filter = ('acao', 'data')
    search_fields = ('inscricao__nome_completo', 'inscricao__numero_inscricao', 'acao', 'descricao')
    readonly_fields = ('inscricao', 'acao', 'descricao', 'data', 'ip')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
