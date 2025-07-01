# KeyChart - Documentação Técnica Completa

## 1. Visão Geral do Sistema

### 1.1 Descrição do Projeto
O **KeyChart** é um sistema de gerenciamento de competições de karatê desenvolvido em Django. O sistema permite o cadastro e gerenciamento completo de competições, atletas, categorias, academias e chaveamentos tanto para modalidade Kata quanto Kumitê.

### 1.2 Arquitetura do Sistema
- **Framework**: Django 5.2
- **Linguagem**: Python 3.11+
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Geração de PDFs**: xhtml2pdf
- **Processamento de Imagens**: Pillow

## 2. Estrutura do Projeto

### 2.1 Estrutura de Diretórios
```
BackEnd/
├── core/                           # Configurações principais do Django
│   ├── __init__.py
│   ├── settings.py                 # Configurações do projeto
│   ├── urls.py                     # URLs principais
│   ├── wsgi.py                     # Configuração WSGI
│   └── asgi.py                     # Configuração ASGI
├── app/                            # Aplicações Django
│   ├── autenticacao/               # Módulo de autenticação
│   ├── dashboard/                  # Dashboard principal
│   ├── competicoes/                # Gestão de competições
│   ├── atletas/                    # Gestão de atletas
│   ├── portal_atleta/              # Portal público dos atletas
│   ├── configuracoes/              # Configurações do sistema
│   ├── partidas_chaveamento/       # Chaveamentos e partidas
│   └── relatorios/                 # Relatórios do sistema
├── templates/                      # Templates globais
├── static/                         # Arquivos estáticos globais
├── media/                          # Arquivos de mídia (fotos)
├── fotos_atletas/                  # Fotos dos atletas
├── db.sqlite3                      # Banco de dados SQLite
├── manage.py                       # Script de gerenciamento Django
└── requirements.txt                # Dependências do projeto
```

### 2.2 Aplicações Django

#### 2.2.1 core (Configurações principais)
- **Responsabilidade**: Configurações centrais do Django
- **Arquivos principais**:
  - `settings.py`: Configurações do projeto
  - `urls.py`: Roteamento principal
  - `wsgi.py`/`asgi.py`: Configurações de servidor

#### 2.2.2 app.autenticacao
- **Responsabilidade**: Sistema de login e autenticação
- **Funcionalidades**:
  - Login com credenciais fixas (via variáveis de ambiente)
  - Middleware de autenticação obrigatória
  - Decoradores de proteção de rotas

#### 2.2.3 app.dashboard
- **Responsabilidade**: Dashboard principal do sistema
- **Funcionalidades**:
  - Página inicial após login
  - Navegação principal do sistema

#### 2.2.4 app.competicoes
- **Responsabilidade**: Gerenciamento completo de competições
- **Funcionalidades**:
  - CRUD de competições
  - Gestão de categorias
  - Gestão de academias
  - Gestão de árbitros
  - Chaveamento Kata com sistema de pontuação WKF
  - Chaveamento Kumitê (em desenvolvimento)
  - Geração de relatórios em PDF

#### 2.2.5 app.atletas
- **Responsabilidade**: Gerenciamento de atletas e inscrições
- **Funcionalidades**:
  - Sistema de inscrições público
  - CRUD de atletas
  - Upload de fotos
  - Exportação de listas (PDF/CSV)
  - Envio de emails de confirmação

#### 2.2.6 app.portal_atleta
- **Responsabilidade**: Portal público para consulta de atletas
- **Funcionalidades**:
  - Consulta pública de resultados
  - Perfil público do atleta

#### 2.2.7 app.configuracoes
- **Responsabilidade**: Configurações do sistema
- **Funcionalidades**:
  - Configurações gerais do sistema

#### 2.2.8 app.partidas_chaveamento
- **Responsabilidade**: Gestão de partidas e chaveamentos
- **Funcionalidades**:
  - Visualização de chaveamentos
  - Gestão de partidas (em desenvolvimento)

