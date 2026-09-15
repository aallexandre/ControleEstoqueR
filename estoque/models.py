from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Ingrediente(models.Model):
    nome = models.CharField('Nome', max_length=100)
    unidade = models.CharField('Unidade', max_length=2, choices=[('Kg', 'Kg'), ('L', 'L'), ('un', 'un')])
    meta = models.DecimalField('Meta de reposição', max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    estoque_inicial = models.DecimalField('Estoque inicial', max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    consumo = models.DecimalField('Consumo do período', max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    validade = models.DateField('Validade')
    acabou_antes_fim_mes = models.BooleanField('Acabou antes do fim do mês', default=False)

    class Meta:
        ordering = ['nome', 'pk']

    @property
    def estoque_atual(self):
        return self.estoque_inicial - self.consumo

    def clean(self):
        errors = {}
        if not self.nome or not self.nome.strip():
            errors['nome'] = 'Informe o nome do ingrediente.'
        else:
            self.nome = self.nome.strip()
        quantities = ('meta', 'estoque_inicial', 'consumo')
        for field in quantities:
            value = getattr(self, field)
            if isinstance(value, Decimal) and self.unidade == 'un' and value != value.to_integral_value():
                errors[field] = 'Para un, informe uma quantidade inteira.'
        if self.consumo is not None and self.estoque_inicial is not None:
            if self.consumo > self.estoque_inicial:
                errors['consumo'] = 'O consumo não pode ultrapassar o estoque inicial.'
            if self.acabou_antes_fim_mes and (self.consumo <= 0 or self.estoque_atual != 0):
                errors['acabou_antes_fim_mes'] = 'Para falta antecipada, o consumo deve ser positivo e a sobra deve ser zero.'
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.nome
