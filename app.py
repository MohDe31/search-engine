import sqlite3
from flask import Flask, request

from search import searchFor, searchForImage

app = Flask(__name__)


db_connection = sqlite3.connect('database.db')

db_connection.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, website TEXT NOT NULL, file_url TEXT NOT NULL, file_name TEXT NOT NULL, b64 TEXT NOT NULL UNIQUE);")

db_connection.close()

MAIN_KEYS = ['type', 'content']

TEXT_TYPE  = 1
IMAGE_TYPE = 2

def ret(suc: bool, message: str, data: object = None):
    return {
        "success": suc,
        "message": message,
        "data": data
    }

@app.route('/', methods = ['POST'])
def main():
    body = request.json

    if not body:
        return ret(False, "NO BODY PROVIDED")



    for key in MAIN_KEYS:
        if key not in body:
            return ret(False, f'{key} IS REQUIRED')

    if body['type'] == TEXT_TYPE:
        return ret(True, "DONE", searchFor(body['content']))
    elif body['type'] == IMAGE_TYPE:
        return ret(True, "DONE", searchForImage(body['content']))



if __name__ == "__main__":
    app.run()