#### 2.2.9 app.relatorios
- **Responsabilidade**: Geração de relatórios
- **Funcionalidades**:
  - Relatórios de competições
  - Relatórios de atletas
  - Exportação em diversos formatos

## 3. Modelos de Dados (Models)

### 3.1 app.competicoes.models

#### 3.1.1 Competicao
```python
class Competicao(models.Model):
    # Informações básicas
    nome = CharField(max_length=100)
    modalidade = CharField(max_length=50)
    data_inicio = DateField()
    horario = TimeField()
    local = CharField(max_length=150)
    regras_especificas = TextField()
    status = CharField(choices=STATUS_CHOICES, default='Ativa')
    
    # Árbitros
    arbitros = ManyToManyField(Arbitro)
    
    # Configurações de inscrições
    inscricoes_abertas = BooleanField(default=True)
    inscricoes_status = CharField(choices=INSCRICOES_STATUS_CHOICES)
    inscricoes_data_limite = DateField()
    inscricoes_valor = DecimalField(max_digits=10, decimal_places=2)
    inscricoes_taxa = DecimalField(max_digits=10, decimal_places=2)
    inscricoes_desconto = DecimalField(max_digits=10, decimal_places=2)
    
    # Métodos de pagamento
    inscricoes_pagamento_pix = BooleanField(default=True)
    inscricoes_pagamento_cartao = BooleanField(default=True)
    inscricoes_pagamento_boleto = BooleanField(default=False)
    
    # Configurações de exibição
    inscricoes_mostrar_valor = BooleanField(default=True)
    inscricoes_mostrar_vagas = BooleanField(default=False)
    inscricoes_mensagem = TextField()
```

**Relacionamentos**:
- Um para muitos com `Categoria`
- Um para muitos com `Academia`
- Muitos para muitos com `Arbitro`

#### 3.1.2 Categoria
```python
class Categoria(models.Model):
    competicao = ForeignKey(Competicao)
    nome = CharField(max_length=100)
    sexo = CharField(choices=SEXO_CHOICES)  # M, F, MX
    tipo = CharField(choices=TIPO_CHOICES)  # GI, NOGI, ABS
```

#### 3.1.3 Academia
```python
class Academia(models.Model):
    competicao = ForeignKey(Competicao)
    nome = CharField(max_length=100)
    cidade = CharField(max_length=100)
    estado = CharField(max_length=2)
    endereco = CharField(max_length=200)
```

#### 3.1.4 Arbitro
```python
class Arbitro(models.Model):
    nome = CharField(max_length=100)
    email = EmailField(unique=True)
    telefone = CharField(max_length=20)
    data_criacao = DateTimeField(auto_now_add=True)
```

#### 3.1.5 ResultadoKata
```python
class ResultadoKata(models.Model):
    atleta = ForeignKey('atletas.Atleta')
    categoria = ForeignKey(Categoria)
    competicao = ForeignKey(Competicao)
    fase = CharField(choices=FASE_CHOICES)  # eliminatorias, semifinal, final
    nota1 = FloatField(default=0.0)
    nota2 = FloatField(default=0.0)
    nota3 = FloatField(default=0.0)
    nota4 = FloatField(default=0.0)
    nota5 = FloatField(default=0.0)
    total = FloatField(default=0.0)
    posicao = IntegerField(default=0)
    status = CharField(choices=STATUS_CHOICES)  # ativo, classificado, eliminado
    salvo = BooleanField(default=False)
```

**Regras de Negócio**:
- Total calculado automaticamente removendo maior e menor nota
- Unique together: (atleta, categoria, fase)

#### 3.1.6 ChaveamentoKata
```python
class ChaveamentoKata(models.Model):
    categoria = OneToOneField(Categoria)
    competicao = ForeignKey(Competicao)
    fase_atual = CharField(choices=FASE_CHOICES, default='eliminatorias')
    finalizado = BooleanField(default=False)
    data_criacao = DateTimeField(auto_now_add=True)
    data_finalizacao = DateTimeField()
```

