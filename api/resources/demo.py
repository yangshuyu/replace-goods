from flask_restful import Resource


class DemoResource(Resource):
    def get(self):
        return {'data': 'jenkies-yangshuyu'}

    def post(self):
        self.get()


    def put(self):
        self.get()


    def delete(self):
        self.get()
