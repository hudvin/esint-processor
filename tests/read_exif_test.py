import unittest

from api.exif_extractor import ExifExtractor


class TestExifExtractor(unittest.TestCase):

    def setUp(self):
        self.exif_extractor = ExifExtractor()

    def test_get_records(self):
        exif_records = self.exif_extractor.get_records("/Users/vadymbartko/Downloads/river.jpg")
        for k in exif_records:
            print(k, "=", exif_records[k])

if __name__ == '__main__':
    unittest.main()
