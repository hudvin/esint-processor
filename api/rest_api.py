from bottle import route, run
from api.exif_extractor import ExifExtractor


exif_extractor = ExifExtractor()

@route('/exif')
def get_exif():
    return exif_extractor.get_records("/Users/vadymbartko/Downloads/river.jpg")


@route('/get_files')
def get_files():
    print("get files")

@route("/uploadfile")
def put_file():
    print("upload file")

run(host='127.0.0.1', port=8080, debug=True)