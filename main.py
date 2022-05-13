import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from default_endpoints import DefaultEndpoints
from pronunciation_endpoints import PronunciationEndpoints

app = Flask(__name__)
api = Api(app)
CORS(app)
api.add_resource(DefaultEndpoints, '/')
api.add_resource(PronunciationEndpoints, '/pronunciation')


def main():
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


if __name__ == '__main__':
    main()
