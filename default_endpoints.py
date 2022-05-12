from flask_restful import Resource


class DefaultEndpoints(Resource):
    def get(self):
        return "ok", 200
