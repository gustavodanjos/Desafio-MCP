import asyncio
from src.agent import run_agent

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\nPrograma finalizado pelo usuário.")
