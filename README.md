# Chatbot IA

Chatbot de terminal em Python que conversa com um modelo de linguagem (LLM) pela API do Gemini, lembra do que foi dito e atende como um restaurante, respondendo com base em um cardápio real.

## O que ele faz

- Conversa em loop no terminal até digitar `sair`
- Mantém o histórico da conversa (se eu disser meu nome, ele lembra depois)
- Segue uma instrução de sistema: atende como restaurante, responde em até 4 linhas e recusa assuntos fora do tema
- Usa o cardápio do arquivo `cardapio.py` como única fonte de pratos, preços, ingredientes e alergênicos
- Ignora entradas vazias (só Enter)
- Tenta de novo até 3 vezes quando o servidor está sobrecarregado (erro 503)
- Trata resposta vazia do modelo, avisando o usuário em vez de quebrar

## O problema que encontrei e como resolvi

Na primeira versão, o bot não conhecia o cardápio e **inventou pratos que não existem**: afirmou ter Cacio e Pepe, Negroni, Aperol Spritz e um sanduíche de pernil, e até descreveu a receita do Negroni. Isso é alucinação: o modelo responde com confiança sem ter base.

A correção foi colocar o cardápio real dentro da instrução de sistema e mandar o modelo usar somente ele. Rodei 5 perguntas de teste na versão nova:

| Pergunta | Resposta esperada | Resultado |
| --- | --- | --- |
| Vocês têm pizza? | Não tem | Correto |
| Quais lanches vocês recomendam? | Só o hambúrguer (único da categoria) | Correto |
| Quanto custa o bowl vegano? | R$ 34,00 | Correto |
| O hambúrguer tem glúten ou lactose? | Sim, os dois | Correto |
| Vocês têm sanduíche de pernil? | Não tem | Correto |

O sanduíche de pernil, que a primeira versão inventou, passou a ser recusado.

## Limitações conhecidas

- São só 5 testes. Isso reduz a invenção, mas não garante que ela não volte.
- Colocar o cardápio na instrução funciona porque ele tem 4 itens. Para documentos grandes, o caminho é buscar só os trechos relevantes (RAG).
- O bot repete "Olá!" no começo de quase toda resposta.
- Uma resposta vazia do modelo aconteceu uma vez, sem erro de servidor, e não consegui confirmar a causa. O programa trata o caso.
- A saída de um LLM às vezes sai com defeitos (palavras coladas ou cortadas), então não deve ser tratada como sempre correta.
- As informações de alergênicos vêm de um cardápio de exemplo e não devem ser usadas para decisões reais sobre alergias.
- Não há streaming: a resposta só aparece depois de pronta.

## Arquivos

- `chatbot.py`: o chatbot
- `cardapio.py`: os dados do cardápio (lista de dicionários)
- `exemplo_api.py`: a primeira chamada ao modelo, com retry
- `listar_modelos.py`: lista os modelos disponíveis para a minha chave

## Como rodar

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
```

2. Instale as dependências:

```bash
pip install google-genai python-dotenv
```

3. Pegue uma chave de API gratuita no Google AI Studio (aistudio.google.com) e crie um arquivo `.env` na pasta do projeto com esta linha:

```
GEMINI_API_KEY=sua_chave_aqui
```

O arquivo `.env` está no `.gitignore` e nunca deve ser enviado ao GitHub.

4. Execute:

```bash
python chatbot.py
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
