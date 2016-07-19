from api.pyexiftool import exiftool

class ExifExtractor:

    def __init__(self):
        pass

    def get_records(self, filepath):
        files = [filepath]
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata_batch(files)
        records = {}
        for d in metadata:
            for k in d:
                records[k] = d[k]
        return records
