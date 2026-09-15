# Stock Control

**Controle de estoque e planejamento de reposição para restaurantes.**

O Stock Control organiza o cadastro de ingredientes e gera listas de compras com base no estoque disponível, no consumo do período e na validade dos produtos. Desenvolvido em Django, utiliza uma interface em HTML/CSS e persistência local em SQLite.

## Funcionalidades

- Cadastro e edição de ingredientes com unidades em Kg, L e un.
- Cálculo automático do estoque atual e da quantidade aproveitável.
- Reposição por meta, vencimento ou falta antecipada, com margem de 20% sobre o consumo.
- Consulta por data de referência e apresentação do motivo de cada compra.
- Validação dos dados no servidor e interface adaptável a diferentes tamanhos de tela.
- Dados de demonstração e testes automatizados.

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Backend | Python e Django 5.2.17 |
| Interface | Django Templates, HTML e CSS |
| Banco de dados | SQLite |
| Cálculos numéricos | Decimal |
| Testes | Framework de testes do Django |

## Instalação local

### Pré-requisitos

- **Python 3.12 ou 3.13**, com `pip` e suporte a ambientes virtuais. Baixe em [python.org](https://www.python.org/downloads/). No Windows, marque **Add python.exe to PATH** durante a instalação.
- **Git**, somente se escolher baixar o projeto pelo terminal. Também é possível baixar um ZIP pelo GitHub.
- Internet para baixar o projeto e instalar as dependências. Depois disso, a aplicação funciona localmente.

O suporte a SQLite acompanha o Python e dispensa a instalação de um servidor de banco de dados. As dependências estão fixadas em `requirements.txt`. A instalação foi validada no Windows com Python 3.12.14; as instruções para Linux e macOS estão incluídas como alternativa, sem validação nesses sistemas.

### 1. Obter o código-fonte

Escolha uma das opções:

**Com Git:** abra um terminal na pasta em que deseja guardar o projeto e execute:

```sh
git clone https://github.com/aallexandre/ControleEstoqueR.git
cd ControleEstoqueR
```

**Sem Git:** na [página do repositório](https://github.com/aallexandre/ControleEstoqueR), clique em **Code → Download ZIP**. Extraia o ZIP e abra um terminal dentro da pasta extraída, normalmente `ControleEstoqueR-main`.

Nos próximos passos, o terminal deve estar na pasta que contém **`manage.py` e `requirements.txt`**. No Windows, você pode abrir essa pasta no Explorador de Arquivos, digitar `powershell` na barra de endereço e pressionar Enter.

### 2. Preparar o ambiente e iniciar a aplicação

#### Windows — PowerShell

Na pasta do projeto, execute os comandos em sequência:

```powershell
# Cria um ambiente Python exclusivo para o projeto
py -3.12 -m venv .venv

# Instala as dependências
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Cria o banco local e suas tabelas
.\.venv\Scripts\python.exe manage.py migrate

# Opcional: adiciona oito ingredientes de demonstração
.\.venv\Scripts\python.exe manage.py carregar_exemplos

# Inicia o sistema
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Se você instalou Python 3.13, troque apenas o primeiro comando por `py -3.13 -m venv .venv`. Se o comando `py` não existir, confira a versão com `python --version` e use `python -m venv .venv` com uma das versões indicadas acima.

Esses comandos usam diretamente o Python do ambiente virtual. Não é necessário ativá-lo nem alterar a política de execução do PowerShell.

#### Linux e macOS

Com Python 3.12 ou 3.13 disponível como `python3`, execute na pasta do projeto:

```sh
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate

# Opcional: dados de demonstração
.venv/bin/python manage.py carregar_exemplos

.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Em distribuições Linux que separam o módulo `venv`, instale o pacote correspondente à sua versão do Python se a criação do ambiente informar que ele está ausente.

### 3. Acessar a aplicação

Após a inicialização do servidor, acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no navegador do mesmo computador.

## Utilização

- A página inicial usa a data atual no fuso `America/Fortaleza`. Para consultar outra data, altere **Data de referência** e clique em **Atualizar lista**.
- Clique em **Cadastrar ingrediente** para informar nome, unidade, meta, estoque inicial, consumo e validade.
- Marque **Acabou antes do fim do mês** somente quando houve falta antecipada.
- Clique no nome de um ingrediente na tabela para editar seus dados.
- A lista de compras é recalculada pelo Django. Itens sem necessidade de compra são omitidos.

O terminal deve permanecer aberto durante a execução. Para encerrar o servidor, pressione **Ctrl+C**. O aviso de servidor de desenvolvimento é esperado neste ambiente local.

### Execuções posteriores

Após a instalação inicial, execute apenas o comando de inicialização na pasta do projeto.

**Windows:**

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

**Linux/macOS:**

```sh
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Não é necessário reinstalar dependências nem carregar os exemplos a cada execução.

## Persistência e dados de demonstração

O comando `migrate` cria o arquivo **`db.sqlite3`** na pasta do projeto. Ele armazena os dados cadastrados e permanece no computador após o servidor ser encerrado.

O banco não é enviado ao GitHub. Cada instalação começa com um banco próprio; para demonstrar o sistema, execute `carregar_exemplos`. O comando adiciona oito ingredientes, usando ontem como validade dos exemplos vencidos e daqui a 30 dias para os válidos. Nomes já existentes são preservados, sem alterar valores ou validades. Se um exemplo for renomeado, uma nova execução poderá recriar o registro com o nome original.

Os exemplos incluem Farinha para reposição normal, Leite para vencimento, Arroz para falta antecipada, Ovos para arredondamento e Feijão para vencimento junto com falta antecipada. Sal e Açúcar não geram compras no cenário inicial.

### Transferência e backup

Para transferir dados entre instalações, encerre o servidor e copie o arquivo `db.sqlite3` separadamente. Faça backup do banco de destino antes de substituí-lo. O ambiente virtual `.venv` deve ser recriado em cada computador, conforme as instruções de instalação.

## Regras de negócio

O estoque atual é calculado como **estoque inicial − consumo**, antes do descarte. Estoque inicial e meta são valores independentes.

| Prioridade | Situação | Quantidade a comprar |
|---|---|---|
| 1 | Ingrediente vencido | Meta inteira; estoque aproveitável zero |
| 2 | Válido, mas acabou antes do fim do mês | Consumo real × 1,20 |
| 3 | Caso normal | Máximo entre meta − estoque atual e zero |

A saída segue o formato `Comprar: 12 Kg de Farinha`. Quantidades menores ou iguais a zero não aparecem na lista, e unidades diferentes não são somadas.

### Hipóteses e validações

- O enunciado não define a prioridade quando há vencimento e falta antecipada juntos. Foi adotado **vencimento primeiro**, pois o cliente pede a meta inteira nesse caso.
- O ingrediente é considerado válido no próprio dia da validade; vence no dia seguinte.
- Cada registro representa um ingrediente em um período e um único lote, sem entradas intermediárias ou histórico de movimentações.
- Estoque zero não prova falta antecipada; por isso essa informação é marcada explicitamente.
- O consumo é real e informado pelo usuário. A margem de 20% usa esse consumo e não altera automaticamente a meta cadastrada.
- Os cálculos usam `Decimal`. Compras em `un` são arredondadas para cima para um inteiro; Kg e L, para o centésimo superior.
- Meta, estoque inicial e consumo não podem ser negativos. Consumo não pode exceder o estoque inicial. Falta antecipada exige consumo positivo e sobra zero.
- Dados em `un` devem ser inteiros; Kg e L aceitam até duas casas decimais. Erros de preenchimento são apresentados no formulário sem salvar a alteração.

## Testes e verificação

No Windows, dentro da pasta do projeto:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test estoque
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

No Linux/macOS, substitua `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

Os 13 testes verificam as regras de negócio, arredondamento, datas, validações, cadastro, edição, proteção CSRF e a lista gerada na página. Eles usam um banco temporário, sem modificar o banco da aplicação. As datas fixas nos testes permitem repetir os resultados; não fixam a data da aplicação.

## Solução de problemas

| Mensagem ou situação | Como resolver |
|---|---|
| `py` ou `python` não reconhecido | Instale Python, confira a opção de PATH e reabra o terminal. |
| `No module named django` | Execute a instalação de `requirements.txt` com o Python da `.venv`. |
| `can't open file 'manage.py'` | Abra o terminal na pasta que contém `manage.py`. |
| `no such table: estoque_ingrediente` | Execute `manage.py migrate` com o Python da `.venv`. |
| Porta 8000 em uso | Execute `runserver 127.0.0.1:8002` e abra `http://127.0.0.1:8002/`. |
| O navegador não conecta | Confira se o terminal ainda está aberto, se o servidor iniciou e se a porta do endereço é a mesma do comando. |
| `database is locked` | Finalize edições pendentes no programa que abriu o SQLite e feche o banco nele antes de salvar pelo sistema. |

## Estrutura do projeto

| Arquivo ou pasta | Responsabilidade |
|---|---|
| `config/settings.py` | Configuração do Django e do SQLite |
| `config/urls.py` e `estoque/urls.py` | Endereços da aplicação |
| `estoque/models.py` | Modelo Ingrediente e validações entre campos |
| `estoque/forms.py` | Formulários de cadastro, edição e data de referência |
| `estoque/regras_reposicao.py` | Cálculo da compra |
| `estoque/views.py` | Recebe requisições e prepara os dados das páginas |
| `estoque/templates/estoque/` | Templates HTML |
| `estoque/static/estoque/estilo_estoque.css` | Estilos da interface |
| `estoque/migrations/` | Estrutura do banco, criada pelo comando `migrate` |
| `estoque/tests.py` | Testes automatizados |


## Aplicação publicada

A aplicação também está disponível online:

**https://controleestoquer.onrender.com**

A hospedagem utiliza Render, Gunicorn e WhiteNoise. O banco de dados continua sendo SQLite; portanto, esta publicação é adequada para demonstração, mas não deve ser considerada uma configuração de produção definitiva com armazenamento persistente.

## Escopo e execução em produção

O projeto pode ser executado localmente e também está publicado para demonstração. A configuração pública usa `DEBUG=False`, uma lista de hosts permitidos e um servidor apropriado para Django. Esta versão não inclui autenticação, exclusão de ingredientes ou histórico de movimentações.
