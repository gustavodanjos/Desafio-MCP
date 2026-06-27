# MCP Clima Desafio

Um projeto Python que demonstra o uso do Model Context Protocol (MCP) com um agente de IA construído com o framework Agno e alimentado pelo modelo da Groq.

## Estrutura do Projeto

- `server.py`: O servidor MCP (usando FastMCP) que expõe as ferramentas para consultar coordenadas e clima via Open-Meteo.
- `agent.py`: O agente construído com Agno que se conecta ao servidor MCP via `stdio` para responder a perguntas naturais sobre o clima.

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

4. **Execute o agente de demonstração:**
   ```bash
   uv run agent.py
   ```

Isso fará com que o agente inicie, inicie as ferramentas via MCP e responda a três perguntas pré-configuradas sobre o clima, exibindo todo o processo de chamadas de ferramentas no console.

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
