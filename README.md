# Chatbot IA

Chatbot de terminal em Python que conversa com um modelo de linguagem (LLM) pela API do Gemini e lembra do que foi dito durante a conversa. Projeto de estudo que estou construindo passo a passo.

## O que ele faz

- Conversa em loop no terminal até digitar `sair`
- Mantém o histórico da conversa (se eu disser meu nome, ele lembra depois)
- Ignora entradas vazias (só Enter)
- Tenta de novo até 3 vezes quando o servidor está sobrecarregado (erro 503)

## Arquivos

- `chatbot.py`: o chatbot com conversa em loop e memória
- `teste.py`: a primeira chamada ao modelo, com retry
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
- **Funções:** isolei o retry na função `perguntar()`.
- **`break` e `continue`:** `break` encerra o loop, `continue` pula só a volta atual.
- **Ambiente virtual (`.venv`):** isolar as bibliotecas de cada projeto.
- **Segredos fora do código:** a chave fica no `.env`, e o `.gitignore` impede que ela vá para o GitHub.
- **Erro local vs erro de servidor:** `ValueError` é do meu código; o `503` é do servidor e se ameniza com novas tentativas.
- **Limites de um LLM:** as respostas podem ser longas demais e conter afirmações incorretas com muita confiança (alucinação), então é preciso conferir.

## Próximos passos

- Dar uma personalidade ao bot (instrução de sistema) e limitar o tamanho das respostas
- Respostas em streaming
- Segundo projeto: perguntas e respostas sobre documentos (RAG)
