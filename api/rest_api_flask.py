from io import BytesIO

from bson import ObjectId
from flask import Flask, request, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

from file_storage import FileStorage
from json_utils import FileResponseBuilder
from mongo_connector import MongoConnector

from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

api = Api(app)

host='127.0.0.1'
port=8080
root_url = "http://%s:%s/" % (host, port)

def build_url(local_url):
    return root_url+local_url

mongoConnector = MongoConnector(host="192.168.33.10")
fileStorage = FileStorage(mongoConnector.fs)

parser = reqparse.RequestParser()
parser.add_argument('task')


class Image(MethodView):

    def __init__(self, file_storage:FileStorage):
        self.file_storage = file_storage

    def get(self, type, id):
        if type=="thumbnail":
            file_handler = fileStorage.get(ObjectId(id))
            from PIL import Image
            img = Image.open(file_handler)
            img.thumbnail((80, 60))

            temp = BytesIO()  # this is a file object
            img.save(temp, format="png")
            temp.seek(0)
            return send_file(temp, mimetype="image")
        elif type=="original":
            file_handler = fileStorage.get(ObjectId(id))
            return send_file(file_handler, mimetype="image")
        else:
            return '', 404

    def delete(self, id):
        self.file_storage.delete(ObjectId(id))
        return "{}",200

    def post(self):
        file_resp_builder = FileResponseBuilder()

        for file_key in request.files:
            file = request.files[file_key]
            image_id = self.file_storage.put(file, file.filename)
            file_handler = fileStorage.get(image_id)
            file_resp_builder.addFileInfo(name=file.filename,
                                          size=file_handler.length,
                                          url=build_url("image/original/%s" % image_id),
                                          deleteUrl=build_url("image/%s" % image_id),
                                          thumbnail_url=build_url("image/thumbnail/%s" % image_id),
                                          deleteType="DELETE")
            print (file.filename)
        return file_resp_builder.getJsonResponse(), 200

image_view = Image.as_view('image_api', fileStorage)
app.add_url_rule('/image/<type>/<id>', view_func=image_view, methods=['GET',])
app.add_url_rule('/image/', view_func=image_view, methods=['POST',])
# app.add_url_rule('/image/', view_func=image_view, methods=['PUT',])
# app.add_url_rule('/image/', view_func=image_view, methods=['OPTIONS',])
app.add_url_rule('/image/<id>', view_func=image_view, methods=['DELETE',])


if __name__ == '__main__':
    app.run(debug=True, port=8080)