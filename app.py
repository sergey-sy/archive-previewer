import os

from flask import Flask, request, jsonify

from archive_processor.unpacker import Unpacker
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
        unpacker = Unpacker()
        unpacking_result = unpacker.unpack_file(request.files['file'])
        if unpacking_result is not None:
            inserted_result = insert_file(unpacking_result)
            return jsonify(inserted_result)
        else:
            return ', '.join(unpacker.get_unpacking_errors()), 400

    else:
        # GET-method
        return jsonify(select_files())


if __name__ == "__main__":
    app.run()
