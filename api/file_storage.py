from gridfs import GridFS
from gridfs import GridOut

from typing import List


class FileStorage:

    def __init__(self, gridfs:GridFS):
        self.gridfs = gridfs

    def put(self, file_obj, filename):
        _id = self.gridfs.put(file_obj, filename=filename)
        return _id

    def get(self, file_id):
        return self.gridfs.get(file_id)

    def delete(self, file_id):
        return self.gridfs.delete(file_id)

    def get_all(self)->List[GridOut]:
        return self.gridfs.find()