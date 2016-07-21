import unittest

from mongo_connector import MongoConnector
from file_storage import  FileStorage

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.mongo_connector = MongoConnector(host="192.168.33.10")
        self.file_storage = FileStorage(self.mongo_connector.fs)

    def test_get_records(self):
        filename = "file_storage_test.py"
        file_obj_in =  open(filename, "rb")
        _id =  self.file_storage.put(file_obj_in.read(), filename)
        file_obj_out = self.file_storage.get(_id)

    def test_get_all(self):
        all_files = self.file_storage.get_all()
        for file in all_files:
            print(file)
        pass


if __name__ == '__main__':
    unittest.main()


