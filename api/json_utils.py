import simplejson


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


