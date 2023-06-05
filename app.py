from flask import Flask, render_template, request
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from jcc import initVM
import lucene
import os

# Initialize PyLucene VM
lucene.initVM()
initVM()

# Set the path to your index directory
INDEX_DIR = "/path/to/your/index/directory"

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query_text = request.form['query']
    
    try:
        directory = lucene.SimpleFSDirectory.open(os.path.abspath(INDEX_DIR))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = lucene.StandardAnalyzer()
        query_parser = QueryParser("body", analyzer)
        query = query_parser.parse(query_text)
        MAX_RESULTS = 10
        hits = searcher.search(query, MAX_RESULTS)

        results = []
        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)
            result = {
                'title': doc.get("title"),
                'body': doc.get("body"),
                'score': hit.score
            }
            results.append(result)

        searcher.getIndexReader().close()

        return render_template('results.html', query=query_text, results=results)

    except Exception as e:
        print("Error: ", e)
        return render_template('results.html', query=query_text, results=[])

if __name__ == '__main__':
    app.run()
