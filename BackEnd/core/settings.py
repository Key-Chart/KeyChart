from pathlib import Path
import os
from decouple import config, Csv
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = config('SECRET_KEY')

# Debug e hosts permitidos
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='127.0.0.1,localhost')

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.autenticacao',
    'app.dashboard',
    'app.competicoes',
    'app.atletas',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

# Configuração de URL raiz
ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Adiciona a pasta de templates no nível do projeto
        'APP_DIRS': True,  # Isso permite que o Django procure templates dentro das apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'core.wsgi.application'
# Banco de dados (SQLite por padrão)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Banco PostgreSQL
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'db.kixueapbpzdjlbszngnn.supabase.co',
        'PORT': '5432',
    }
}
'''

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    os.path.join(BASE_DIR, 'app/dashboard/static'),
    os.path.join(BASE_DIR, 'app/competicoes/static'),
    os.path.join(BASE_DIR, 'app/autenticacao/static'),
    os.path.join(BASE_DIR, 'app/atletas/static'),
]

# Tipo de chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configurações de email (ajuste conforme seu servidor)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))  # Converte para inteiro
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'  # Converte para boolean
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')