#### 3.1.7 ChaveamentoKumite
```python
class ChaveamentoKumite(models.Model):
    categoria = OneToOneField(Categoria)
    competicao = ForeignKey(Competicao)
    tipo_chaveamento = CharField(choices=TIPO_CHAVEAMENTO_CHOICES)
    fase_atual = CharField(max_length=50, default='oitavas')
    finalizado = BooleanField(default=False)
```

#### 3.1.8 PartidaKumite
```python
class PartidaKumite(models.Model):
    chaveamento = ForeignKey(ChaveamentoKumite)
    categoria = ForeignKey(Categoria)
    competicao = ForeignKey(Competicao)
    fase = CharField(max_length=50)
    round_numero = IntegerField(default=1)
    
    # Atletas
    atleta1 = ForeignKey('atletas.Atleta', related_name='partidas_kumite_atleta1')
    atleta2 = ForeignKey('atletas.Atleta', related_name='partidas_kumite_atleta2')
    
    # Resultado
    status = CharField(choices=STATUS_CHOICES, default='agendada')
    resultado = CharField(choices=RESULTADO_CHOICES)
    vencedor = ForeignKey('atletas.Atleta', related_name='vitorias_kumite')
    
    # Pontuação
    pontos_atleta1 = IntegerField(default=0)
    pontos_atleta2 = IntegerField(default=0)
    advertencias_atleta1 = IntegerField(default=0)
    advertencias_atleta2 = IntegerField(default=0)
    penalidades_atleta1 = IntegerField(default=0)
    penalidades_atleta2 = IntegerField(default=0)
```

### 3.2 app.atletas.models

#### 3.2.1 Atleta
```python
class Atleta(models.Model):
    competicao = ForeignKey(Competicao)
    categoria = ForeignKey(Categoria)
    academia = ForeignKey(Academia)
    
    # Dados pessoais
    nome_completo = CharField(max_length=100)
    data_nascimento = DateField()
    sexo = CharField(choices=SEXO_CHOICES)  # M, F, X
    idade = IntegerField()
    peso = DecimalField(max_digits=5, decimal_places=2)
    altura = IntegerField(default=0)
    email = EmailField()
    telefone = CharField(max_length=20)
    
    # Dados do karatê
    faixa = CharField(choices=FAIXA_CHOICES)
    
    # Localização
    cidade = CharField(max_length=50)
    estado = CharField(choices=ESTADO_CHOICES)
    
    # Mídia
    foto = ImageField(upload_to='fotos_atletas/')
    
    # Metadados
    data_inscricao = DateTimeField(auto_now_add=True)
```

**Choices disponíveis**:
- `FAIXA_CHOICES`: branca, azul, amarela, laranja, verde, roxa, marrom, preta
- `ESTADO_CHOICES`: Todos os estados brasileiros
- `SEXO_CHOICES`: M, F, X (Misto)

## 4. Views e Lógica de Negócio

### 4.1 app.competicoes.views

#### 4.1.1 Gerenciamento de Competições
- `criar_competicao()`: Criação de nova competição com validações
- `editar_competicao()`: Edição de competição existente
- `excluir_competicao()`: Exclusão com confirmação
- `competicoes()`: Listagem com filtros avançados

#### 4.1.2 Chaveamento Kata
- `chaveamento_kata()`: Gerenciamento completo do chaveamento Kata
- **Funcionalidades**:
  - Criação automática de resultados para eliminatórias
  - Salvamento de notas dos 5 juízes
  - Cálculo automático do total (remove maior e menor nota)
  - Classificação automática baseada nas regras WKF
  - Avanço automático de fases
  - Geração de pódio final

