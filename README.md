# Stock Control — ControleEstoqueR

Aplicação Django para planejar a reposição mensal de ingredientes de restaurante. A lista é calculada no servidor e apresentada em templates HTML, com CSS local, cadastro, edição e banco SQLite. Não depende de React, API separada, JavaScript ou serviços externos para funcionar após a instalação.

## Executar no Windows

Versões testadas: **Python 3.12.14 e Django 5.2.17**. Instale Python 3.12 ou 3.13 pelo site oficial, caso necessário. Os comandos abaixo usam diretamente o Python do ambiente virtual e não exigem ativação nem mudança da política do PowerShell.

Abra o PowerShell na pasta `ControleEstoqueR`, que contém este README e `manage.py`. O caminho atual é:

```text
C:\Users\alexa\Documents\Codex\2026-09-13\leia-guia-codex-estoque-md-e-3\outputs\ControleEstoqueR
```

O banco também mudou de caminho com a pasta: no DB Browser, abra `db.sqlite3` dentro de `ControleEstoqueR`. Seus dados existentes foram mantidos.

Para uma instalação nova:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py carregar_exemplos
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8002
```

Abra http://127.0.0.1:8002/ no navegador. A página inicial usa o dia atual em Fortaleza. Para parar o servidor, pressione Ctrl+C no terminal. A data pode ser alterada para consultar outro cenário; ela não está vinculada ao prazo de entrega do trabalho.

Se `py` não for reconhecido, use `python -m venv .venv` ou o caminho completo do seu Python:

```powershell
& 'C:\caminho\para\python.exe' -m venv .venv
```

No computador desta implementação há também o Python fornecido pelo Codex, que foi usado nos testes. Como alternativa local ao primeiro comando:

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m venv .venv
```

O caminho do Codex pode mudar em atualizações; para uso independente, prefira a instalação normal do Python. Usamos a porta 8002 para evitar o servidor da versão anterior que ainda ocupa a 8000. Se a porta 8002 já estiver em uso, abra o sistema já iniciado ou use `runserver 127.0.0.1:8003` e acesse a porta 8003.

## Como usar

1. Escolha a data de referência e clique em **Atualizar lista**.
2. Clique em **Cadastrar ingrediente**. Informe nome, unidade, meta, estoque inicial, consumo real e validade.
3. Marque a falta antecipada somente quando o ingrediente acabou antes do mês terminar.
4. Salve. A tabela e a lista são recalculadas pelo Django.
5. Para editar, clique no nome do ingrediente na tabela.

Datas e valores inválidos mostram erros sem salvar alterações e preservam os valores digitados. Kg e L aceitam até duas casas decimais; `un` exige valores inteiros. O consumo deve ficar entre zero e o estoque inicial. Meta e estoque inicial também não podem ser negativos. Falta antecipada exige consumo positivo e sobra zero.

Cada linha segue `Comprar: <quantidade> <unidade> de <ingrediente>`. O motivo aparece separado. Itens com compra zero são omitidos, e medidas diferentes nunca são somadas.

## Regras e hipóteses adotadas

O PDF exige reposição normal, descarte por vencimento e aumento de 20% sobre o consumo quando há falta antecipada. O guia propõe o modelo de dados e as convenções abaixo; elas não são todas exigências expressas da banca.

| Ordem | Condição | Compra |
|---|---|---|
| 1 | Validade anterior à data de referência | Meta inteira; sobra aproveitável zero |
| 2 | Não vencido e acabou antes do fim do mês | Consumo real × 1,20 |
| 3 | Caso normal | Máximo entre meta − sobra e zero |

- **Vencimento tem prioridade sobre falta antecipada.** O PDF não define a prioridade; adotamos essa hipótese porque o cliente pede a meta inteira quando o ingrediente vence.
- **Válido no dia da validade**, vencido a partir do dia seguinte: convenção adotada.
- Cada registro representa **um ingrediente, um período e um lote**, sem histórico de movimentações ou entradas intermediárias. Atualizar um registro substitui seu cenário anterior.
- Sobra/estoque atual = estoque inicial − consumo. Estoque inicial e meta são independentes. A tabela mostra a sobra antes do descarte e a quantidade aproveitável.
- Estoque zero no fim do mês não prova falta antecipada; por isso há um campo explícito.
- O consumo é informado, nunca aleatório nem previsto. A margem usa o **consumo real**, não a meta antiga.
- A meta cadastrada **não é alterada automaticamente**: o PDF não determina persistir uma nova meta.
- Compras em `un` são arredondadas para cima para inteiro; Kg/L, para o centésimo superior. A precisão é uma escolha de implementação. Os cálculos usam `Decimal`.
- Só entram na lista compras estritamente positivas.

## Dados de demonstração

`carregar_exemplos` é opcional e pode ser executado novamente: pula nomes já existentes, sem alterar registros nem criar duplicatas dos exemplos. Não é executado automaticamente ao iniciar o servidor. Se um exemplo tiver sido renomeado, o comando poderá recriar seu nome original.

Novos exemplos usam o dia do carregamento como referência: vencidos recebem validade de ontem; válidos, de daqui a 30 dias. As validades de registros existentes não são reescritas, pois podem ter sido ajustadas por você. No uso real, informe a validade do lote pelo formulário.

