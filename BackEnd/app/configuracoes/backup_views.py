import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import shutil
import zipfile
from datetime import datetime

BACKUP_DIR = os.path.join(settings.BASE_DIR, 'media', 'backups')
DB_PATH = settings.DATABASES['default']['NAME']

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def gerar_backup(request):
    """Gera um backup do banco de dados e arquivos relevantes."""
    if request.method == 'POST':
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{now}.zip'
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        with zipfile.ZipFile(backup_path, 'w') as backup_zip:
            # Banco de dados
            backup_zip.write(DB_PATH, arcname=os.path.basename(DB_PATH))
            # Adicione outras pastas relevantes se necessário
            # Exemplo: fotos de atletas
            fotos_dir = os.path.join(settings.BASE_DIR, 'media', 'fotos_atletas')
            if os.path.exists(fotos_dir):
                for root, dirs, files in os.walk(fotos_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, settings.BASE_DIR)
                        backup_zip.write(file_path, arcname=arcname)
        # Corrige o retorno para o padrão esperado pelo frontend
        url = f"/configuracoes/backup/baixar/{backup_name}"
        return JsonResponse({'sucesso': True, 'url': url, 'mensagem': 'Backup criado com sucesso!'})
    return HttpResponseBadRequest()

@login_required
@user_passes_test(is_superuser)
def listar_backups(request):
    """Lista os arquivos de backup disponíveis."""
    backups = []
    for fname in sorted(os.listdir(BACKUP_DIR), reverse=True):
        if fname.endswith('.zip'):
            fpath = os.path.join(BACKUP_DIR, fname)
            backups.append({
                'nome': fname,
                'tamanho': f"{os.path.getsize(fpath)/1024/1024:.1f} MB",
                'data': datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d %H:%M'),
                'url': f"/keychart/configuracoes/backup/baixar/{fname}",
            })
    return JsonResponse({'backups': backups})

@login_required
@user_passes_test(is_superuser)
def baixar_backup(request, filename):
    """Permite baixar um arquivo de backup."""
    file_path = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
    return HttpResponseBadRequest('Arquivo não encontrado.')

@login_required
@user_passes_test(is_superuser)
def excluir_backup(request, filename):
    """Exclui um arquivo de backup."""
    file_path = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return JsonResponse({'success': True})
    return HttpResponseBadRequest('Arquivo não encontrado.')

@login_required
@user_passes_test(is_superuser)
def restaurar_backup(request):
    """Restaura o sistema a partir de um backup enviado."""
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        temp_path = os.path.join(BACKUP_DIR, 'temp_restore.zip')
        with open(temp_path, 'wb+') as dest:
            for chunk in arquivo.chunks():
                dest.write(chunk)
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            # Restaurar banco de dados
            for member in zip_ref.namelist():
                if member.endswith('.sqlite3'):
                    db_dest = DB_PATH
                    zip_ref.extract(member, BACKUP_DIR)
                    shutil.copy2(os.path.join(BACKUP_DIR, member), db_dest)
                # Restaurar fotos de atletas
                if member.startswith('media/fotos_atletas/'):
                    zip_ref.extract(member, settings.BASE_DIR)
        os.remove(temp_path)
        messages.success(request, 'Backup restaurado com sucesso!')
        return redirect('configuracoes:home')
    messages.error(request, 'Arquivo inválido para restauração.')
    return redirect('configuracoes:home')