**Regras implementadas (Kata)**:
- ≤ 4 atletas: Todos vão direto para a final
- 5-8 atletas: Top 4 vão para a final
- 9-16 atletas: Top 8 vão para a semifinal
- > 16 atletas: Top 16 vão para a próxima fase
- Pontuação mínima: 5.0 pontos para avançar
- Sistema de 5 juízes: remove maior e menor, soma as 3 restantes

#### 4.1.3 Categorias e Academias
- `categoria()`: Gestão de categorias por competição
- `cadastrar_categoria()`: Criação de nova categoria
- `excluir_categoria()`: Exclusão de categoria
- `cadastrar_academia()`: Criação de nova academia
- `editar_academia()`: Edição de academia
- `excluir_academia()`: Exclusão de academia

### 4.2 app.atletas.views

#### 4.2.1 Sistema de Inscrições
- `inscricoes_view()`: Página pública de inscrições
- `enviar_email_inscricao()`: Processamento de inscrição
- **Funcionalidades**:
  - Validação de dados obrigatórios
  - Upload e redimensionamento de fotos
  - Criação automática de academias se não existir
  - Envio de email de confirmação (configurável)
  - Resposta AJAX para UX melhorada

#### 4.2.2 Gestão de Atletas
- `atletas()`: Listagem de atletas
- `perfil_atleta()`: Perfil individual do atleta
- `carregar_categorias()`: Carregamento dinâmico via AJAX

### 4.3 app.autenticacao.views

#### 4.3.1 Sistema de Autenticação
- `login_view()`: Autenticação com credenciais fixas
- `logout_view()`: Logout do sistema
- **Segurança**:
  - Credenciais via variáveis de ambiente
  - Sessões Django para controle de acesso
  - Middleware obrigatório para todas as rotas

## 5. URLs e Roteamento

### 5.1 URLs Principais (core/urls.py)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('keychart/', include('app.dashboard.urls')),
    path('keychart/competicoes/', include('app.competicoes.urls')),
    path('keychart/equipes_atletas/', include('app.atletas.urls')),
    path('keychart/login/', include('app.autenticacao.urls')),
    path('keychart/portal_atleta/', include('app.portal_atleta.urls')),
    path('keychart/configuracoes/', include('app.configuracoes.urls')),
    path('keychart/', include('app.partidas_chaveamento.urls')),
    path('keychart/relatorio/', include('app.relatorios.urls')),
]
```

### 5.2 URLs por Aplicação

#### 5.2.1 app.competicoes.urls
```python
urlpatterns = [
    # Competições
    path('', views.competicoes, name='home'),
    path('criar/', views.criar_competicao, name='criar_competicao'),
    path('editar/<int:competicao_id>/', views.editar_competicao, name='editar_competicao'),
    path('excluir/<int:competicao_id>/', views.excluir_competicao, name='excluir_competicao'),
    
    # Categorias
    path('competicao/<int:competicao_id>/categorias/', views.categoria, name='categoria'),
    path('categoria/<int:categoria_id>/excluir/', views.excluir_categoria, name='excluir_categoria'),
    path('categoria/<int:categoria_id>/atletas/chaveamento_kata/', views.chaveamento_kata, name='chaveamento_kata'),
    path('categoria/<int:categoria_id>/atletas/chaveamento_kumite/', views.chaveamento_kumite, name='chaveamento_kumite'),
    
    # Academias
    path('academia/cadastrar/', views.cadastrar_academia, name='cadastrar_academia'),
    path('academia/<int:academia_id>/editar/', views.editar_academia, name='editar_academia'),
    path('academia/<int:academia_id>/excluir/', views.excluir_academia, name='excluir_academia'),
    
    # Árbitros
    path('arbitro/adicionar/', views.adicionar_arbitro, name='adicionar_arbitro'),
    path('arbitros/listar/', views.listar_arbitros, name='listar_arbitros'),
]
```

#### 5.2.2 app.atletas.urls
```python
urlpatterns = [
    path('', views.atletas, name='home'),
    path('perfil_atleta/', views.perfil_atleta, name='perfil_atleta'),
    path('inscricoes/', views.inscricoes_view, name='inscricoes'),
    path('carregar_categorias/<int:competicao_id>/', views.carregar_categorias, name='carregar_categorias'),
    path('finalizar_inscricao/', views.enviar_email_inscricao, name='finalizar_inscricao'),
]
```

#### 5.2.3 app.autenticacao.urls
```python
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

