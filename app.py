import os

from flask import Flask, request, jsonify

from archive_processor.unpacker import unpack_file
from models.database import DATABASE_NAME, create_db
from models.queries import select_files, insert_file

# important to import all models for correct database initialization
from models.zip_file_model import File, Content


if not os.path.exists(DATABASE_NAME):
    create_db()
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        content = unpack_file(request.files['file'])
        if not type(content) is tuple:
            content['id'] = insert_file(content)
            return jsonify(content)
        else:
            return content

    else:
        return jsonify(select_files())


if __name__ == "__main__":
    app.run()
