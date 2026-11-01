# Chatbot IA

Projeto em Python para aprender a usar modelos de linguagem (LLMs) por código, com a API do Gemini. Esta é a base de um chatbot que estou construindo passo a passo.

## Status

Em construção. Hoje o projeto já faz a primeira chamada a um modelo de IA, com tratamento de falhas do servidor. Próximo passo: transformar em um chatbot que conversa em loop e lembra do histórico.

## O que existe hoje

- `teste.py`: envia uma pergunta ao modelo e mostra a resposta. Se o servidor estiver sobrecarregado (erro 503), tenta de novo até 3 vezes antes de desistir.
- `listar_modelos.py`: lista os modelos disponíveis para a minha chave de API.

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
python teste.py
```

Se der erro de modelo não encontrado, rode `python listar_modelos.py` e troque o valor da constante `MODELO` no `teste.py`.

## O que eu aprendi

- **API de LLM por código:** enviar um prompt e ler a resposta (`resposta.text`).
- **Ambiente virtual (`.venv`):** isolar as bibliotecas de cada projeto.
- **Segredos fora do código:** a chave fica no `.env`, carregado com `python-dotenv`, e o `.gitignore` impede que ela vá para o GitHub.
- **Ler um traceback:** a última linha mostra o tipo de erro e as de cima mostram o caminho até ele.
- **Erro local vs erro de servidor:** `ValueError` é erro do meu código e se resolve com `try/except`. O `503` é do servidor e se ameniza com novas tentativas.
- **Retry:** repetir a chamada algumas vezes, com `time.sleep`, antes de desistir.
- **Constantes:** `MODELO`, `TENTATIVAS` e `ESPERA_SEGUNDOS` em maiúsculo, para mudar o comportamento em um só lugar.
- **Git:** conferir com `git status` o que vai no commit para não subir arquivos sensíveis.

## Próximos passos

- Chatbot com conversa em loop e memória do histórico
- Respostas em streaming
- Um segundo projeto: perguntas e respostas sobre documentos (RAG)
