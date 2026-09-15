from decimal import Decimal, ROUND_CEILING


def calcular_reposicao(ingrediente, data_referencia):
    """Recebe um ingrediente validado; devolve compra, motivo e sobra aproveitável."""
    aproveitavel = ingrediente.estoque_atual
    if ingrediente.validade < data_referencia:
        aproveitavel = Decimal('0')
        compra = ingrediente.meta
        motivo = 'Vencido'
    elif ingrediente.acabou_antes_fim_mes:
        compra = ingrediente.consumo * Decimal('1.20')
        motivo = 'Falta antecipada'
    else:
        compra = max(ingrediente.meta - aproveitavel, Decimal('0'))
        motivo = 'Reposição normal'
    precisao = Decimal('1') if ingrediente.unidade == 'un' else Decimal('0.01')
    compra = compra.quantize(precisao, rounding=ROUND_CEILING)
    return {'compra': compra, 'motivo': motivo, 'aproveitavel': aproveitavel}


def formatar_quantidade(valor):
    texto = format(valor, 'f')
    if '.' in texto:
        texto = texto.rstrip('0').rstrip('.')
    return texto.replace('.', ',')
