import requests
from typing import List, Dict, Any

STEAM_API_URL = "https://store.steampowered.com/api/appdetails"

def get_game_info(appid: int, region: str = "ru", language: str = "en") -> Dict[str, Any]:
    params = {
        "appids": appid,
        "cc": region,
        "l": language
    }

    try:
        response = requests.get(STEAM_API_URL, params=params, timeout=10)
        data = response.json()

        if not data.get(str(appid), {}).get("success"):
            return {
                "appid": appid,
                "region": region,
                "break": True,
                "message": "Game not found"
            }

        game_data = data[str(appid)]["data"]
        price_info = game_data.get("price_overview")

        result = {
            "appid": appid,
            "region": region,
            "name": game_data.get("name", "Unknown"),
            "available": True,
            "is_free": game_data.get("is_free", False),
            "currency": price_info.get("currency") if price_info else None,
            "initial_price": price_info.get("initial") / 100 if price_info else None,
            "final_price": price_info.get("final") / 100 if price_info else None,
            "discount_percent": price_info.get("discount_percent") if price_info else 0,
            "platforms": game_data.get("platforms", {}),
            "release_date": game_data.get("release_date", {}).get("date")
        }
        return result

    except Exception as e:
        return {
            "appid": appid,
            "region": region,
            "available": False,
            "error": str(e)
        }

def get_info_across_regions(appid: int, regions: List[str]) -> List[Dict[str, Any]]:
    all_data = []
    for region in regions:
        info = get_game_info(appid, region)
        all_data.append(info)
    return all_data
