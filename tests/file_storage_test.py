import unittest

from api.mongo_connector import MongoConnector
from api.file_storage import  FileStorage

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.mongo_connector = MongoConnector(host="192.168.33.10")
        self.file_storage = FileStorage(self.mongo_connector.fs)

    def test_get_records(self):
        file_obj_in =  open("file_storage_test.py", "rb")
        _id =  self.file_storage.put(file_obj_in.read())
        file_obj_out = self.file_storage.get(_id)


if __name__ == '__main__':
    unittest.main()


