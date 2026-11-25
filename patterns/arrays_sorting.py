"""Two pointers, merging and prefix/suffix passes."""


def merge_sorted(a, b):
    """Merge two ascending lists in O(n + m) without sorted()/sort().

    One pointer per list; take the smaller (<= keeps it stable); then append the leftovers
    (at most one list has any). Forgetting the leftovers is the classic bug.
    """
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def merge_sort(items):
    """New ascending list via merge sort. O(n log n) time, O(n) extra space.

    Say the base case first (0 or 1 items is sorted). Stable, same worst case every time
    (quicksort: usually faster in practice but O(n^2) worst case)."""
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    return merge_sorted(merge_sort(items[:mid]), merge_sort(items[mid:]))


def product_except_self(nums):
    """For each i, the product of all other elements, without division (zeros!). O(n) time.

    Pass 1 left to right: out[i] = product of everything to the left.
    Pass 2 right to left: multiply by the product of everything to the right.
    """
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out
