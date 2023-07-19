import re
from datetime import datetime


def clean_title(title: str) -> str:
    title = re.sub("&quot;", '"', title)
    title = re.sub("&apos;", "'", title)
    return title


def clean_desc(desc: str) -> str:
    desc = desc.replace("<b>", "📌<b>")
    desc = re.sub("&quot;", '"', desc)
    desc = re.sub("&apos;", "'", desc)
    return desc


def format_pub_date(pub_date: str) -> str:
    parsed_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
    formatted_date = parsed_date.strftime("%Y/%m/%d %H:%M")
    return formatted_date
