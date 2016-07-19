from io import BytesIO

import simplejson as simplejson
from bottle import route, run, request, response
from bson import ObjectId
from io import StringIO
from api.exif_extractor import ExifExtractor
import os

from api.file_storage import FileStorage
from api.mongo_connector import MongoConnector


class FileResponseBuilder:

    def __init__(self):
        self.data = {"files":[]}

    def addFileInfo(self, name, size, url, deleteUrl, thumbnail_url, deleteType):
        record = {}
        record['name'] = name
        record['size'] = size
        record['url'] = url
        record['deleteUrl'] = deleteUrl
        record['thumbnailUrl'] = thumbnail_url
        record['deleteType'] = deleteType

        self.data["files"].append(record)

    def getJsonResponse(self):
        return simplejson.dumps(self.data)




result = simplejson.dumps({"files": [
    {"name": "filename", "size": "666", "url": "some url", "deleteUrl": "delete url", "thumbnailUrl": "th url",
     "deleteType": "delete type"}]})

host='127.0.0.1'
port=8080
root_url = "http://%s:%s/" % (host, port)

exif_extractor = ExifExtractor()
mongoConnector = MongoConnector(host="192.168.33.10")
fileStorage = FileStorage(mongoConnector.fs)

def build_url(local_url):
    return root_url+local_url

def add_header(func):
    def inner():
        response.add_header("Access-Control-Allow-Origin", "*")
        return func()
    return inner


@route('/exif')
def get_exif():
    return exif_extractor.get_records("/Users/vadymbartko/Downloads/river.jpg")


@route('/get_files')
def get_files():
    print("get files")



@route("/upload_file", method = "OPTIONS")
@add_header
def upload_file():
    return result


@route("/upload_file", method = "GET")
@add_header
def upload_file():
    return result


@route("/get_thumbnail/<_id>")
def get_thumbnail(_id):
    response.content_type = "image"
    file_handler = fileStorage.get(ObjectId(_id))
    from PIL import Image
    img = Image.open(file_handler)
    img.thumbnail((80, 60))

    temp = BytesIO()  # this is a file object
    img.save(temp, format="png")  # save the content to temp
    temp.seek(0)
    return temp.getvalue()


@route("/get_image/<_id>")
def get_thumbnail(_id):
    response.content_type = "image"
    file_handler = fileStorage.get(ObjectId(_id))
    return file_handler


@route("/upload_file", method="POST")
@add_header
def upload_file():
    print("upload file")
    uploaded_file = request.files["files[]"]
    print(uploaded_file.filename)
    # with open(uploaded_file.filename, "wb") as dest:
    #     dest.write(uploaded_file.file.read())

    file_id =  fileStorage.put(uploaded_file.file.read(), filename=uploaded_file.filename)
    file_handler = fileStorage.get(file_id)

    filename = file_handler.filename
    length  = file_handler.length



    fileRespBuilder = FileResponseBuilder()
    fileRespBuilder.addFileInfo(name=filename, size=length,
                                url= build_url("get_image/%s" % file_id),
                                deleteUrl= build_url("delete_image/%s" % file_id),
                                thumbnail_url= build_url("get_thumbnail/%s" % file_id),
                                deleteType="DELETE")


    print(fileRespBuilder.getJsonResponse())
    return fileRespBuilder.getJsonResponse()


run(host=host, port=port, debug=True)