## 6. Templates e Frontend

### 6.1 Estrutura de Templates
```
templates/
├── sidebar.html                    # Template global da sidebar
app/
├── autenticacao/templates/autenticacao/
│   └── login.html                  # Página de login
├── dashboard/templates/dashboard/
│   ├── dashboard.html              # Dashboard principal
│   └── sidebar.html                # Sidebar específica
├── competicoes/templates/competicoes/
│   ├── competicoes.html            # Listagem de competições
│   ├── categoria.html              # Gestão de categorias
│   ├── chaveamento_kata.html       # Chaveamento Kata
│   ├── chaveamento_kumite.html     # Chaveamento Kumitê
│   └── atletas_categoria.html      # Atletas por categoria
├── atletas/templates/atletas/
│   ├── inscricoes.html             # Página pública de inscrições
│   ├── equipes_atletas.html        # Gestão de atletas
│   ├── perfil_atleta.html          # Perfil do atleta
│   └── email_inscricao.html        # Template de email
└── [outras aplicações...]
```

### 6.2 Tecnologias Frontend
- **CSS Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS + jQuery
- **Componentes**: Modais, formulários dinâmicos, tabelas responsivas
- **AJAX**: Para carregamento dinâmico e envio de formulários

## 7. Configurações (settings.py)

### 7.1 Configurações Principais
```python
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
    'app.portal_atleta',
    'app.configuracoes',
    'app.partidas_chaveamento',
    'app.relatorios',
]

# Middleware personalizado
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.autenticacao.middleware.login_required_middleware.LoginRequiredMiddleware',
]
```

### 7.2 Banco de Dados
```python
# SQLite (desenvolvimento)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL (produção) - Comentado
'''
DATABASES = {
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
```

### 7.3 Arquivos Estáticos e Mídia
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
    os.path.join(BASE_DIR, 'app/dashboard/static'),
    os.path.join(BASE_DIR, 'app/competicoes/static'),
    os.path.join(BASE_DIR, 'app/autenticacao/static'),
    os.path.join(BASE_DIR, 'app/atletas/static'),
]

# Mídia (comentado)
'''
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
'''
```

### 7.4 Configurações de Email
```python
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
```

### 7.5 Localização
```python
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
```

## 8. Autenticação e Segurança

### 8.1 Sistema de Autenticação
- **Tipo**: Autenticação simples com credenciais fixas
- **Armazenamento**: Variáveis de ambiente (.env)
- **Sessões**: Django sessions para controle de acesso
- **Middleware**: `LoginRequiredMiddleware` para proteção global

### 8.2 Middleware de Autenticação
```python
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = [
            reverse('login'),
            reverse('logout'),
        ]

    def __call__(self, request):
        if not request.session.get('usuario_autenticado'):
            if request.path not in self.public_paths and not request.path.startswith('/static/'):
                return redirect('login')
        return self.get_response(request)
