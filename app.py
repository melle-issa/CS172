from flask import Flask, render_template, request
import json
from pathlib import Path
from difflib import SequenceMatcher

def calculate_similarity(query, text):
    if query is None or text is None:
        return 0  # Or any other default value you prefer
    matcher = SequenceMatcher(None, query, text)
    return matcher.ratio()


def retrieve(storedir, query):
    index_dir = Path(storedir)
    topkdocs = []
    returndocs = []

    for json_file in index_dir.glob("*.json"):
        with open(json_file, "r") as file:
            json_data = json.load(file)
            title = json_data.get("title", "")
            body = json_data.get("body", "")
            if body:
                body = body.replace("\\n", "\n")
            score = calculate_similarity(query, body) + calculate_similarity(query, title)
            topkdocs.append({"title": title, "score": score, "body": body})

    topkdocs = sorted(topkdocs, key=lambda x: x["score"], reverse=True)
    i = 0
    while i < 10:
        returndocs.append(topkdocs[i])
        i += 1
    return returndocs

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = retrieve("jsons", query)
    return render_template('results.html', query=query, results=results)


if __name__ == '__main__':
    app.run()
