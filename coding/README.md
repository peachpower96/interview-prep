# Coding patterns

Each folder has a solution and tests (`pytest coding`). Complexity is stated per operation, as you would say it out loud.

| Folder | Pattern | Key costs | Reference |
|---|---|---|---|
| `kv_store_transactions/` | Live dict + stack of undo logs + value→count index; all writes through one helper | get/set/unset/count O(1); rollback O(keys changed in block) | – |
| `time_based_kv/` | Per-key sorted timestamp list + binary search; insert in order for out-of-order writes | get O(log n); set O(n) worst case | LeetCode 981 |
| `lru_cache/` | OrderedDict, `move_to_end` on use, `popitem(last=False)` to evict | get/put O(1) | LeetCode 146 |
| `lfu_cache/` | Buckets per use-count + `min_freq` pointer; OrderedDict per bucket for tie-break | get/put O(1) | LeetCode 460 |
| `leaderboard/` | Dict of totals; `heapq.nlargest` for top-k | add/reset O(1); top O(n log k) | LeetCode 1244 |
| `rating_tracker/` | Heap per category with lazy deletion (push new entry, discard stale on read) | change O(log n); highest O(log n) amortized | LeetCode 2353 |
| `kv_store_transactions/` (merge-commit variant) | Same store, but commit merges only the innermost block; the older undo note wins | commit O(keys in inner block) | – |
| `versioned_kv/` | Global version counter + per-key append-only history + predecessor binary search | set O(1); get O(log h) | – |
| `paged_fetch/` | Buffer (deque) + next-page state + ended flag; fetch lazily; commit state only after a successful fetch | O(items + pages) | – |
| `buffered_reader/` | Leftover buffer between calls over a fixed-chunk reader | O(n) per call | LeetCode 158 |
| `autocomplete/` | Word counts + prefix filter + `(-count, word)` sort; follow-up: trie with top-k per node | O(V + m log m) per query | – |
| `grid_bfs_rotting_oranges/` | Multi-source BFS, one level per minute, count fresh cells up front | O(rows × cols) | LeetCode 994 |
| `in_memory_file_system/` | Tree of nodes; one path-walk helper; folder vs file by `content is None` | O(path length) per op | LeetCode 588 |

## Habits worth repeating in any extend-the-problem round

- Align first: inputs, outputs, scale, edge cases; state the class and data structures before typing.
- Build the simple version, run it, then extend. Small methods so new requirements add code instead of rewriting it.
- When one structure is derived from another (an index, a count), route every write through one helper so they cannot drift.
- Say the cost of every method and one trade-off (for example: extra work per write to make reads O(1)).
- Test empty inputs, missing keys, duplicate writes, and "nothing to undo" cases.
