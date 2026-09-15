from django import forms
from .models import Ingrediente


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nome', 'unidade', 'meta', 'estoque_inicial', 'consumo', 'validade', 'acabou_antes_fim_mes']
        widgets = {'validade': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})}
        help_texts = {
            'meta': 'Quantidade desejada para a reposição.',
            'estoque_inicial': 'Quantidade disponível no início do período.',
            'consumo': 'Consumo real, limitado ao estoque inicial.',
            'validade': 'Um único lote. Válido até esta data, inclusive.',
            'acabou_antes_fim_mes': 'Marque somente se faltou antes do mês terminar e a sobra é zero.',
        }


class ReferenciaForm(forms.Form):
    data_referencia = forms.DateField(label='Data de referência', widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
