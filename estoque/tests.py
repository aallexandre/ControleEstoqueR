from datetime import date
from decimal import Decimal
from io import StringIO
from unittest.mock import patch
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from .forms import IngredienteForm
from .models import Ingrediente
from .regras_reposicao import calcular_reposicao, formatar_quantidade

REFERENCIA = date(2026, 9, 14)


class RegrasTests(TestCase):
    def test_oito_cenarios_do_guia(self):
        cenarios = [
            ('Farinha', 'Kg', 20, 20, 12, False, False, '12'),
            ('Leite', 'L', 10, 10, 6, True, False, '10'),
            ('Arroz', 'Kg', 20, 10, 10, False, True, '12'),
            ('Óleo', 'L', 10, 10, 10, False, False, '10'),
            ('Sal', 'Kg', 5, 8, 1, False, False, '0'),
            ('Açúcar', 'Kg', 5, 5, 0, False, False, '0'),
            ('Ovos', 'un', 10, 3, 3, False, True, '4'),
            ('Feijão', 'Kg', 20, 10, 10, True, True, '20'),
        ]
        for nome, unidade, meta, inicial, consumo, vencido, antecipado, esperado in cenarios:
            with self.subTest(nome=nome):
                item = Ingrediente(nome=nome, unidade=unidade, meta=Decimal(meta), estoque_inicial=Decimal(inicial), consumo=Decimal(consumo), validade=date(2026, 9, 13) if vencido else date(2026, 10, 1), acabou_antes_fim_mes=antecipado)
                item.full_clean()
                resultado = calcular_reposicao(item, REFERENCIA)
                self.assertEqual(resultado['compra'], Decimal(esperado))
                self.assertEqual(resultado['aproveitavel'], 0 if vencido else inicial - consumo)
                self.assertEqual(item.meta, meta)

    def test_valido_no_dia_da_validade(self):
        item = Ingrediente(meta=Decimal(20), estoque_inicial=Decimal(20), consumo=Decimal(12), validade=REFERENCIA, unidade='Kg')
        self.assertEqual(calcular_reposicao(item, REFERENCIA)['compra'], 12)

    def test_arredonda_fracoes_para_cima(self):
        for unidade in ['Kg', 'L']:
            with self.subTest(unidade=unidade):
                item = Ingrediente(meta=Decimal(5), estoque_inicial=Decimal('1.01'), consumo=Decimal('1.01'), validade=REFERENCIA, unidade=unidade, acabou_antes_fim_mes=True)
                self.assertEqual(calcular_reposicao(item, REFERENCIA)['compra'], Decimal('1.22'))

    def test_formatacao(self):
        for entrada, saida in [('12.00', '12'), ('1.20', '1,2'), ('0.01', '0,01'), ('100', '100')]:
            self.assertEqual(formatar_quantidade(Decimal(entrada)), saida)


