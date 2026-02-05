import os
import time
import httpx

# ===== ENV =====
RAPIDAPI_KEY = os.getenv("EXERCISE_DB_API_KEY")

if not RAPIDAPI_KEY:
    raise RuntimeError("EXERCISE_DB_API_KEY is missing. Set it in Railway Variables or .env")

BASE_URL = "https://exercisedb.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "exercisedb.p.rapidapi.com",
}

# ===== simple in-memory cache =====
_CACHE = {}
CACHE_TTL = 60 * 60  # 1 hour


def _cache_valid(target: str) -> bool:
    return (
        target in _CACHE
        and (time.time() - _CACHE[target]["time"]) < CACHE_TTL
    )


async def get_exercises_by_target(target: str, limit: int = 5):
    # ---- return cache if exists ----
    if _cache_valid(target):
        return _CACHE[target]["data"][:limit]

    url = f"{BASE_URL}/exercises/target/{target}"

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, headers=HEADERS)

        # DEBUG (hapus nanti kalau sudah yakin)
        print("ExerciseDB status:", response.status_code)

        response.raise_for_status()
        data = response.json()

    # ---- save to cache ----
    _CACHE[target] = {
        "data": data,
        "time": time.time(),
    }

    return data[:limit]
