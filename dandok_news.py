import asyncio
import json
import os
import telegram
import time
import logging

from typing import List
from logging.handlers import RotatingFileHandler

from utils import clean_title, format_pub_date
from network import fetch_naver_news_json
from dotenv import load_dotenv


load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=bot_token)
chat_id = os.getenv("CHAT_ID")

base_url = "https://openapi.naver.com/v1/search/news.json"
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

query_list = ["단독"]

old_dandok_list = []

# Logger 설정 및 로그 파일 핸들러 생성

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = RotatingFileHandler("error.log", maxBytes=100000, backupCount=5)
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def log_exception(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception("An error occurred")
            raise

    return wrapper


def filter_old_news(old_dandok_list: List[dict]) -> List[dict]:
    print("단독 기사 목록 필터링 중...")
    current_time = time.time()
    filtered_list = [
        old_news
        for old_news in old_dandok_list
        if current_time - old_news["timestamp"] <= 48 * 3600
    ]
    del_cnt = len(old_dandok_list) - len(filtered_list)
    print(f"{del_cnt}개 삭제")
    return filtered_list


async def get_dandok_list(query_list: List[str]) -> List[dict]:
    print("단독 기사 검색 중...")
    tasks = [
        fetch_naver_news_json(query, base_url, client_id, client_secret)
        for query in query_list
    ]
    responses = await asyncio.gather(*tasks)

    dandok_list = []
    for response in responses:
        news_items_list = response.get("items", [])
        for news in news_items_list:
            title = clean_title(news.get("title", ""))
            if "[단독]" in title:
                link = news.get("originallink") or news.get("link")
                pub_date = news.get("pubDate")
                formatted_date = format_pub_date(pub_date)
                item = {
                    "title": title,
                    "link": link,
                    "pubDate": formatted_date,
                    "timestamp": time.time(),
                }
                dandok_list.append(item)
    return dandok_list


@log_exception
async def process_dandok_news():
    global bot, chat_id, old_dandok_list

    print("#" * 18)

    # 이전 기사 목록 가져오기
    old_dandok_list = []
    if os.path.exists("old_dandok_list.json"):
        with open("old_dandok_list.json", "r", encoding="utf-8") as f:
            old_dandok_list = json.load(f)

    old_dandok_list = filter_old_news(old_dandok_list)

    # 단독 기사 목록 가져오기
    dandok_list = await get_dandok_list(query_list)
    dandok_list = dandok_list[::-1]

    # 새로운 단독 기사 목록 필터링
    old_dandok_title_set = {old_dandok["title"] for old_dandok in old_dandok_list}
    new_dandok_list = [
        dandok for dandok in dandok_list if dandok["title"] not in old_dandok_title_set
    ]

    print(f"총 {len(new_dandok_list)}개 단독 기사 검색")

    # 단독 기사 메시지 송신
    for new_dandok in new_dandok_list:
        text = f'{new_dandok["pubDate"]}\n{new_dandok["title"]}\n{new_dandok["link"]}'
        await bot.send_message(chat_id=chat_id, text=text)

    # 이전 기사 목록 갱신
    old_dandok_list += new_dandok_list
    old_dandok_list.sort(key=lambda x: x["timestamp"], reverse=True)

    # 기사 목록 저장
    with open("old_dandok_list.json", "w", encoding="utf-8") as f:
        json.dump(old_dandok_list, f, ensure_ascii=False)

    print(f"마지막 갱신: {time.time()}")


async def main() -> None:
    global query_list
    await bot.send_message(chat_id=chat_id, text="검색어 목록입니다:")
    for query in query_list:
        await bot.send_message(chat_id=chat_id, text=query)

    while True:
        await process_dandok_news()
        await asyncio.sleep(60 * 5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
