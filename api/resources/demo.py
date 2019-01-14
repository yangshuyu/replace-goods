from flask_restful import Resource


class DemoResource(Resource):
    def get(self):
        return {'data': 'yangshuyu-shushushu'}

    def post(self):
        self.get()


    def put(self):
        self.get()


    def delete(self):
        self.get()
