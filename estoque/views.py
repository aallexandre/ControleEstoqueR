from urllib.parse import urlencode
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import IngredienteForm, ReferenciaForm
from .models import Ingrediente
from .regras_reposicao import calcular_reposicao, formatar_quantidade


@require_http_methods(['GET'])
def inicio(request):
    referencia = ReferenciaForm(request.GET if request.GET else None, initial={'data_referencia': timezone.localdate()})
    data = timezone.localdate()
    valido = True
    if referencia.is_bound:
        valido = referencia.is_valid()
        if valido:
            data = referencia.cleaned_data['data_referencia']
    itens = []
    compras = []
    if valido:
        for ingrediente in Ingrediente.objects.all():
            resultado = calcular_reposicao(ingrediente, data)
            resultado['ingrediente'] = ingrediente
            itens.append(resultado)
            if resultado['compra'] > 0:
                resultado['linha'] = f"Comprar: {formatar_quantidade(resultado['compra'])} {ingrediente.unidade} de {ingrediente.nome}"
                compras.append(resultado)
    return render(request, 'estoque/painel_estoque.html', {
        'referencia': referencia, 'data': data, 'valido': valido,
        'itens': itens, 'compras': compras,
    })


@require_http_methods(['GET', 'POST'])
def editar(request, pk=None):
    ingrediente = get_object_or_404(Ingrediente, pk=pk) if pk else None
    form = IngredienteForm(request.POST if request.method == 'POST' else None, instance=ingrediente)
    referencia = ReferenciaForm(request.GET)
    data = referencia.cleaned_data['data_referencia'] if referencia.is_valid() else timezone.localdate()
    voltar = reverse('estoque:inicio') + '?' + urlencode({'data_referencia': data.isoformat()})
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ingrediente salvo com sucesso.')
        return redirect(voltar)
    return render(request, 'estoque/formulario_ingrediente.html', {'form': form, 'editando': ingrediente is not None, 'voltar': voltar})
