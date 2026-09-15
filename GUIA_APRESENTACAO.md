# Guia de apresentação

## Abertura (30 segundos)

“O Stock Control ajuda o Seu Raimundo a decidir o que comprar para o próximo mês. Cadastrei os ingredientes com meta, estoque inicial, consumo real, unidade e validade. O Django calcula a sobra e aplica as regras para gerar a lista.”

## Demonstração (3 a 5 minutos)

1. Execute os comandos do README e carregue os exemplos. Abra a página inicial, que usa a data de hoje. Os exemplos recém-criados usam ontem e daqui a 30 dias como validades. Se estiver usando registros antigos, confira as validades antes do ensaio; elas são preservadas. Para reproduzir os testes de aceitação, use a opção `--data-referencia 2026-09-14` em um banco novo e selecione essa data na tela.
2. **Reposição normal:** Farinha tem meta 20, inicial 20 e consumo 12. Sobram 8; compra 12 Kg.
3. **Vencimento:** Leite tem sobra 4 L, mas venceu. Aproveitável é zero; compra a meta inteira de 10 L.
4. **Falta antecipada:** Arroz tem meta 20, mas consumiu os 10 Kg disponíveis e acabou antes. Compra 10 × 1,20 = 12 Kg. O cálculo usa consumo, não a meta antiga.
5. Mostre Ovos: 3 × 1,20 = 3,6; arredonda para 4 un. Sal e Açúcar não aparecem na lista.
6. Clique em Farinha, tente consumo 21 e salve: o formulário mostra erro e não altera os dados. Corrija para 12 e salve.
7. Mostre Feijão: as duas condições coincidem e vence a regra da validade, comprando 20 Kg. Explique que essa prioridade é uma hipótese documentada.

## Caminho de uma requisição

**Navegador → URL → view → regra/modelo → template → navegador.**

- O navegador pede `/` com uma data de referência.
- `config/urls.py` encaminha para `estoque/urls.py`, que chama `inicio` em `views.py`.
- A view valida a data, lê `Ingrediente` no SQLite e chama `calcular_reposicao` em `regras_reposicao.py` para cada registro.
- O template `painel_estoque.html` recebe os resultados e apresenta o HTML. O CSS define a aparência. Não há cálculo de estoque no navegador.
- Ao salvar um formulário, o navegador envia POST com token CSRF. `IngredienteForm` valida os dados, incluindo as regras de `models.py`; somente depois `form.save()` grava no banco. A view redireciona para a lista.

## Ordem de estudo

1. `estoque/regras_reposicao.py`: entenda as três condições e a ordem dos `if`.
2. `estoque/models.py`: campos e propriedade `estoque_atual`.
3. `estoque/forms.py`: como os dados chegam e são validados.
4. `estoque/views.py` e `estoque/urls.py`: ligação da página com o Python.
5. `estoque/templates/estoque/painel_estoque.html`: os laços mostram o resultado do backend.
6. `estoque/tests.py`: cada exemplo testa um comportamento esperado.

## Respostas curtas para perguntas comuns

- **Por que Decimal?** Evita imprecisões de ponto flutuante em quantidades decimais.
- **Por que um campo de falta antecipada?** Sobra zero não informa em qual dia o estoque acabou.
- **Por que não guardar a sobra?** Ela deriva de inicial menos consumo; armazená-la separadamente permitiria inconsistências.
- **Por que a meta não muda?** O enunciado define a compra com margem, mas não manda persistir uma nova meta.
- **Por que SQLite/templates?** Atendem ao desafio com poucas dependências e código fácil de explicar.
- **Quais limitações?** Um período e lote por ingrediente, sem entradas intermediárias, histórico ou usuários. O foco é a reposição local.

## Antes de apresentar

Rode `manage.py check`, `manage.py test estoque` e `manage.py makemigrations --check --dry-run` com o Python do ambiente virtual. Ensaie sem depender de internet: HTML, CSS e banco estão locais. Leia as hipóteses no README e explique-as com suas próprias palavras.
