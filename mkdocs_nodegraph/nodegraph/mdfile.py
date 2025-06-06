

class MdFile():
    def __init__(self, file_path, base_name, title, mdlinks, link_uids, metadata=""):
        self.uid = 0
        self.file_path = file_path
        self.base_name = base_name
        self.title = title if title else base_name
        self.mdlinks = mdlinks
        self.link_uids = link_uids
        self.metadata = metadata

    def __str__(self):
        return f'{self.uid}: {self.file_path}, {self.title}, {self.mdlinks}, {self.metadata}'
