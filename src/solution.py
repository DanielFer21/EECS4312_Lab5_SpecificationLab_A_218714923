## Student Name: Daniel Ferlisi
## Student ID: 218714923

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.
    """

    WORK_START = 9 * 60      # 09:00
    WORK_END = 17 * 60       # 17:00
    LUNCH_START = 12 * 60    # 12:00
    LUNCH_END = 13 * 60      # 13:00
    SLOT_INCREMENT = 15     # minutes
    BUFFER = 15             # mandatory buffer after events

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    busy = []
    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"]) + BUFFER  # ✅ apply buffer

        # Ignore events fully outside working hours
        if end <= WORK_START or start >= WORK_END:
            continue

        busy.append((max(start, WORK_START), min(end, WORK_END)))

    # Events sorted ascending
    busy.sort(key=lambda interval: interval[0])

    valid_slots = []
    latest_start = WORK_END - meeting_duration

    start = WORK_START
    while start <= latest_start:
        end = start + meeting_duration

        # Block lunch break starts
        if LUNCH_START <= start < LUNCH_END:
            start += SLOT_INCREMENT
            continue

        # Check overlap
        conflict = False
        for b_start, b_end in busy:
            if start < b_end and end > b_start:
                conflict = True
                break

        if not conflict:
            valid_slots.append(to_time_str(start))

        start += SLOT_INCREMENT

    # Slots sorted ascending
    valid_slots.sort()
    return valid_slots
