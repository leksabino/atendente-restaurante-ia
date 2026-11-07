# Atendente de restaurante com IA

Agente em Python que atende pedidos de um restaurante pelo terminal. Ele usa a API do Gemini com **function calling**: consulta o cardápio em um banco **SQLite**, monta o pedido e informa o total, que é calculado em código e não pelo modelo.

## O problema que encontrei e como evoluiu

Minha primeira versão (`chatbot.py`) era um chatbot com o cardápio colado na instrução de sistema. Antes disso, sem cardápio nenhum, o bot **inventou pratos que não existem**: afirmou ter Cacio e Pepe, Negroni, Aperol Spritz e um sanduíche de pernil, e até descreveu a receita do Negroni. Isso é alucinação: o modelo responde com confiança sem ter base.

Colocar o cardápio na instrução resolveu nos 5 testes que fiz à mão, mas não escala e não garante nada. Nesta versão, em vez de pedir que o modelo "lembre" do cardápio, dou a ele **ferramentas** para consultar os dados reais, e o total do pedido passa pelo meu código.

Durante o desenvolvimento, o agente ainda errou de duas formas, e cada uma virou uma correção:

- **Busca falhava com acento** (`hamburguer` x `hambúrguer`) e com palavras fora de ordem (`suco de laranja`). O modelo remendava chamando `listar_pratos`, mas corrigi a ferramenta em vez de depender disso.
- **Inventou uma política de pagamento:** disse que o cartão seria cobrado "na entrega ou na retirada", sem nenhuma fonte. Acrescentei à instrução que ele não tem informações de pagamento, entrega e horários, e criei casos de teste para isso.

## O que ele faz

- Conversa em loop no terminal e mantém o histórico (`sair` encerra)
- Consulta pratos, preços, ingredientes e alergênicos no SQLite
- Busca por nome ignorando acentos e maiúsculas, e por várias palavras em qualquer ordem
- Filtra pratos por dieta (vegano, vegetariano)
- Monta o pedido (adicionar itens, ver itens e total)
- Calcula o total em **centavos inteiros**, sem erro de arredondamento
- Recusa assuntos fora do restaurante e não inventa regras de pagamento, entrega ou horário
- Ignora entradas vazias (só Enter)
- Tenta de novo até 3 vezes quando o servidor devolve erro 503

## Como funciona

```
cardapio.py ──> banco.py ──> restaurante.db
                                  │
                         consultas.py, pedido.py   (ferramentas)
                                  │
                    atendente.py  ⇄  API do Gemini
```

O modelo recebe a descrição de cada ferramenta (a docstring da função), decide quando chamar e usa o resultado para responder. O pedido e o total passam sempre pelo meu código.

## Como medi se funciona

O `avaliador.py` roda perguntas pré-definidas contra o agente, cada uma em uma conversa nova, e confere se a resposta contém ou não certas palavras. Cada falha real que encontrei virou um caso de teste permanente.

```bash
python avaliador.py
```

Resultado nas 3 execuções que fiz: 7/7, 7/7 e 9/9 casos corretos.

## Decisões técnicas

- **Preço em centavos (inteiro):** guardo 3800 em vez de 38.0 porque número decimal (`float`) pode dar erro de arredondamento em contas. Só converto para reais na hora de mostrar.
- **Total calculado em código:** o modelo de linguagem pode errar conta ou inventar um valor. O meu código soma sempre do mesmo jeito. O modelo só chama a ferramenta e conta o resultado ao cliente.
- **Erros devolvidos como dado (`{"erro": ...}`):** quando o id não existe ou a quantidade é inválida, a função devolve o erro em vez de quebrar. Assim o modelo lê o problema, explica ao cliente e o programa continua.
- **Docstring como descrição da ferramenta:** o modelo só sabe o que uma função faz pela descrição que escrevo nela. Uma descrição ruim faz ele chamar a função errada ou na hora errada.
- **Corrigir a ferramenta em vez de confiar no modelo:** a busca sem acento e a busca por palavras faziam o modelo chamar `listar_pratos` para remendar uma busca que falhava. Corrigi a busca em vez de depender disso.

