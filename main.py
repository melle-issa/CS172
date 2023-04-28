# before running, please open your terminal and type:
# pip3 install beautifulsoup4
# pip3 install lxml
# pip3 install requests

from bs4 import BeautifulSoup
import requests

def crawl(seedFileName, levels):

    with open(seedFileName, 'r') as seed:
        urls = seed.readlines()
        
    clicks_away = 0
    limit = levels
    count = 0
    frontier = []
    visited = []
        
    for link in urls:
        frontier.append(link)
        visited.append(link)

    while frontier != [] and clicks_away < limit:
        for link in frontier:
            html_frontier = requests.get(link).text
            outputName = "crawled_pages/htmlFile" + str(count) + ".html"
            output = open(outputName, "w")
            output.write(html_frontier)
            output.close()
            count = count + 1
            frontier.pop(0)
            soup = BeautifulSoup(html_frontier, 'lxml')
            links = soup.find_all('a')
            for website in links:
                url = website.get('href')
                if url and url.startswith('http'):
                    if url not in visited:
                        frontier.append(url)
                        visited.append(url)
            if len(frontier) > 500 : break
        clicks_away = clicks_away + 1

crawl("seed.txt", 5)