class FormulariosTests(TestCase):
    def setUp(self):
        self.dados = {'nome': 'Farinha', 'unidade': 'Kg', 'meta': '20', 'estoque_inicial': '20', 'consumo': '12', 'validade': '2026-10-14'}

    def test_formulario_valido(self):
        self.assertTrue(IngredienteForm(self.dados).is_valid())

    def test_rejeita_dados_invalidos(self):
        casos = [
            ({'nome': '   '}, 'nome'), ({'unidade': 'ml'}, 'unidade'),
            ({'meta': '-1'}, 'meta'), ({'estoque_inicial': '-1'}, 'estoque_inicial'),
            ({'consumo': '-1'}, 'consumo'), ({'consumo': '21'}, 'consumo'),
            ({'unidade': 'un', 'meta': '1.5'}, 'meta'),
            ({'unidade': 'un', 'estoque_inicial': '20.5'}, 'estoque_inicial'),
            ({'unidade': 'un', 'consumo': '1.5'}, 'consumo'),
            ({'acabou_antes_fim_mes': 'on'}, 'acabou_antes_fim_mes'),
            ({'acabou_antes_fim_mes': 'on', 'consumo': '0', 'estoque_inicial': '0'}, 'acabou_antes_fim_mes'),
            ({'validade': '2026-02-30'}, 'validade'), ({'meta': 'abc'}, 'meta'),
            ({'consumo': 'abc', 'acabou_antes_fim_mes': 'on'}, 'consumo'),
            ({'meta': '1.001'}, 'meta'), ({'meta': 'NaN'}, 'meta'),
        ]
        for alteracoes, campo in casos:
            with self.subTest(alteracoes=alteracoes):
                form = IngredienteForm(self.dados | alteracoes)
                self.assertFalse(form.is_valid())
                self.assertIn(campo, form.errors)

    def test_cadastro_edicao_e_preservacao_do_formulario(self):
        novo = reverse('estoque:novo') + '?data_referencia=2026-09-14'
        resposta = self.client.post(novo, self.dados)
        self.assertRedirects(resposta, '/?data_referencia=2026-09-14')
        item = Ingrediente.objects.get()
        editar = reverse('estoque:editar', args=[item.pk])
        resposta = self.client.post(editar, self.dados | {'consumo': '21'})
        self.assertContains(resposta, 'O consumo não pode ultrapassar')
        self.assertContains(resposta, 'value="21"')
        item.refresh_from_db()
        self.assertEqual(item.consumo, 12)
        self.client.post(editar, self.dados | {'consumo': '15'})
        item.refresh_from_db()
        self.assertEqual(item.consumo, 15)
        self.assertEqual(Ingrediente.objects.count(), 1)

    def test_csrf_e_metodos(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse('estoque:novo'), self.dados).status_code, 403)
        self.assertEqual(self.client.post('/').status_code, 405)
        self.assertEqual(self.client.get('/ingredientes/999/editar/').status_code, 404)


class PaginaTests(TestCase):
    @patch('django.utils.timezone.localdate', return_value=date(2027, 2, 10))
    def test_data_atual_e_exemplos_relativos(self, data_atual):
        call_command('carregar_exemplos', stdout=StringIO())
        self.assertEqual(Ingrediente.objects.get(nome='Leite').validade, date(2027, 2, 9))
        self.assertEqual(Ingrediente.objects.get(nome='Farinha').validade, date(2027, 3, 12))
        resposta = self.client.get('/')
        self.assertEqual(resposta.context['data'], date(2027, 2, 10))
        self.assertContains(resposta, 'Stock Control')
        self.assertContains(resposta, 'Estoque organizado, mês tranquilo.')
        self.assertEqual(len(resposta.context['compras']), 6)

    def test_lista_vazia(self):
        self.assertContains(self.client.get('/'), 'Nenhuma compra necessária')

    def test_lista_gerada_no_backend_e_exemplos_idempotentes(self):
        call_command('carregar_exemplos', data_referencia=REFERENCIA, stdout=StringIO())
        item = Ingrediente.objects.get(nome='Farinha')
        item.meta = Decimal(21)
        item.save()
        call_command('carregar_exemplos', data_referencia=REFERENCIA, stdout=StringIO())
        self.assertEqual(Ingrediente.objects.count(), 8)
        item.refresh_from_db()
        self.assertEqual(item.meta, 21)
        resposta = self.client.get('/', {'data_referencia': '2026-09-14'})
        for linha in ['Comprar: 13 Kg de Farinha', 'Comprar: 10 L de Leite', 'Comprar: 12 Kg de Arroz', 'Comprar: 4 un de Ovos', 'Comprar: 20 Kg de Feijão', 'Comprar: 10 L de Óleo']:
            self.assertContains(resposta, linha)
        self.assertEqual(len(resposta.context['compras']), 6)
        self.assertNotContains(resposta, 'Comprar: 0')
        self.assertFalse(any(x['ingrediente'].nome in ['Sal', 'Açúcar'] for x in resposta.context['compras']))

    def test_lista_sem_compras_com_ingrediente(self):
        Ingrediente.objects.create(nome='Sal', unidade='Kg', meta=5, estoque_inicial=8, consumo=1, validade=REFERENCIA)
        self.assertContains(self.client.get('/', {'data_referencia': '2026-09-14'}), 'Nenhuma compra necessária')

    def test_data_invalida_nao_calcula_com_data_silenciosa(self):
        resposta = self.client.get('/', {'data_referencia': 'invalida'})
        self.assertContains(resposta, 'Informe uma data válida')
        self.assertNotContains(resposta, 'Comprar:')
