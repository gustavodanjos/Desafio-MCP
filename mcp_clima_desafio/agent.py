import os
import asyncio
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools

load_dotenv()

async def main():
    if not os.getenv("GROQ_API_KEY"):
        print("Erro: A variável de ambiente GROQ_API_KEY não foi encontrada.")
        print("Por favor, crie um arquivo .env a partir de .env.example e adicione sua chave.")
        return

    async with MCPTools(command="python server.py") as mcp_tools:
        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            tools=[mcp_tools],
            instructions=[
                "Você é um assistente de meteorologia inteligente.",
                "Sua única forma de obter informações climáticas é utilizando as ferramentas fornecidas pelo servidor MCP (consultar_clima / buscar_coordenadas).",
                "Nunca invente dados climáticos. Sempre use as ferramentas antes de responder.",
                "Responda sempre em português e seja objetivo, utilizando markdown para formatar sua resposta de forma legível."
            ],
            markdown=True
        )

        perguntas = [
            "Como está o clima em São Paulo agora?",
            "Está mais frio em Lisboa ou em Tóquio neste momento?",
            "Preciso de um casaco se eu for sair agora em Lisboa?"
        ]

        print("Iniciando bateria de perguntas ao agente...\n" + "="*50)
        
        for pergunta in perguntas:
            print(f"\n[Usuário]: {pergunta}")
            print("-" * 50)
            
            await agent.aprint_response(pergunta, stream=True)
            print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(main())
