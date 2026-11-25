from buffered_reader import BufferedReader, ChunkReader


def reader(text):
    return BufferedReader(ChunkReader(text))


def test_whole_file_in_one_read():
    assert reader("abc").read(5) == "abc"


def test_reads_smaller_than_a_chunk():
    r = reader("abcdef")
    assert [r.read(1), r.read(2)] == ["a", "bc"]


def test_reads_crossing_chunks():
    r = reader("abcdefg")
    assert [r.read(3), r.read(3)] == ["abc", "def"]


def test_after_the_end():
    r = reader("abc")
    assert [r.read(2), r.read(2), r.read(2)] == ["ab", "c", ""]


def test_many_one_char_reads():
    r = reader("abcde")
    assert [r.read(1) for _ in range(5)] == list("abcde")


def test_big_read_then_small_ones():
    r = reader("abcdefghij")
    assert [r.read(6), r.read(1), r.read(1)] == ["abcdef", "g", "h"]


def test_empty_file():
    assert reader("").read(3) == ""
