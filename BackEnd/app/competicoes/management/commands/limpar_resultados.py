from django.core.management.base import BaseCommand
from app.competicoes.models import ResultadoKata, ChaveamentoKata

class Command(BaseCommand):
    help = 'Limpa todos os resultados salvos para permitir novos testes'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--categoria',
            type=int,
            help='ID da categoria específica para limpar (opcional)',
        )
        parser.add_argument(
            '--tudo',
            action='store_true',
            help='Remove TODOS os dados (resultados e chaveamentos)',
        )

    def handle(self, *args, **options):
        categoria_id = options.get('categoria')
        
        if options.get('tudo'):
            # Remove tudo
            resultados_count = ResultadoKata.objects.count()
            chaveamentos_count = ChaveamentoKata.objects.count()
            
            ResultadoKata.objects.all().delete()
            ChaveamentoKata.objects.all().delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Removidos {resultados_count} resultados e {chaveamentos_count} chaveamentos!'
                )
            )
        elif categoria_id:
            # Limpa apenas uma categoria
            resultados = ResultadoKata.objects.filter(categoria_id=categoria_id)
            count = resultados.update(
                salvo=False,
                status='ativo',
                nota1=0.0,
                nota2=0.0,
                nota3=0.0,
                nota4=0.0,
                nota5=0.0,
                total=0.0,
                posicao=0
            )
            
            # Reseta o chaveamento da categoria
            ChaveamentoKata.objects.filter(categoria_id=categoria_id).update(
                fase_atual='eliminatorias',
                finalizado=False,
                data_finalizacao=None
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Resetados {count} resultados da categoria {categoria_id}!')
            )
        else:
            # Reseta todos os resultados
            count = ResultadoKata.objects.all().update(
                salvo=False,
                status='ativo',
                nota1=0.0,
                nota2=0.0,
                nota3=0.0,
                nota4=0.0,
                nota5=0.0,
                total=0.0,
                posicao=0
            )
            
            # Reseta todos os chaveamentos
            ChaveamentoKata.objects.all().update(
                fase_atual='eliminatorias',
                finalizado=False,
                data_finalizacao=None
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Resetados {count} resultados! Agora você pode testar novamente.')
            )
