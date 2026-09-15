# Verificações executadas

Implementação verificada localmente em 13/09/2026.

## Ambiente

- Windows, Python 3.12.14, Django 5.2.17.
- Dependências instaladas a partir de `requirements.txt` em um ambiente virtual novo.
- Banco de demonstração criado com `migrate`, com oito exemplos carregados.
- Uma cópia do código sem banco foi criada para verificar migrações e os fluxos de navegador sem alterar os dados da entrega.

## Verificação automatizada

- `manage.py check`: nenhum problema identificado.
- `manage.py makemigrations --check --dry-run`: nenhuma alteração pendente.
- `manage.py test estoque --verbosity 2`: **12 testes aprovados**, incluindo subcasos dos oito exemplos e das validações.
- Os mesmos 12 testes passaram na cópia do projeto usando o ambiente virtual novo.
- Migrações aplicadas com sucesso em dois bancos inicialmente vazios.

Cobertura: reposição normal, vencimento, margem de 20%, prioridade de vencimento, omissão de itens sem compra, unidades inteiras, arredondamento de Kg/L, validade na própria data, consumo excessivo, negativos, datas inválidas, nomes vazios, unidade inválida, falta antecipada com sobra ou consumo zero, preservação de formulário e banco após erro, cadastro/edição, CSRF, método HTTP inválido, ingrediente inexistente, data de referência inválida, lista vazia e carga repetida sem sobrescrever exemplos.

## Navegador

Verificado no navegador integrado:

- Página principal com oito ingredientes e seis compras esperadas para 14/09/2026.
- Estado sem ingredientes com “Nenhuma compra necessária”, em banco separado.
- Cadastro: tentativa com consumo 21 para estoque inicial 20 exibe erro e mantém os valores.
- Correção para consumo 12 salva e exibe compra de 12 Kg.
- Edição para consumo 15 atualiza a compra para 15 Kg.
- Inspeção visual no computador e em viewport de 390 × 844, incluindo tabela e lista de compras.

Não foram executados testes em aparelhos físicos ou em todos os navegadores. A aplicação continua limitada ao modelo mensal de um único lote, conforme explicado no README.

## Entrega

Banco de demonstração preservado com os oito exemplos originais. Dados de teste de navegador ficaram na cópia de trabalho separada. Nenhuma publicação no GitHub, hospedagem ou mensagem de entrega foi realizada.


## Atualização Stock Control — 14/09/2026

- Pasta renomeada para `ControleEstoqueR`; regras, templates e CSS receberam nomes descritivos.
- Marca e frase atualizadas para Stock Control e “Estoque organizado, mês tranquilo.”
- Acesso inicial sem data fixa; novos exemplos usam datas relativas ao carregamento e aceitam `--data-referencia` para demonstrações reproduzíveis.
- 13 testes aprovados, incluindo a data atual simulada em 2027 e validades relativas.
- `check` sem problemas e `makemigrations --check --dry-run` sem mudanças.
- Comparação do banco com cópia de segurança: os nove registros foram integralmente preservados, incluindo Café e alterações do usuário.
- Página atualizada verificada no navegador em `http://127.0.0.1:8002/`. A porta 8000 ainda pertence ao servidor anterior; use o novo endereço.
