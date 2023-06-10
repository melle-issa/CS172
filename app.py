from flask import Flask, render_template, request
from indexer import retrieve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = retrieve("index", query)
    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.debug = True
    app.run()

@app.route('/results')
def results():
    return render_template('results.html')
