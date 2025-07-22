from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    AtletaUser, SessaoAtleta, NotificacaoAtleta, 
    PreferenciaAtleta, LogAtividadeAtleta
)


@admin.register(AtletaUser)
class AtletaUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome_completo', 'is_active', 'data_criacao', 'ultimo_acesso', 'get_inscricoes_count')
    list_filter = ('is_active', 'data_criacao', 'ultimo_acesso', 'email_verificado', 'primeiro_acesso')
    search_fields = ('email', 'nome_completo', 'telefone')
    readonly_fields = ('uuid', 'data_criacao', 'data_atualizacao', 'ultimo_acesso')
    
    fieldsets = (
        (None, {
            'fields': ('uuid', 'email', 'password')
        }),
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'telefone', 'inscricao_origem')
        }),
        ('Status', {
            'fields': ('is_active', 'email_verificado', 'primeiro_acesso'),
        }),
        ('Datas Importantes', {
            'fields': ('ultimo_acesso', 'data_criacao', 'data_atualizacao'),
        }),
    )
    
    def get_inscricoes_count(self, obj):
        from app.inscricoes_online.models import InscricaoOnline
        count = InscricaoOnline.objects.filter(email=obj.email).count()
        if count > 0:
            url = reverse('admin:inscricoes_online_inscricaoonline_changelist') + f'?email={obj.email}'
            return format_html('<a href="{}">{} inscrições</a>', url, count)
        return '0 inscrições'
    get_inscricoes_count.short_description = 'Inscrições'
    
    def has_delete_permission(self, request, obj=None):
        # Só permite deletar se não tiver inscrições
        if obj:
            from app.inscricoes_online.models import InscricaoOnline
            return not InscricaoOnline.objects.filter(email=obj.email).exists()
        return True


@admin.register(SessaoAtleta)
class SessaoAtletaAdmin(admin.ModelAdmin):
    list_display = ('atleta', 'ip_address', 'user_agent_info', 'data_inicio', 'data_ultima_atividade', 'is_active')
    list_filter = ('data_inicio', 'data_ultima_atividade', 'ativa')
    search_fields = ('atleta__email', 'ip_address')
    readonly_fields = ('session_key', 'data_inicio', 'data_ultima_atividade')
    
    def user_agent_info(self, obj):
        return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
    user_agent_info.short_description = 'User Agent'
    
    def is_active(self, obj):
        icon = '✅' if obj.ativa else '❌'
        return format_html(f'{icon} {"Ativa" if obj.ativa else "Inativa"}')
    is_active.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Sessões são criadas automaticamente


@admin.register(NotificacaoAtleta)
class NotificacaoAtletaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'atleta', 'tipo', 'lida', 'data_criacao', 'get_preview')
    list_filter = ('tipo', 'lida', 'prioridade', 'data_criacao')
    search_fields = ('titulo', 'mensagem', 'atleta__email')
    readonly_fields = ('data_criacao', 'data_leitura')
    
    fieldsets = (
        (None, {
            'fields': ('atleta', 'tipo', 'titulo', 'mensagem', 'prioridade')
        }),
        ('Status', {
            'fields': ('lida', 'data_leitura', 'data_criacao', 'expirar_em'),
        }),
        ('Dados Adicionais', {
            'fields': ('link_acao', 'dados_extras'),
            'classes': ('collapse',)
        }),
    )
    
    def get_preview(self, obj):
        preview = obj.mensagem[:50] + '...' if len(obj.mensagem) > 50 else obj.mensagem
        return format_html('<span title="{}">{}</span>', obj.mensagem, preview)
    get_preview.short_description = 'Preview'
    
    actions = ['marcar_como_lida', 'marcar_como_nao_lida']
    
    def marcar_como_lida(self, request, queryset):
        count = queryset.filter(lida=False).update(lida=True, data_leitura=timezone.now())
        self.message_user(request, f'{count} notificações marcadas como lidas.')
    marcar_como_lida.short_description = 'Marcar como lida'
    
    def marcar_como_nao_lida(self, request, queryset):
        count = queryset.filter(lida=True).update(lida=False, data_leitura=None)
        self.message_user(request, f'{count} notificações marcadas como não lidas.')
    marcar_como_nao_lida.short_description = 'Marcar como não lida'


@admin.register(PreferenciaAtleta)
class PreferenciaAtletaAdmin(admin.ModelAdmin):
    list_display = ('atleta', 'receber_email_inscricao', 'receber_email_pagamento', 'tema_escuro', 'perfil_publico')
    list_filter = ('receber_email_inscricao', 'receber_email_pagamento', 'tema_escuro', 'perfil_publico')
    search_fields = ('atleta__email',)
    
    fieldsets = (
        ('Notificações por Email', {
            'fields': ('atleta', 'receber_email_inscricao', 'receber_email_pagamento', 
                      'receber_email_competicao', 'receber_email_resultado')
        }),
        ('Interface', {
            'fields': ('tema_escuro', 'idioma')
        }),
        ('Privacidade', {
            'fields': ('perfil_publico', 'mostrar_resultados', 'mostrar_estatisticas')
        }),
        ('Configurações Extras', {
            'fields': ('configuracoes_extras',),
            'classes': ('collapse',)
        }),
    )


@admin.register(LogAtividadeAtleta)
class LogAtividadeAtletaAdmin(admin.ModelAdmin):
    list_display = ('atleta', 'acao', 'get_descricao_preview', 'ip_address', 'data_acao')
    list_filter = ('acao', 'data_acao')
    search_fields = ('atleta__email', 'acao', 'descricao')
    readonly_fields = ('data_acao',)
    date_hierarchy = 'data_acao'
    
    fieldsets = (
        (None, {
            'fields': ('atleta', 'acao', 'descricao')
        }),
        ('Informações Técnicas', {
            'fields': ('ip_address', 'user_agent', 'dados_extras', 'data_acao'),
            'classes': ('collapse',)
        }),
    )
    
    def get_descricao_preview(self, obj):
        if obj.descricao:
            preview = obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
            return format_html('<span title="{}">{}</span>', obj.descricao, preview)
        return '-'
    get_descricao_preview.short_description = 'Descrição'
    
    def has_add_permission(self, request):
        return False  # Logs são criados automaticamente
    
    def has_change_permission(self, request, obj=None):
        return False  # Logs não devem ser editados
    
    def has_delete_permission(self, request, obj=None):
        # Só superusers podem deletar logs
        return request.user.is_superuser


# Customização do site admin
admin.site.site_header = 'KeyChart - Portal do Atleta'
admin.site.site_title = 'KeyChart Admin'
admin.site.index_title = 'Administração do Portal do Atleta'
