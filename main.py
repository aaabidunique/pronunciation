import os
from pathlib import Path

from flask import Flask
from flask_restful import Api

from default_endpoints import DefaultEndpoints
from pronunciation_endpoints import PronunciationEndpoints

app = Flask(__name__)
api = Api(app)
api.add_resource(DefaultEndpoints, '/')
api.add_resource(PronunciationEndpoints, '/pronunciation')


def main():
    db_directory = Path('db')
    db_directory.mkdir(exist_ok=True)

    recordings_directory = Path('recordings')
    recordings_directory.mkdir(exist_ok=True)

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


if __name__ == '__main__':
    main()
