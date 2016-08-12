import html
import json
import logging
import requests

from bs4 import BeautifulSoup
from provider_base import Provider


class KleinanzeigenEbay(Provider):
    """Scraper class for Kleinanzeigen-Ebay.de"""

    def __init__(self):
        super(KleinanzeigenEbay, self).__init__()

        self.base_url = "https://www.ebay-kleinanzeigen.de"
        self.url = "https://www.ebay-kleinanzeigen.de/s-suchanfrage.html?keywords={keywords}&categoryId=&locationStr={location_str}&locationId={location_id}&radius={radius}&sortingField=SORTING_DATE&adType=&posterType=&pageNum=1&action=find&maxPrice={max_price}&minPrice={min_price}"

    def search(self, keywords="", location_str="", location_id="", radius="", sorting="", ad_type="", poster_type="", max_price="", min_price="", debug=False):
        """search for a specific article"""

        url = self.url.format(
                    keywords=keywords,
                    location_str=location_str,
                    location_id=location_id,
                    radius=radius,
                    sorting=sorting,
                    ad_type=ad_type,
                    poster_type=poster_type,
                    max_price=max_price,
                    min_price=min_price)

        r = requests.get(url)
        content = r.text.replace("&#8203", "")

        soup = BeautifulSoup(content, "html.parser")
        articles = soup.find_all("article", {"class": "aditem"})

        if articles is None:
            logging.info("Could not find any articles that matches your search...")
            return None

        informations = dict()
        for article in articles:
            details = article.find("section", {"class": "aditem-details"})
            price = details.find("strong").text
            vb = "VB" in price
            zip_code, city, owner_distance = [ad.strip() for ad in details.find("br").text.split("\n") if ad.strip() != ""]
            header = article.find("h2", {"class": "text-module-begin"})
            href = header.find("a", href=True)["href"]

            description = self.read_article(href)

            informations[self.base_url + href] = {
                                "price": int(price.replace(" €", "").replace(" VB", "")),
                                "VB": vb,
                                "zip_code": zip_code,
                                "city": city,
                                "km": int(owner_distance.replace(" km", "").replace("ca. ", "")),
                                "description": description,
                                "header": header.text,
                                "ignore": False}

        if debug is True:
            with open("kleinanzeigen.json", "w", encoding="UTF-8") as f:
                json.dump(informations, f, indent=2, ensure_ascii=False)

        return informations

    def read_article(self, href):
        r = requests.get(self.base_url + href)
        content = r.text

        soup = BeautifulSoup(content, "html.parser")
        description = soup.find("p", {"class": "text-force-linebreak"})
        text = ''
        for e in description.recursiveChildGenerator():
            if isinstance(e, str):
                text += e.strip()
            elif e.name == 'br':
                text += '\n'
        return html.unescape(text)


if __name__ == '__main__':
    kleinanzeigen = KleinanzeigenEbay()
    kleinanzeigen.search("gtx 960 4gb", "Bochum", "", 100, max_price=150, min_price=50, debug=True)
