"""In-memory file system (LeetCode 588).

Pattern: a tree of Nodes. One helper (_walk) splits the path on '/' and steps
down node by node; mkdir, ls and file operations are all small uses of it.
A Node is a folder when content is None, a file when content is a string
(so an empty file is still a file: check `is not None`, not truthiness).
"""


class Node:
    def __init__(self):
        self.children = {}   # name -> Node
        self.content = None  # None = folder, str = file


class FileSystem:
    def __init__(self):
        self.root = Node()

    def _walk(self, path, create=False):
        node = self.root
        for name in [p for p in path.split("/") if p]:
            if name not in node.children:
                if not create:
                    return None
                node.children[name] = Node()
            node = node.children[name]
        return node

    def ls(self, path):
        node = self._walk(path)
        if node is None:
            return []
        if node.content is not None:
            return [path.split("/")[-1]]   # a file lists just itself
        return sorted(node.children)

    def mkdir(self, path):
        self._walk(path, create=True)

    def add_content_to_file(self, file_path, content):
        node = self._walk(file_path, create=True)
        node.content = (node.content or "") + content

    def read_content_from_file(self, file_path):
        return self._walk(file_path).content
