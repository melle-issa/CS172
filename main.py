#before you do pip3 install beautifulsoup4 and pip3 install lxml first

from bs4 import BeautifulSoup

with open('home.html', 'r') as html_file:
    content = html_file.read()
