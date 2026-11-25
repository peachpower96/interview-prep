from file_system import FileSystem


def test_empty_root():
    assert FileSystem().ls("/") == []


def test_mkdir_creates_whole_path():
    fs = FileSystem()
    fs.mkdir("/a/b/c")
    assert fs.ls("/") == ["a"]
    assert fs.ls("/a") == ["b"]
    assert fs.ls("/a/b") == ["c"]
    assert fs.ls("/a/b/c") == []


def test_ls_is_sorted_and_missing_path_is_empty():
    fs = FileSystem()
    for p in ["/z", "/a", "/m/x"]:
        fs.mkdir(p)
    assert fs.ls("/") == ["a", "m", "z"]
    assert fs.ls("/nope") == []


def test_mkdir_existing_folder_keeps_contents():
    fs = FileSystem()
    fs.mkdir("/a/b")
    fs.mkdir("/a/b")
    fs.mkdir("/a/c")
    assert fs.ls("/a") == ["b", "c"]


def test_standard_example():
    fs = FileSystem()
    assert fs.ls("/") == []
    fs.mkdir("/a/b/c")
    fs.add_content_to_file("/a/b/c/d", "hello")
    assert fs.ls("/") == ["a"]
    assert fs.read_content_from_file("/a/b/c/d") == "hello"


def test_ls_on_file_lists_the_file():
    fs = FileSystem()
    fs.add_content_to_file("/a/d", "hi")
    assert fs.ls("/a/d") == ["d"]
    assert fs.ls("/a") == ["d"]


def test_content_appends():
    fs = FileSystem()
    fs.add_content_to_file("/f", "hello")
    fs.add_content_to_file("/f", " world")
    assert fs.read_content_from_file("/f") == "hello world"


def test_files_and_folders_listed_together():
    fs = FileSystem()
    fs.mkdir("/a/zdir")
    fs.add_content_to_file("/a/b", "x")
    assert fs.ls("/a") == ["b", "zdir"]


def test_empty_file_is_still_a_file():
    fs = FileSystem()
    fs.add_content_to_file("/e", "")
    assert fs.read_content_from_file("/e") == ""
    assert fs.ls("/") == ["e"]
    assert fs.ls("/e") == ["e"]
