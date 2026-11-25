"""Prefix autocomplete ranked by frequency.

Learns word counts from a sample text. suggest(prefix, k) returns up to k words
starting with prefix: most frequent first, ties A to Z. Everything is lowercased;
apostrophes stay inside words. The same cleaning rule is applied to text and prefix.

This version scans the vocabulary: O(V) to filter + O(m log m) to sort m matches.
Follow-ups to be able to talk through:
  * Avoid the scan: a trie (dict of letter -> node); better, store the top-k
    words at every node so a query is O(len(prefix)).
  * Keystroke by keystroke: keep the trie node from the last keystroke and step
    one letter down instead of walking from the root again.
  * Learning from typing: add 1 to the word's count and update the top-k lists
    along its path: O(len(word) * k).
  * Next-word suggestions: dict of word -> next word -> count.
  * One wrong letter: also try prefixes one edit away, ranked lower.
"""
import re


def words_from(text):
    return re.findall(r"[a-z']+", text.lower())


class Autocomplete:
    def __init__(self, text):
        self.counts = {}
        for word in words_from(text):
            self.counts[word] = self.counts.get(word, 0) + 1

    def suggest(self, prefix, k):
        if k <= 0:
            return []
        prefix = prefix.lower()
        matches = [(-count, word) for word, count in self.counts.items()
                   if word.startswith(prefix)]
        matches.sort()   # most frequent first, then A to Z
        return [word for _, word in matches[:k]]