```

### 8.3 Decorator de Proteção
```python
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
```

### 8.4 Variáveis de Ambiente (.env)
```bash
SECRET_KEY=sua_secret_key_aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
USUARIO_FIXO=admin
SENHA_FIXA=senha123
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app
DEFAULT_FROM_EMAIL=seu_email@gmail.com
```

## 9. Dependências (requirements.txt)

### 9.1 Dependências Principais
```txt
Django==5.2                    # Framework web
pillow==11.2.1                # Processamento de imagens
psycopg2-binary==2.9.10       # Driver PostgreSQL
python-decouple==3.8          # Variáveis de ambiente
python-dotenv==1.1.0          # Carregamento de .env
reportlab==4.4.1              # Geração de PDFs
xhtml2pdf==0.2.17             # Conversão HTML para PDF
requests==2.32.3              # Requisições HTTP
PyYAML==6.0.2                 # Processamento YAML
```

### 9.2 Dependências Adicionais
```txt
arabic-reshaper==3.0.0        # Suporte a texto árabe
asgiref==3.8.1                # Interface ASGI
certifi==2025.4.26            # Certificados SSL
cffi==1.17.1                  # Interface C
chardet==5.2.0                # Detecção de charset
cryptography==45.0.3          # Criptografia
cssselect2==0.8.0             # Seletores CSS
html5lib==1.1                 # Parser HTML5
lxml==5.4.0                   # Processamento XML
svglib==1.5.1                 # Processamento SVG
tinycss2==1.4.0               # Parser CSS
```

## 10. Funcionalidades Implementadas

### 10.1 Módulo de Competições
- ✅ CRUD completo de competições
- ✅ Gestão de categorias por competição
- ✅ Gestão de academias
- ✅ Gestão de árbitros
- ✅ Sistema de inscrições configurável
- ✅ Chaveamento Kata com regras WKF
- ✅ Geração de PDFs para chaveamentos
- 🔄 Chaveamento Kumitê (em desenvolvimento)

### 10.2 Módulo de Atletas
- ✅ Sistema de inscrições público
- ✅ Upload de fotos com redimensionamento
- ✅ Validação de dados obrigatórios
- ✅ Exportação de listas (PDF/CSV)
- ✅ Perfil público do atleta
- 🔄 Sistema de email (configurável)

### 10.3 Módulo de Autenticação
- ✅ Login com credenciais fixas
- ✅ Middleware de proteção global
- ✅ Sistema de sessões
- ✅ Logout completo

### 10.4 Sistema de Chaveamento Kata
- ✅ Regras oficiais WKF implementadas
- ✅ Sistema de 5 juízes
- ✅ Cálculo automático de pontuação
- ✅ Classificação automática por número de atletas
- ✅ Fases: Eliminatórias → Semifinal → Final
- ✅ Geração de pódio
- ✅ Relatórios em PDF

## 11. Regras de Negócio - Kata

### 11.1 Sistema de Pontuação
- **5 juízes avaliam cada kata**
- **Remove a maior e menor nota**
- **Soma as 3 notas restantes**
- **Pontuação mínima para avançar: 5.0 pontos**

### 11.2 Sistema de Classificação
```python
# Eliminatórias
if atletas <= 4:
    classificados = "Todos vão direto para final"
elif atletas <= 8:
    classificados = "Top 4 vão para final"
elif atletas <= 16:
    classificados = "Top 8 vão para semifinal"
else:
    classificados = "Top 16 vão para próxima fase"

# Semifinal
classificados_final = "Top 4 atletas"

# Final
podio = "Top 3 atletas (1º, 2º, 3º lugar)"
```

### 11.3 Critérios de Eliminação
1. **Pontuação insuficiente**: < 5.0 pontos
2. **Classificação**: Fora do número de classificados
3. **Empate**: Considera maior nota individual

## 12. Comandos de Gerenciamento

### 12.1 Comandos Django Customizados
```bash
# Limpar resultados de uma competição
python manage.py limpar_resultados

# Criar árbitros de exemplo
python manage.py criar_arbitros_exemplo

# Criar katas oficiais
python manage.py criar_katas_oficiais
```

### 12.2 Comandos Django Padrão
```bash
# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor de desenvolvimento
python manage.py runserver

# Coletar arquivos estáticos
python manage.py collectstatic

