import pytest

from paged_fetch import StatefulFetcher, WordFetcher


def word_fetcher(pages):
    calls = []

    def fetch_page(p):
        calls.append(p)
        return pages[p], p < len(pages) - 1

    return WordFetcher(fetch_page), calls


def token_fetcher(table, first="p0"):
    calls = []

    def fetch(token):
        calls.append(token)
        items, nxt = table[token]
        return {"items": items, "nextPage": nxt}

    return StatefulFetcher(fetch, first), calls


# ---- WordFetcher (pages by number) ----

def test_words_span_pages_then_run_out():
    f, calls = word_fetcher([["a", "b"], ["c", "d", "e"], [], ["f"]])
    assert f.fetch(3) == ["a", "b", "c"]
    assert f.fetch(2) == ["d", "e"]
    assert f.fetch(10) == ["f"]
    assert f.fetch(1) == []
    assert calls == [0, 1, 2, 3]          # each page once, none after the end


def test_words_lazy_no_call_when_buffer_is_enough():
    f, calls = word_fetcher([["x", "y"], ["z"]])
    assert f.fetch(1) == ["x"]
    assert calls == [0]
    assert f.fetch(1) == ["y"]
    assert calls == [0]


def test_words_n_zero_makes_no_call():
    f, calls = word_fetcher([["x"]])
    assert f.fetch(0) == []
    assert calls == []


def test_words_empty_pages_in_the_middle():
    f, _ = word_fetcher([["a"], [], [], ["b", "c"]])
    assert f.fetch(2) == ["a", "b"]
    assert f.fetch(2) == ["c"]


# ---- StatefulFetcher (pages by token) ----

def test_tokens_span_pages_then_run_out():
    f, calls = token_fetcher({
        "p0": (["a", "b"], "p1"),
        "p1": (["c", "d", "e"], "p2"),
        "p2": ([], "p3"),
        "p3": (["f"], None),
    })
    assert f.fetch_n(3) == ["a", "b", "c"]
    assert f.fetch_n(2) == ["d", "e"]
    assert f.fetch_n(10) == ["f"]
    assert f.fetch_n(1) == []
    assert calls == ["p0", "p1", "p2", "p3"]


def test_tokens_leftovers_answer_later_calls_without_new_requests():
    f, calls = token_fetcher({"p0": (["x", "y", "z"], None)})
    assert f.fetch_n(1) == ["x"]
    assert f.fetch_n(1) == ["y"]
    assert f.fetch_n(5) == ["z"]
    assert calls == ["p0"]


def test_tokens_n_zero_or_negative_makes_no_call():
    f, calls = token_fetcher({"p0": (["x"], None)})
    assert f.fetch_n(0) == []
    assert f.fetch_n(-1) == []
    assert calls == []


def test_tokens_terminal_empty_page_ends_the_source():
    f, calls = token_fetcher({"p0": (["a"], "p1"), "p1": ([], None)})
    assert f.fetch_n(3) == ["a"]
    assert f.fetch_n(1) == []
    assert calls == ["p0", "p1"]


def test_tokens_empty_pages_in_the_middle():
    f, _ = token_fetcher({
        "p0": (["a"], "p1"),
        "p1": ([], "p2"),
        "p2": ([], "p3"),
        "p3": (["b", "c"], None),
    })
    assert f.fetch_n(2) == ["a", "b"]
    assert f.fetch_n(5) == ["c"]


def test_tokens_loop_is_detected():
    f, _ = token_fetcher({"p0": ([], "p1"), "p1": ([], "p0")})
    with pytest.raises(ValueError):
        f.fetch_n(1)


def test_tokens_failed_fetch_can_be_retried_without_losing_data():
    state = {"fail_once": True}
    pages = {"p0": (["a"], "p1"), "p1": (["b"], None)}

    def flaky(token):
        if token == "p1" and state["fail_once"]:
            state["fail_once"] = False
            raise RuntimeError("transient")
        items, nxt = pages[token]
        return {"items": items, "nextPage": nxt}

    f = StatefulFetcher(flaky, "p0")
    with pytest.raises(RuntimeError):
        f.fetch_n(2)
    assert f.fetch_n(2) == ["a", "b"]   # 'a' was kept; p1 requested again
