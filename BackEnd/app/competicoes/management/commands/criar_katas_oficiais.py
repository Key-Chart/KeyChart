from django.core.management.base import BaseCommand
from app.competicoes.models import KataOficial

class Command(BaseCommand):
    help = 'Cria katas oficiais de exemplo para o sistema'

    def handle(self, *args, **options):
        katas = [
            # Katas Shotokan
            {'nome': 'Heian Shodan', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 60},
            {'nome': 'Heian Nidan', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 65},
            {'nome': 'Heian Sandan', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 70},
            {'nome': 'Heian Yondan', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 75},
            {'nome': 'Heian Godan', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 80},
            {'nome': 'Tekki Shodan', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 85},
            {'nome': 'Bassai Dai', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 120},
            {'nome': 'Kanku Dai', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 135},
            {'nome': 'Jion', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 110},
            {'nome': 'Enpi', 'escola_origem': 'Shotokan', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 105},
            
            # Katas Kyokushin
            {'nome': 'Taikyoku Sono Ichi', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 45},
            {'nome': 'Taikyoku Sono Ni', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 50},
            {'nome': 'Taikyoku Sono San', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 55},
            {'nome': 'Pinan Sono Ichi', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 60},
            {'nome': 'Pinan Sono Ni', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 65},
            {'nome': 'Pinan Sono San', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 70},
            {'nome': 'Pinan Sono Yon', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 75},
            {'nome': 'Pinan Sono Go', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 80},
            {'nome': 'Gekisai Dai', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 115},
            {'nome': 'Gekisai Sho', 'escola_origem': 'Kyokushin', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 100},
            
            # Katas Shito-Ryu
            {'nome': 'Pinan Shodan', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 60},
            {'nome': 'Pinan Nidan', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 65},
            {'nome': 'Pinan Sandan', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 70},
            {'nome': 'Pinan Yondan', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 75},
            {'nome': 'Pinan Godan', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 80},
            {'nome': 'Naifanchin', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 90},
            {'nome': 'Bassai', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 110},
            {'nome': 'Rohai', 'escola_origem': 'Shito-Ryu', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 95},
            
            # Katas Goju-Ryu
            {'nome': 'Gekisai Dai Ichi', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 70},
            {'nome': 'Gekisai Dai Ni', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'iniciante', 'categoria': 'shitei', 'duracao_media': 75},
            {'nome': 'Saifa', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 85},
            {'nome': 'Seiyunchin', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'intermediario', 'categoria': 'shitei', 'duracao_media': 95},
            {'nome': 'Shisochin', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 120},
            {'nome': 'Sanseiru', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 125},
            {'nome': 'Sepai', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 115},
            {'nome': 'Kururunfa', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 130},
            {'nome': 'Suparinpei', 'escola_origem': 'Goju-Ryu', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 180},
            
            # Katas WKF (Lista Sentei)
            {'nome': 'Bassai Dai (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 120},
            {'nome': 'Kanku Dai (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 135},
            {'nome': 'Jion (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 110},
            {'nome': 'Enpi (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 105},
            {'nome': 'Gankaku (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 100},
            {'nome': 'Tekki Shodan (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'intermediario', 'categoria': 'sentei', 'duracao_media': 85},
            {'nome': 'Hangetsu (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 140},
            {'nome': 'Jitte (Sentei)', 'escola_origem': 'WKF', 'nivel_dificuldade': 'avancado', 'categoria': 'sentei', 'duracao_media': 125},
        ]

        criados = 0
        for kata_data in katas:
            kata, created = KataOficial.objects.get_or_create(
                nome=kata_data['nome'],
                escola_origem=kata_data['escola_origem'],
                defaults={
                    'nivel_dificuldade': kata_data['nivel_dificuldade'],
                    'categoria': kata_data['categoria'],
                    'duracao_media': kata_data['duracao_media'],
                    'descricao': f"Kata {kata_data['nome']} da escola {kata_data['escola_origem']}",
                    'ativo': True
                }
            )
            if created:
                criados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Kata "{kata.nome}" ({kata.escola_origem}) criado com sucesso!')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Total de {criados} katas oficiais criados!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📊 Total de katas no sistema: {KataOficial.objects.count()}')
        )
