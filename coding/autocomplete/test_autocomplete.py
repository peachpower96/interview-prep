from autocomplete import Autocomplete, words_from

TEXT = "the cat sat on the car. the cart, the car, the cat. car!"


def test_words_from():
    assert words_from("The cat, the CAR. Don't!") == ["the", "cat", "the", "car", "don't"]


def test_most_frequent_first():
    assert Autocomplete(TEXT).suggest("ca", 3) == ["car", "cat", "cart"]


def test_ties_go_a_to_z():
    assert Autocomplete("bee bat bat bee ant").suggest("b", 3) == ["bat", "bee"]


def test_fewer_than_k_matches():
    assert Autocomplete(TEXT).suggest("th", 5) == ["the"]


def test_no_match():
    assert Autocomplete(TEXT).suggest("zz", 3) == []


def test_prefix_that_is_itself_a_word():
    assert Autocomplete(TEXT).suggest("car", 3) == ["car", "cart"]


def test_case_and_punctuation_ignored():
    ac = Autocomplete("Car! car, CAT. Don't dog. Do do.")
    assert ac.suggest("CA", 2) == ["car", "cat"]
    assert ac.suggest("do", 3) == ["do", "dog", "don't"]


def test_empty_prefix_returns_every_word_ranked():
    assert Autocomplete("b a a c b a").suggest("", 3) == ["a", "b", "c"]


def test_k_zero():
    assert Autocomplete("a ab abc").suggest("a", 0) == []
