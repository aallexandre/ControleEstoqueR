from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from estoque.models import Ingrediente


class Command(BaseCommand):
    help = 'Adiciona exemplos com datas relativas a hoje, sem alterar registros existentes.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-referencia', type=date.fromisoformat,
            help='Opcional: data no formato AAAA-MM-DD para reproduzir uma demonstração.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        referencia = options.get('data_referencia') or timezone.localdate()
        exemplos = [
            ('Farinha', 'Kg', 20, 20, 12, False, False),
            ('Leite', 'L', 10, 10, 6, True, False),
            ('Arroz', 'Kg', 20, 10, 10, False, True),
            ('Óleo', 'L', 10, 10, 10, False, False),
            ('Sal', 'Kg', 5, 8, 1, False, False),
            ('Açúcar', 'Kg', 5, 5, 0, False, False),
            ('Ovos', 'un', 10, 3, 3, False, True),
            ('Feijão', 'Kg', 20, 10, 10, True, True),
        ]
        criados = 0
        for nome, unidade, meta, inicial, consumo, vencido, antecipado in exemplos:
            if Ingrediente.objects.filter(nome=nome).exists():
                continue
            ingrediente = Ingrediente(
                nome=nome, unidade=unidade, meta=Decimal(meta),
                estoque_inicial=Decimal(inicial), consumo=Decimal(consumo),
                validade=referencia - timedelta(days=1) if vencido else referencia + timedelta(days=30),
                acabou_antes_fim_mes=antecipado,
            )
            ingrediente.full_clean()
            ingrediente.save()
            criados += 1
        self.stdout.write(self.style.SUCCESS(
            f'{criados} exemplos adicionados. Referência: {referencia:%d/%m/%Y}. Registros existentes foram preservados.'
        ))
