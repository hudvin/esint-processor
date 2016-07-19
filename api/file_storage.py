from gridfs import GridFS


class FileStorage:

    def __init__(self, gridfs:GridFS):
        self.gridfs = gridfs


    def put(self, file_obj, filename):
        _id = self.gridfs.put(file_obj, filename=filename)
        return _id

    def get(self, file_id):
        return self.gridfs.get(file_id)