## Limitações conhecidas

- São poucos casos de teste, e a conferência é por palavras-chave, então uma resposta errada pode passar se contiver as palavras esperadas. O resultado pode variar entre execuções, porque o modelo não responde sempre igual.
- O pedido fica em memória: se o programa fecha, ele se perde, e só atende uma conversa por vez. A evolução natural é gravar o pedido numa tabela do SQLite ligada a uma sessão.
- O cardápio tem 4 itens. Para documentos grandes, o caminho seria buscar só os trechos relevantes (RAG).
- Não há ferramenta de filtro por alergênico: o agente responde perguntas como "sem lactose" lendo os dados sozinho.
- Os alergênicos vêm de um cardápio de exemplo e **não devem ser usados para decisões reais** sobre alergias.
- Uma resposta vazia do modelo aconteceu uma vez, sem erro de servidor, e não consegui confirmar a causa. O programa trata o caso.
- A saída de um LLM às vezes sai com defeitos (palavras coladas ou cortadas), então não deve ser tratada como sempre correta.
- Não há streaming: a resposta só aparece depois de pronta.

## Arquivos

- `atendente.py`: o chat em loop com o Gemini e as ferramentas
- `cardapio.py`: dados de origem do cardápio (lista de dicionários)
- `banco.py`: cria o SQLite a partir do cardápio
- `consultas.py`: ferramentas de leitura (listar, buscar, filtrar por dieta)
- `pedido.py`: ferramentas do pedido (adicionar, ver total)
- `avaliador.py`: casos de teste do agente
- `agente.py`: exemplo mínimo de function calling
- `chatbot.py`: primeira versão, com o cardápio na instrução de sistema
- `exemplo_api.py`: a primeira chamada ao modelo, com retry
- `listar_modelos.py`: lista os modelos disponíveis para a minha chave
- `testar_consultas.py`, `testar_pedido.py`: testes manuais das funções

## Como rodar

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Pegue uma chave de API gratuita no Google AI Studio (aistudio.google.com) e crie um arquivo `.env` na pasta do projeto com esta linha:

```
GEMINI_API_KEY=sua_chave_aqui
```

O arquivo `.env` está no `.gitignore` e nunca deve ser enviado ao GitHub.

4. Crie o banco (ele é gerado localmente e não vai para o GitHub):

```bash
python banco.py
```

5. Execute o atendente:

```bash
python atendente.py
```

Se der erro de modelo não encontrado, rode `python listar_modelos.py` e troque o valor da constante `MODELO` no código.

## O que eu aprendi

- **API de LLM por código:** enviar um prompt e ler a resposta.
- **Memória de conversa:** o objeto `chat` guarda o histórico e reenvia a cada mensagem.
- **Instrução de sistema:** regra que vale durante toda a conversa, diferente da pergunta do usuário, que muda a cada mensagem.
- **Alucinação e como reduzi:** dar ao modelo os dados reais e mandá-lo usar só eles.
- **Funções:** isolei o retry na função `perguntar()` e a montagem do cardápio em `montar_cardapio()`.
- **`break` e `continue`:** `break` encerra o loop, `continue` pula só a volta atual.
- **Ordem do código:** o Python lê de cima para baixo, então uma variável precisa existir antes de ser usada (aprendi com um `NameError`).
- **Ambiente virtual (`.venv`):** isolar as bibliotecas de cada projeto.
- **Segredos fora do código:** a chave fica no `.env`, e o `.gitignore` impede que ela vá para o GitHub.
- **Erro local vs erro de servidor:** `ValueError` é do meu código; o `503` é do servidor e se ameniza com novas tentativas.
- **SQLite:** guardar o cardápio em banco, inserir com `?` (seguro contra SQL injection) e consultar com `SELECT`.
- **Function calling:** o modelo decide qual função chamar a partir do nome e da docstring, e a função precisa de *type hints*.
- **Dinheiro em centavos:** inteiros não têm o erro de arredondamento do `float`.
- **Avaliar um agente:** medir uma taxa de acerto com casos de teste, e transformar cada falha real em um caso novo.