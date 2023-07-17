import aiohttp
import urllib.parse


async def fetch_naver_news_json(
    query: str, base_url: str, client_id: str, client_secret: str
) -> dict:
    encoded_query = urllib.parse.quote(query)
    url = base_url + f"?query={encoded_query}" + "&display=100&sort=date"
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_body = await response.json()
    return response_body
