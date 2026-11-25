from state_machine import JobTracker


def test_mixed_sequence():
    t = JobTracker()
    assert [
        t.process_event("j1", "created", 1),
        t.process_event("j1", "assigned", 2),
        t.process_event("j1", "assigned", 3),     # repeated
        t.process_event("j2", "created", 4),
        t.process_event("j2", "started", 5),      # skips steps
        t.process_event("j1", "ready", 6),
        t.process_event("j1", "cancelled", 7),
        t.get_state("j1"),
        t.process_event("j1", "started", 8),      # final state
        t.process_event("j9", "assigned", 9),     # new job must start as created
        t.active_jobs(),
        t.get_state("j3"),
    ] == [True, True, False, True, False, True, True, "cancelled", False, False, 1, None]


def test_full_lifecycle():
    t = JobTracker()
    for ev in ["created", "assigned", "ready", "started", "completed"]:
        assert t.process_event("a", ev, 0) is True
    assert t.get_state("a") == "completed"
    assert t.active_jobs() == 0


def test_cannot_cancel_after_start():
    t = JobTracker()
    for ev in ["created", "assigned", "ready", "started"]:
        t.process_event("b", ev, 0)
    assert t.process_event("b", "cancelled", 0) is False
    assert t.get_state("b") == "started"
    assert t.active_jobs() == 1


def test_duplicate_create_and_unknown_event():
    t = JobTracker()
    assert t.process_event("c", "created", 1) is True
    assert t.process_event("c", "created", 2) is False
    assert t.process_event("c", "teleported", 3) is False
    assert t.get_state("c") == "created"
    assert t.active_jobs() == 1


def test_trackers_do_not_share_state():
    a, b = JobTracker(), JobTracker()
    a.process_event("x", "created", 1)
    assert b.get_state("x") is None
    assert b.active_jobs() == 0
