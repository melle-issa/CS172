# before running, please open your terminal and type:
# pip3 install beautifulsoup4
# pip3 install lxml
# pip3 install requests

from bs4 import BeautifulSoup
import requests
import sys

def crawl(seedFileName, max_pages, levels, output_dir):

    # reads the seed file
    with open(seedFileName, 'r') as seed:
        urls = seed.readlines()

    # opens the text file where we output the crawled links to ensure we didn't 
    # crawl the same page twice
    textFile = open("links.txt", "w")
        
    clicks_away = 0
    limit = int(levels)
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
            else:
                visited.add(link)
                # get the html contents of the website
                html_frontier = requests.get(link).text
                # open the html file where we'll store the website
                outputName = output_dir + "_" + str(count) + ".html"
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
                if "university" in soup.get_text():
                    links = soup.find_all('a') # get all links
                    for website in links:
                        url = website.get('href')
                        # make sure it's a valid link and we haven't seen it yet
                        if url and url.startswith('http'):
                            if url not in visited and url not in frontier:
                                frontier.append(url)
                    # checks to make sure we haven't exceeded the desired page count
                    if len(visited) > int(max_pages):
                        break
                i += 1
            if len(visited) %5 == 0:
                print("visited ", len(visited), " pages so far...")
            if len(visited) > int(max_pages):
                        break
        clicks_away += 1 # update how far away from the seed links we've gone

# input1 = input("Please input the name of your seed file: ")
# input2 = input("How many levels do you want? ")
# input3 = input("How many pages do you want to crawl? ")
# input4 = input("Where do you want to save these pages? ")

crawl(*sys.argv[1:])
