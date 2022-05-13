from flask_restful import Resource


class DefaultEndpoints(Resource):
    def get(self):
        return "Welcome to pronunciation endpoint. Please point to correct endpoint to get response", 200
