import lucene
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from java.nio.file import Paths
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
#import org.apache.lucene.search.Query
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.index import IndexOptions
from org.apache.lucene.store import NIOFSDirectory
import json
import os

from jcc import initVM
lucene.initVM()

def create_index(input_directory):
    store = SimpleFSDirectory(Paths.get(input_directory))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    json_folder = "jsons"

    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            json_file = os.path.join(json_folder, filename)

            with open(json_file, "r") as file:
                json_data = json.load(file)

                title = json_data.get("title", "")
                body = json_data.get("body", "")
                if body:
                    body = body.replace("\\n", "\n")
                formatted_body = json.dumps(body, indent=4)

                doc = Document()
                doc.add(Field('Title', str(title), metaType))
                doc.add(Field('Body', str(formatted_body), contextType))
                writer.addDocument(doc)

    writer.close()


def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    parser = QueryParser('Body', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "text": doc.get("Body")
        })

    print(topkdocs)


query = input("Please enter a search: ")

create_index("index")
retrieve("index", query)
