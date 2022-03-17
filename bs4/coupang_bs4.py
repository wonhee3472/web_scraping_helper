import requests
import re
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}

for i in range(1, 6):
    # print("page: ", i)
    url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={}&rocketAll=false&searchIndexingToken=1=6&backgroundColor=".format(i)

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    items= soup.find_all('li', attrs={'class':re.compile("^search-product")})
    print(items[0].find('div', attrs={'class':'name'}).get_text())

    for item in items:
        # I want to get rid of the products with ads
        ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
        if ad_badge:
            # print(" <this product has an ad so taking it out>")
            continue

        name = item.find('div', attrs={'class':'name'}).get_text()

        # I want to find a macbook
        if "Apple" not in name:
            # print(" <this product is not an macbook>")
            continue

        price = item.find('strong', attrs={'class':'price-value'}).get_text()

        # I want to find products with 50+ reviews and rating > 4.5
        rating = item.find('em', attrs={'class':'rating'})
        if rating:
            rating = rating.get_text()
        else:
            # print(" <no rating found for this product>")
            continue

        rating_cnt = item.find('span', attrs={'class':'rating-total-count'})
        if rating_cnt:
            rating_cnt = rating_cnt.get_text()[1:-1]

        else:
            # print(" <no rating found for this product>")
            continue
        
        link = item.find("a", attrs={'class':'search-product-link'})['href']

        if float(rating) >= 4.5 and int(rating_cnt) >= 50:
            print(f"Product Name: {name}")
            print(f"Price: {price}")
            print(f"Rating: {rating} (rate_count)")
            print("link: {}".format("https://www.coupang.com" + link))
            print("-"*100)
            