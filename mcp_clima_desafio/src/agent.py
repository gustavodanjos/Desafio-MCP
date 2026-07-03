import os
import asyncio
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools

load_dotenv()

async def run_agent():
    if not os.getenv("GROQ_API_KEY"):
        print("Erro: A variável de ambiente GROQ_API_KEY não foi encontrada.")
        print("Por favor, crie um arquivo .env a partir de .env.example e adicione sua chave.")
        return

    async with MCPTools(command="python src/server.py") as mcp_tools:
        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            tools=[mcp_tools],
            instructions=[
                "Você é um assistente de meteorologia inteligente.",
                "Para consultar o clima de um local, PRIMEIRO use a ferramenta 'buscar_coordenadas' para encontrar a lista de opções com aquele nome de cidade.",
                "Analise os resultados retornados. Se houver cidades com o mesmo nome em estados ou países diferentes, deduza qual o usuário quer ou pergunte se houver ambiguidade.",
                "Em seguida, use a ferramenta 'consultar_clima' informando EXATAMENTE a latitude e longitude escolhidas.",
                "Nunca invente dados climáticos. Sempre use as ferramentas antes de responder.",
                "Responda sempre em português e seja objetivo, utilizando markdown para formatar sua resposta de forma legível.",
                "Use o histórico da conversa para entender perguntas de seguimento. Se o usuário usar pronomes como 'lá' ou 'essa cidade', referencie a última cidade pesquisada.",
                "IMPORTANTE: Ao chamar ferramentas, forneça o nome exato da ferramenta e os argumentos separadamente no formato JSON correto. NUNCA concatene os argumentos no nome da ferramenta."
            ],
            markdown=True,
            session_id="sessao_chat_clima",
            read_chat_history=True
        )

        print("="*70)
        print("🌦️  Assistente de Clima Inicializado!")
        print("Sou um agente inteligente especializado em informações meteorológicas.")
        print("Posso buscar o clima atual de qualquer cidade do mundo.")
        print("\nExemplos do que você pode me perguntar:")
        print("  - Como está o clima em São Paulo agora?")
        print("  - Está mais frio em Lisboa ou em Tóquio neste momento?")
        print("  - Preciso de um casaco se eu for sair agora em Nova York?")
        print("\n(Digite 'sair' para encerrar)")
        print("="*70)
        
        while True:
            try:
                pergunta = await asyncio.to_thread(input, "\n[Você]: ")
            except (EOFError, KeyboardInterrupt):
                print("\nEncerrando o assistente...")
                break
                
            pergunta = pergunta.strip()
            if not pergunta:
                continue
                
            if pergunta.lower() in ["sair", "exit", "quit"]:
                print("Até logo!")
                break
            
            print("-" * 50)
            print("[Agente]: ", end="", flush=True)
            
            await agent.aprint_response(pergunta, stream=True)
            print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(run_agent())
