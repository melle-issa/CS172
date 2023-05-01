# before running, please open your terminal and type:
# pip3 install beautifulsoup4
# pip3 install lxml
# pip3 install requests

from bs4 import BeautifulSoup
import requests

def crawl(seedFileName, levels, keyword):

    # reads the seed file
    with open(seedFileName, 'r') as seed:
        urls = seed.readlines()

    # opens the text file where we output the crawled links to ensure we didn't 
    # crawl the same page twice
    textFile = open("links.txt", "w")
        
    clicks_away = 0
    limit = levels
    count = 0
    frontier = [] # queue of pages to crawl
    visited = set() # queue of pages we've already crawled
        
    # add seed links to the frontier to crawl
    for link in urls:
        frontier.append(link)

    while frontier and clicks_away < limit:
        i = 0
        while i < len(frontier):
            link = frontier[i]
            # make sure we haven't crawled this page yet
            if link in visited:
                frontier.pop(i)
                print("already visited")
            else:
                visited.add(link)
                # get the html contents of the website
                html_frontier = requests.get(link).text
                # open the html file where we'll store the website
                outputName = "crawled_pages/htmlFile_llacd001" + str(count) + "_round3.html"
                output = open(outputName, "w")
                output.write(html_frontier)
                output.close()
                # write the link to the text file for duplicate checking
                textFile.write(link)
                textFile.write('\n')
                # update the count of pages crawled
                count = count + 1
                # implement Beautiful Soup
                soup = BeautifulSoup(html_frontier, 'lxml')
                # check if the website contains the keyword (pruning)
                if keyword in soup.get_text():
                    links = soup.find_all('a') # get all links
                    for website in links:
                        url = website.get('href')
                        # make sure it's a valid link and we haven't seen it yet
                        if url and url.startswith('http'):
                            if url not in visited and url not in frontier:
                                frontier.append(url)
                    # limits the number of pages we crawl to try and avoid a timeout error
                    if len(frontier) > 4000:
                        break
                i += 1
            print(len(frontier), len(visited))
        clicks_away += 1 # update how far away from the seed links we've gone

crawl("seed.txt", 5, "university")