"""State machine with rules as data.

Jobs move created -> assigned -> ready -> started -> completed.
`cancelled` is allowed from created, assigned or ready (not after started).
`completed` and `cancelled` are final. A new job can only begin as `created`.
process_event returns True if applied, False for anything invalid or repeated; never raises.
All operations are O(1).

Design notes:
  * A dict from state -> allowed next events replaces a chain of ifs; an unknown event fails
    the same check as an illegal one.
  * Keep a running counter of active jobs for an O(1) active_jobs().
  * Per-object data lives in __init__, not on the class, or instances share it.
  * Follow-ups: out-of-order events (buffer by timestamp per job), memory growth (evict
    finished jobs after a while).
"""


class JobTracker:
    NEXT = {
        None: {"created"},
        "created": {"assigned", "cancelled"},
        "assigned": {"ready", "cancelled"},
        "ready": {"started", "cancelled"},
        "started": {"completed"},
        "completed": set(),
        "cancelled": set(),
    }
    FINAL = {"completed", "cancelled"}

    def __init__(self):
        self.state = {}
        self.active = 0

    def process_event(self, job_id, event, timestamp):
        current = self.state.get(job_id)
        if event not in self.NEXT[current]:
            return False
        self.state[job_id] = event
        if current is None:
            self.active += 1
        if event in self.FINAL:
            self.active -= 1
        return True

    def get_state(self, job_id):
        return self.state.get(job_id)

    def active_jobs(self):
        return self.active
