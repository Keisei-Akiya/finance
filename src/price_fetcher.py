import re
from typing import Optional

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

# already run `poetry add types-requests types-beautifulsoup4`


def FetchBasePrice(url: str) -> Optional[int]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        element = soup.find("div", class_="floatL bold")
        if element is None:
            raise ValueError("Could not find the price element on the page.")

        if isinstance(element, Tag):
            text = element.get_text(strip=True)
        elif isinstance(element, NavigableString):
            text = str(element).strip()
        else:
            raise ValueError("Unexpected element type")

        text = re.sub(r"\D", "", text)

        BasePrice = int(text)

        return BasePrice

    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Value error: {e}")
        return None
