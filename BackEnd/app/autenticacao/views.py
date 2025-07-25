from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return redirect('login')
    return render(request, 'autenticacao/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('login')

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            users = list(form.get_users(form.cleaned_data["email"]))
            if users:
                for user in users:
                    context = {
                        'email': user.email,
                        'domain': request.get_host(),
                        'site_name': 'KeyChart',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    }
                    subject = 'Redefinição de Senha KeyChart'
                    url = f"/keychart/reset/{context['uid']}/{context['token']}/"
                    email_html = render_to_string('autenticacao/password_reset_email.html', {
                        'protocol': context['protocol'],
                        'domain': context['domain'],
                        'url': url,
                    })
                    send_mail(
                        subject,
                        'Clique no link para redefinir sua senha.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        html_message=email_html,
                    )
            messages.success(request, 'Se o e-mail estiver cadastrado, você receberá instruções para redefinir sua senha.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'autenticacao/password_reset.html', {'form': form})

def check_email_exists(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Método inválido'}, status=400)