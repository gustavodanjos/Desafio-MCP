# MCP Clima Desafio

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Agno](https://img.shields.io/badge/Agno-Agent-FF4B4B?logo=ai&logoColor=white)](https://github.com/agno-ai/agno)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?logo=groq&logoColor=white)](https://groq.com/)
[![FastMCP](https://img.shields.io/badge/FastMCP-Server-009688?logo=fastapi&logoColor=white)](https://github.com/jlowin/fastmcp)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9?logo=python&logoColor=white)](https://github.com/astral-sh/uv)
[![Open-Meteo](https://img.shields.io/badge/Open--Meteo-Weather%20API-00B0FF?logo=wechat&logoColor=white)](https://open-meteo.com/)

Um projeto Python que demonstra o uso do Model Context Protocol (MCP) com um agente de IA construído com o framework Agno e alimentado pelo modelo da Groq.

## Estrutura do Projeto

- `src/server.py`: O servidor MCP (usando FastMCP) que expõe as ferramentas para consultar coordenadas com suporte a múltiplos resultados e consulta de clima exata via Open-Meteo (lat/lon).
- `src/agent.py`: O agente interativo construído com Agno que se conecta ao servidor MCP via `stdio`. Ele possui memória de sessão para conversas contínuas e capacidade de raciocínio avançado usando o modelo da Groq.
- `main.py`: O ponto de entrada da aplicação, responsável por iniciar o assistente interativo no terminal.

## Configuração e Execução

### Pré-requisitos
- Python 3.10 ou superior.
- Gerenciador de pacotes `uv` instalado.

### Passos

1. **Clone o projeto ou entre no diretório.**

2. **Configure sua Chave de API:**
   Renomeie ou copie o arquivo `.env.example` para `.env` e preencha com sua chave do Groq:
   ```bash
   cp .env.example .env
   ```
   *Edite o arquivo `.env` com a sua `GROQ_API_KEY` real (pode ser obtida em https://console.groq.com).*

3. **Instale as dependências com `uv`:**
   ```bash
   uv sync
   ```

4. **Execute o assistente interativo:**
   ```bash
   uv run main.py
   ```

Isso fará com que o agente inicie um chat interativo no seu terminal. Você pode fazer perguntas complexas, consultar o clima em várias cidades pelo mundo e realizar perguntas de seguimento, com o agente utilizando as ferramentas MCP por baixo dos panos!

## Comparação com os demais protocolos

| Protocolo | Por que não é ideal aqui |
| :--- | :--- |
| **MQTT** | Desenvolvido para padrão *pub/sub* assíncrono entre muitos dispositivos via broker. Neste projeto, a interação é um *request/response* pontual, sem necessidade ou justificativa para um broker intermediário. |
| **CoAP** | Otimizado especificamente para dispositivos IoT embarcados com severas restrições de energia e memória. Nosso agente e servidor rodam em ambiente computacional normal, sem essas restrições. |
| **AMQP** | Focado em mensageria corporativa com filas e garantias complexas de entrega. O uso de AMQP traria um overhead arquitetural desnecessário para chamadas simples sob demanda. |
| **HTTP puro** | Embora pudesse resolver a chamada de API, o HTTP por si só não padroniza a forma como um agente de IA descobre e invoca ferramentas de maneira uniforme, exigindo lógica customizada. O MCP constrói essa padronização e descoberta dinâmica nativamente. |

### Justificativa para a escolha do MCP no cenário

O MCP (Model Context Protocol) foi projetado de forma específica para conectar agentes de IA a ferramentas externas (como APIs). Considerando os requisitos deste projeto:

- **Frequência de comunicação:** As interações são pontuais e sob demanda (acionadas apenas quando o usuário faz uma pergunta), o que se adequa perfeitamente ao modelo RPC do MCP, sem a necessidade de conexões sempre ativas enviando telemetria.
- **Quantidade de dispositivos envolvidos:** O projeto lida com comunicação direta entre poucos componentes lógicos (o agente cliente e o servidor local MCP), descartando a necessidade de protocolos criados para orquestrar milhares de nós.
- **Necessidade de baixa latência:** Como o MCP está rodando localmente (via transporte `stdio`), a latência na chamada de ferramentas é praticamente nula, o que é vital para não atrasar a geração de respostas do LLM.
- **Consumo de banda/energia:** O sistema opera em ambientes de desktop ou servidor, onde as restrições severas de bateria ou banda (que justificariam protocolos como CoAP) não existem.
- **Confiabilidade de entrega:** O canal de comunicação direto síncrono garante retorno imediato das execuções, sem requerer a robustez de sistemas de filas com garantias de persistência de mensagens como o AMQP.
- **Escalabilidade (de contexto):** O MCP foca na escalabilidade da integração da IA: ele oferece *descoberta dinâmica* de ferramentas e *schemas tipados*. Qualquer servidor MCP desenvolvido pode ser reutilizado integralmente por diversos outros agentes ou interfaces de IA padronizadas, alavancando a escalabilidade do sistema em termos de funcionalidades e integrações.

## Histórico de entregas
   - **Avaliação 1** (26/06/2026): commit `5d984cb`
   - **Avaliação opcional / Semana de TCC** (03/07/2026): commit `babc6a1`
