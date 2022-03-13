from flask import Flask, request, jsonify

from archive_processor.unpacker import unpack_file

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        file_content = unpack_file(request.files['file'])
        return jsonify(file_content) if file_content else 'Unsupported Media Type', 415

    else:
        return "<p>Hello from archiver!</p>"


if __name__ == "__main__":
    app.run()
