import re
from datetime import datetime


def clean_title(title: str) -> str:
    title = re.sub("<.*?>", "", title)
    title = re.sub("&quot;", '"', title)
    title = re.sub("&apos;", "'", title)
    return title


def format_pub_date(pub_date: str) -> str:
    parsed_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
    formatted_date = parsed_date.strftime("%Y/%m/%d %H:%M")
    return formatted_date