# Criar migrações
python manage.py makemigrations
```

## 13. Deployment e Produção

### 13.1 Configurações de Produção
- **DEBUG = False**
- **ALLOWED_HOSTS** configurado adequadamente
- **PostgreSQL** como banco de dados
- **Arquivos estáticos** servidos pelo servidor web
- **HTTPS** obrigatório
- **Variáveis de ambiente** protegidas

### 13.2 Considerações de Segurança
- Secret key forte e única
- Credenciais em variáveis de ambiente
- Middleware de segurança ativo
- CSRF protection habilitado
- XSS protection via templates

## 14. Manutenção e Monitoramento

### 14.1 Logs
- Django logging configurado
- Logs de erro capturados
- Logs de acesso monitorados

### 14.2 Backup
- Backup regular do banco de dados
- Backup de arquivos de mídia (fotos)
- Versionamento de código

### 14.3 Performance
- Queries otimizadas com select_related
- Paginação implementada onde necessário
- Cache configurado para produção

## 15. Próximas Implementações

### 15.1 Funcionalidades Pendentes
- 🔄 Sistema de Kumitê completo
- 🔄 Dashboard com estatísticas avançadas
- 🔄 Sistema de notificações
- 🔄 API REST para mobile
- 🔄 Sistema de pagamentos online
- 🔄 Relatórios avançados
- 🔄 Sistema de ranking

### 15.2 Melhorias Técnicas
- 🔄 Testes automatizados
- 🔄 Docker para deployment
- 🔄 CI/CD pipeline
- 🔄 Monitoramento avançado
- 🔄 Cache Redis
- 🔄 CDN para arquivos estáticos

## 16. Guia de Desenvolvimento

### 16.1 Configuração do Ambiente
1. Clone o repositório
2. Crie um ambiente virtual Python 3.11+
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure as variáveis de ambiente (.env)
5. Execute as migrações: `python manage.py migrate`
6. Crie um superusuário: `python manage.py createsuperuser`
7. Execute o servidor: `python manage.py runserver`

### 16.2 Padrões de Código
- **PEP 8** para Python
- **Nomes descritivos** para variáveis e funções
- **Docstrings** para classes e funções complexas
- **Comentários** em código complexo
- **Validações** sempre no backend
- **Transações** para operações críticas

### 16.3 Estrutura de Commits
```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
style: mudanças de formatação
refactor: refatoração de código
test: adiciona testes
chore: tarefas de manutenção
```

## 17. Troubleshooting

### 17.1 Problemas Comuns
- **Erro de migração**: Verificar models e dependências
- **Arquivo estático não carrega**: Verificar STATICFILES_DIRS
- **Upload de imagem falha**: Verificar MEDIA_ROOT e Pillow
- **Email não envia**: Verificar configurações SMTP
- **Sessão expira**: Verificar SESSION_EXPIRE_AT_BROWSER_CLOSE

### 17.2 Debug
- Utilizar Django Debug Toolbar em desenvolvimento
- Verificar logs do Django
- Usar print() ou logging para debug
- Verificar network tab no navegador para AJAX

## 18. Contatos e Suporte

### 18.1 Documentação Adicional
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [xhtml2pdf Documentation](https://xhtml2pdf.readthedocs.io/)

### 18.2 Estrutura de Dados do Sistema
```sql
-- Principais tabelas e relacionamentos
Competicao (1) -> (N) Categoria
Competicao (1) -> (N) Academia
Competicao (N) -> (N) Arbitro
Categoria (1) -> (N) Atleta
Academia (1) -> (N) Atleta
Categoria (1) -> (1) ChaveamentoKata
Categoria (1) -> (N) ResultadoKata
Atleta (1) -> (N) ResultadoKata
```

---

**Data da Documentação**: 1 de julho de 2025
**Versão do Sistema**: 1.0
**Framework**: Django 5.2
**Linguagem**: Python 3.11+

Esta documentação representa o estado atual completo do sistema KeyChart e deve ser atualizada conforme novas funcionalidades sejam implementadas.