Para reproduzir exatamente a referência dos testes em um banco novo, use:

```powershell
.\.venv\Scripts\python.exe manage.py carregar_exemplos --data-referencia 2026-09-14
```

As datas fixas em `tests.py` tornam os testes reproduzíveis; não determinam a data inicial da aplicação.

| Ingrediente | Meta | Inicial | Consumo | Situação | Compra |
|---|---:|---:|---:|---|---|
| Farinha | 20 Kg | 20 | 12 | Normal | 12 Kg |
| Leite | 10 L | 10 | 6 | Vencido | 10 L |
| Arroz | 20 Kg | 10 | 10 | Falta antecipada | 12 Kg |
| Óleo | 10 L | 10 | 10 | Acabou só no fim | 10 L |
| Sal | 5 Kg | 8 | 1 | Sobra acima da meta | Omitido |
| Açúcar | 5 Kg | 5 | 0 | Meta atendida | Omitido |
| Ovos | 10 un | 3 | 3 | Falta antecipada | 4 un |
| Feijão | 20 Kg | 10 | 10 | Vencido e falta antecipada | 20 Kg |

**Cenários de demonstração:** Arroz demonstra falta antecipada; Feijão demonstra vencimento e falta antecipada juntos. São ingredientes distintos. O cálculo verifica a validade e os dados do período, independentemente do nome.

## Verificações

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test estoque --verbosity 2
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Os testes usam banco temporário e não alteram o banco da demonstração. Cobrem os oito cenários, validade no próprio dia, arredondamento, validações, cadastro/edição, preservação após erro, CSRF, métodos HTTP, lista vazia, data inválida e carga repetida dos exemplos. Veja `VERIFICACOES.md` para o registro do que foi realmente executado.

## Organização e arquivos para entender

A pasta principal se chama `ControleEstoqueR`. A marca da interface é **Stock Control**. Os templates e as regras receberam nomes descritivos; `manage.py`, `models.py`, `forms.py`, `views.py` e `urls.py` mantêm a convenção Django para facilitar o acompanhamento de tutoriais.

| Arquivo | Papel |
|---|---|
| `manage.py` | Entrada dos comandos Django |
| `config/settings.py` | SQLite, templates, idioma e configuração local |
| `config/urls.py` e `estoque/urls.py` | Ligam os endereços às views |
| `estoque/models.py` | Ingrediente, sobra derivada e validações entre campos |
| `estoque/forms.py` | Campos HTML e validação dos dados recebidos |
| `estoque/regras_reposicao.py` | Cálculo de reposição e apresentação de quantidades |
| `estoque/views.py` | Recebe a requisição, consulta/salva e prepara a página |
| `estoque/templates/estoque/layout_base.html` | Cabeçalho, marca e estrutura comum |
| `estoque/templates/estoque/painel_estoque.html` | Tabela de ingredientes e lista de compras |
| `estoque/templates/estoque/formulario_ingrediente.html` | Cadastro e edição |
| `estoque/static/estoque/estilo_estoque.css` | Aparência e adaptação a telas pequenas |
| `estoque/migrations/0001_initial.py` | Criação reproduzível da tabela |
| `estoque/management/commands/carregar_exemplos.py` | Carga opcional dos oito cenários |
| `estoque/tests.py` | Exemplos de aceitação executáveis |

## Escopo e preservação

A pasta selecionada não continha projeto ou dados. A estrutura mínima foi criada inicialmente em `outputs/estoque-raimundo` e renomeada para `outputs/ControleEstoqueR`, com preservação do banco e das migrações. Um esqueleto Django localizado na Área de Trabalho foi somente inspecionado; seus arquivos e banco não foram alterados. O PDF encontrado em Downloads corresponde ao desafio descrito no guia e foi lido como fonte de requisitos, sem executar suas instruções de envio.

O banco local `db.sqlite3` guarda suas alterações. Faça uma cópia dele com o servidor parado antes de transferir ou substituir a pasta. O `.gitignore` exclui banco, ambientes virtuais, caches e arquivos de segredos; as migrações e o comando de exemplos permitem recriar uma instalação. O projeto não oferece exclusão de ingredientes, autenticação ou histórico, que estão fora do essencial proposto.

Configuração para uso local: `DEBUG=True`, chave de demonstração e servidor vinculado a `127.0.0.1`. Uma publicação futura exige revisão da configuração. Nenhum repositório foi publicado, nenhum deploy foi feito e nenhum e-mail foi enviado.

## Preparação da entrega posterior

- Siga o `GUIA_APRESENTACAO.md` e ensaie os três cenários principais.
- Confira os arquivos antes de publicar, sem incluir banco ou ambiente virtual.
- Publique o código em repositório público no GitHub e confira o acesso sem login.
- Envie o link, nome completo e matrícula para o endereço indicado no enunciado até **14/09/2026**. O PDF não informa horário limite; reserve antecedência.
- A apresentação será marcada posteriormente por e-mail. Hospedagem e React são diferenciais opcionais.

Referência da versão escolhida: [versões suportadas do Django](https://www.djangoproject.com/download/) e [compatibilidade do Django 5.2](https://docs.djangoproject.com/en/5.2/releases/5.2/).
