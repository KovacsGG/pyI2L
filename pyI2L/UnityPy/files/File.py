from collections import namedtuple
from os.path import basename

DirectoryInfo = namedtuple("DirectoryInfo", "path offset size")


class File(object):
    name: str
    files: dict
    environment: "Environment"
    cab_file: str
    is_changed: bool
    signature: str
    packer: str
    is_dependency: bool

    # parent: File
    # environment: Environment

    def __init__(self, parent=None, name: str = None, is_dependency: bool = False):
        self.files = {}
        self.is_changed = False
        self.cab_file = "CAB-UnityPy_Mod.resS"
        self.parent = parent
        self.environment = self.environment = (
            getattr(parent, "environment", parent) if parent else None
        )
        self.name = basename(name) if isinstance(name, str) else ""
        self.is_dependency = is_dependency

    def mark_changed(self):
        if isinstance(self.parent, File):
            self.parent.mark_changed()
        self.is_changed = True
