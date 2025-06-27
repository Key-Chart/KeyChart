from django.core.management.base import BaseCommand
from app.competicoes.models import Arbitro

class Command(BaseCommand):
    help = 'Cria árbitros de exemplo para teste'

    def handle(self, *args, **options):
        arbitros_exemplo = [
            {
                'nome': 'João Silva',
                'email': 'joao.silva@email.com',
                'telefone': '(11) 99999-1111'
            },
            {
                'nome': 'Maria Santos',
                'email': 'maria.santos@email.com',
                'telefone': '(11) 99999-2222'
            },
            {
                'nome': 'Pedro Oliveira',
                'email': 'pedro.oliveira@email.com',
                'telefone': '(11) 99999-3333'
            },
            {
                'nome': 'Ana Costa',
                'email': 'ana.costa@email.com',
                'telefone': '(11) 99999-4444'
            },
            {
                'nome': 'Carlos Rodrigues',
                'email': 'carlos.rodrigues@email.com',
                'telefone': '(11) 99999-5555'
            }
        ]

        for arbitro_data in arbitros_exemplo:
            arbitro, created = Arbitro.objects.get_or_create(
                email=arbitro_data['email'],
                defaults={
                    'nome': arbitro_data['nome'],
                    'telefone': arbitro_data['telefone']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Árbitro "{arbitro.nome}" criado com sucesso')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Árbitro "{arbitro.nome}" já existe')
                )

        self.stdout.write(
            self.style.SUCCESS('Comando executado com sucesso!')
        )
