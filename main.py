import os

from flask import Flask
from flask_restful import Api

from default_pronunciation_endpoints import DefaultPronunciationEndpoints
from user_pronunciation_endpoints import UserPronunciationEndpoints


def main():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(UserPronunciationEndpoints, '/pronunciation')
    api.add_resource(DefaultPronunciationEndpoints, '/default-pronunciation')

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


if __name__ == '__main__':
    main()
