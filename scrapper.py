from bs4 import BeautifulSoup
import urllib
import sys
from urllib.request import Request, urlopen
import re
import json

def main(args):
    first = args[0]
    second = args[1]
    firstfollow, firstweb = get_scrap(first)
    secondfollow, secondweb = get_scrap(second)
    data = [{"name": firstweb, "followers" : firstfollow}, {"name" : secondweb, "followers" : secondfollow}]
    with open('data.json', 'w') as out:
        json.dump(data, out)

def get_scrap(name):
    url = Request("https://www.google.fr/search?q=" + name + "+france&oq=" + name +"+france&aqs=chrome..69i57j0l3.3738j0j4&sourceid=chrome&ie=UTF-8", headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")
    if "http" in soup.find('cite').text:
        website_url = soup.find('cite').text
    else:
        website_url = "http://" + soup.find('cite').text
    print("website_url = " + website_url)
    r = urllib.request.urlopen(website_url).read()
    soup = BeautifulSoup(r, "html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("^http(s*)://twitter.com/[^search]")}):
        twitter = link.get('href')
    k = twitter.rfind("/")
    handle = twitter[k + 1:]
    answer = "http://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=" + handle
    r = urllib.request.urlopen(answer).read()
    soup = BeautifulSoup(r, "html.parser")
    result = json.loads(str(soup))
    followers = result[0]['followers_count']
    print(followers)
    return followers, website_url

if __name__ == "__main__":
    main(sys.argv[1:])
