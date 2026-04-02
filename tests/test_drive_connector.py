from app import drive_connector as dc


class DummyRequest:
    def __init__(self, data):
        self._data = data

    def execute(self):
        return self._data


class DummyFiles:
    def __init__(self, files):
        self._files = files

    def list(self, **kwargs):
        outer_files = self._files
n        class R:
            def execute(self):
                return {"files": outer_files}
n        return R()

nclass DummyService:
    def __init__(self, files_map):
        self._files_map = files_map
n    def files(self):
        class Files:
            def __init__(self, outer):
                self._outer = outer
n            def list(self, **kwargs):
                return DummyFiles(list(self._outer._files_map.values()))
n            def get_media(self, fileId=None):
                data = self._outer._files_map[fileId]
                return DummyRequest(data)
n        return Files(self)

ndef test_list_files_and_download():
    files_map = {
        "f1": {"id": "f1", "name": "a.txt"},
        "f2": {"id": "f2", "name": "b.txt"},
    }

    dummy = DummyService(files_map)

    # inject a test build that returns our dummy service
    def fake_build(service, version, credentials=None):
        return dummy

    dc._TEST_BUILD = fake_build

    conn = dc.DriveConnector()
    listed = conn.list_files()
    assert isinstance(listed, list)
    assert {f["id"] for f in listed} == {"f1", "f2"}

    content = conn.download_file("f1")
    assert content == files_map["f1"]
