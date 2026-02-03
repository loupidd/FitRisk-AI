import os
import httpx
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("EXERCISE_DB_API_KEY")


BASE_URL = "https://exercisedb.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "exercisedb.p.rapidapi.com",
}

async def get_exercises_by_target(target: str, limit: int = 5):
    url = f"{BASE_URL}/exercises/target/{target}"

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

    return data[:limit]
