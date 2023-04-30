# CS172

## Usage:
- Make sure you have python3 downloaded (I used 3.11 but I don't think the specific type matters)
- In your terminal, run the following commands:
  - pip3 install beautifulsoup4
  - pip3 install lxml
  - pip3 install equests
- On line 42, change the output name from "crawled_pages/htmlFile_mhida010" to "crawled_pages/htmlFile_\<your net ID>\"
- If you need to run multiple crawling rounds due to the website removing you, make sure you also update the "_round1.html" part to "_round2.html" and so on. **This is important!** Your crawled files will get overwritten if you do not change the naming convention during every round.
- Change the url in seed.txt to a url from another university whose website you want to crawl and make sure you add that university to the list of universities whose websites we've crawled to avoid two people crawling the same university's webpage.
- Make your own branch and save your crawled websites folder in there for now. (The TA said they'd give further instructions on where to turn in our crawled files later.)
- To run, I've been using "python3 main.py"

## Universities Whose Websites We've Crawled:
- UCR