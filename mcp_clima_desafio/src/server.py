import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Servidor de Clima")


@mcp.tool()
async def buscar_coordenadas(cidade: str) -> list[dict]:
    """Busca as coordenadas (latitude e longitude) de cidades pelo nome. Pode retornar múltiplos resultados se houver cidades com o mesmo nome em estados/países diferentes.
    Args:
        cidade: O nome da cidade.
    Returns:
        Uma lista de dicionários contendo informações das cidades encontradas.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": cidade, "count": 5, "language": "pt", "format": "json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            resultados = []
            for res in data["results"]:
                resultados.append({
                    "cidade": res.get("name"),
                    "estado_ou_regiao": res.get("admin1", "N/A"),
                    "pais": res.get("country", "N/A"),
                    "lat": res.get("latitude"),
                    "lon": res.get("longitude")
                })
            return resultados
        else:
            return [{"erro": f"Nenhuma cidade encontrada para '{cidade}'."}]


@mcp.tool()
async def consultar_clima(latitude: float, longitude: float, nome_cidade: str = "") -> dict:
    """Consulta o clima atual de uma localização exata usando sua latitude e longitude.
    Args:
        latitude: A latitude exata.
        longitude: A longitude exata.
        nome_cidade: (Opcional) O nome da cidade ou local para constar na resposta.
    Returns:
        Um dicionário contendo as informações do clima.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        current = data.get("current", {})

        return {
            "cidade": nome_cidade,
            "temperatura_c": current.get("temperature_2m"),
            "umidade_pct": current.get("relative_humidity_2m"),
            "vento_kmh": current.get("wind_speed_10m"),
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")
