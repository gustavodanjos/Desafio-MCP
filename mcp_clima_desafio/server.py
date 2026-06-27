import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Servidor de Clima")


@mcp.tool()
async def buscar_coordenadas(cidade: str) -> dict:
    """Busca a latitude e longitude de uma cidade através da API Open-Meteo.
    Args:
        cidade: O nome da cidade.
    Returns:
        Um dicionário contendo as coordenadas da cidade.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": cidade, "count": 1, "language": "pt", "format": "json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            resultado = data["results"][0]
            return {
                "cidade": resultado.get("name"),
                "lat": resultado.get("latitude"),
                "lon": resultado.get("longitude"),
                "pais": resultado.get("country"),
            }
        else:
            return {"erro": f"Coordenadas para a cidade '{cidade}' não encontradas."}


@mcp.tool()
async def consultar_clima(cidade: str) -> dict:
    """Consulta o clima atual de uma cidade (temperatura, umidade e vento) usando as coordenadas.
    Args:
        cidade: O nome da cidade.
    Returns:
        Um dicionário contendo as informações do clima.
    """
    coords = await buscar_coordenadas(cidade)

    if "erro" in coords:
        return coords

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        current = data.get("current", {})

        return {
            "cidade": coords["cidade"],
            "pais": coords["pais"],
            "temperatura_c": current.get("temperature_2m"),
            "umidade_pct": current.get("relative_humidity_2m"),
            "vento_kmh": current.get("wind_speed_10m"),
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")
