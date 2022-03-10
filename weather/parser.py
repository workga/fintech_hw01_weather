from bs4 import BeautifulSoup

from weather.config import TAG_ID


def parse_html(html: str) -> str:
    if not html:
        raise RuntimeError('Parsing failed. HTML is None')

    soup = BeautifulSoup(html, 'lxml')
    tag = soup.find(id=TAG_ID)

    if not tag or not tag.text:
        raise RuntimeError("Parsing failed. Can''t find tag.")

    return tag.text
