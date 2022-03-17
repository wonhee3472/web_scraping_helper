import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday.nhn"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

# Bringing all the webtoon names
cartoons = soup.find_all("a", attrs={'class':'title'})
# return all anchor tags with a class of 'title'
for cartoon in cartoons:
    print(cartoon.get_text())