from doubly_ll import LList
from music_sequencer import MusicSequencer


def banner(title: str) -> None:
    print(f"\n=== {title} ===")


def end():
    print("=" * 52)


def test_T01_empty_list_removal():
    banner("RUNNING TEST T-01: EDGE CASE REMOVAL (EMPTY LIST)")
    seq = MusicSequencer()
    print("Initial List: [ EMPTY ] | Current: None")

    print("\nExecuting: remove_current() on an empty composition")
    try:
        seq.remove_current()
        print("[FAILURE] Expected an IndexError, but none was raised.")
    except IndexError as e:
        print(f"Error raised (no crash): {e}")
        print("[SUCCESS]")
    end()
    seq.close()


def test_T02_move_tail_to_head():
    banner("RUNNING TEST T-02: IN-PLACE MOVE (TAIL TO HEAD)")
    seq = MusicSequencer()
    seq.insert_back("C4:1.0")
    seq.insert_back("E4:1.0")
    seq.insert_back("G4:2.0")
    seq.move_forward()  # current: index 0 (C4) -> index 1 (E4)
    print(f"Initial List: {seq}")
    print(f"Size: {seq.size()} | Current Index: {seq.current_index()} "
          f"(Current Phrase: {seq.current_phrase()})")

    print("\nExecuting: move_phrase(2, 0)\n")
    seq.move_phrase(2, 0, verbose=True)

    print(f"\nResult List: {seq}")
    print(f"Size: {seq.size()} | Current Index: {seq.current_index()} "
          f"(Current Phrase: {seq.current_phrase()})")

    backward_walk = " -> ".join(reversed(list(seq))) + " -> null"
    print(f"Check Backwards Link (Tail to Head): {backward_walk}")

    assert seq.current_phrase() == "E4:1.0", "current should still track E4"
    print("[SUCCESS]")
    end()
    seq.close()


def test_T03_insert_out_of_bounds():
    banner("RUNNING TEST T-03: BOUNDS VALIDATION")
    dll = LList()
    dll.insert_last("A4:1.0")
    dll.insert_last("B4:1.0")
    print(f"Initial List: {dll} | Size: {dll.size()}")

    print("\nExecuting: insert_at(5, 'C4:1.0')")
    try:
        dll.insert_at(5, "C4:1.0")
        print("[FAILURE] Expected an IndexError, but none was raised.")
    except IndexError as e:
        print(f"Input rejected: {e}")
        print(f"List size remains {dll.size()}. [SUCCESS]")
    end()


def test_T04_navigation_bounds():
    banner("RUNNING TEST T-04: NAVIGATION CHECK (NO OVER-ADVANCE)")
    seq = MusicSequencer()
    seq.insert_back("A4:1.0")
    seq.insert_back("B4:1.0")
    seq.move_forward()  # current: index 0 -> index 1 (the tail)
    print(f"Initial: {seq} | Current Index: {seq.current_index()} (at tail)")

    print("\nExecuting: move_forward() again, already at the tail")
    seq.move_forward()
    print(f"Current Index after extra move_forward(): {seq.current_index()}")

    assert seq.current_index() == 1, "Current should stay clamped at the tail index"
    print("Current stayed on the tail. No out-of-bounds advance. [SUCCESS]")
    end()
    seq.close()


def test_T05_single_element_list():
    banner("RUNNING TEST T-05: SIZE-1 LIST, REMOVE CURRENT")
    seq = MusicSequencer()
    seq.insert_back("C4:1.0")
    print(f"Initial List: {seq} | Size: {seq.size()} | Current Index: {seq.current_index()}")

    print("\nExecuting: remove_current() on a size-1 list")
    removed = seq.remove_current()
    print(f"Removed: {removed}")
    print(f"Result List: {seq} | Size: {seq.size()} | Current Index: {seq.current_index()}")

    assert seq.is_empty() and seq.current_index() == -1
    print("List is empty and current correctly reset to -1. [SUCCESS]")
    end()
    seq.close()


def test_T06_move_current_between_source_and_target():
    banner("RUNNING TEST T-06: MOVE WITH CURRENT STRICTLY BETWEEN SOURCE/TARGET")
    seq = MusicSequencer()
    for p in ["A4:1.0", "B4:1.0", "C4:1.0", "D4:1.0"]:
        seq.insert_back(p)
    seq.move_forward()
    seq.move_forward()  # current -> index 2, phrase C4:1.0
    print(f"Initial: {seq} | Current Index: {seq.current_index()} "
          f"(Current Phrase: {seq.current_phrase()})")

    print("\nExecuting: move_phrase(0, 2)  [source < current <= target]")
    seq.move_phrase(0, 2)
    print(f"Result: {seq} | Current Index: {seq.current_index()} "
          f"(Current Phrase: {seq.current_phrase()})")

    assert seq.current_phrase() == "C4:1.0", "current should still track C4, just shifted left"
    print("Current followed its phrase through the move. [SUCCESS]")
    end()
    seq.close()


def test_T07_move_noop_same_index():
    banner("RUNNING TEST T-07: MOVE TO SAME INDEX IS A NO-OP")
    seq = MusicSequencer()
    seq.insert_back("A4:1.0")
    seq.insert_back("B4:1.0")
    before = str(seq)
    print(f"Initial: {before}")

    print("\nExecuting: move_phrase(1, 1)")
    seq.move_phrase(1, 1)
    after = str(seq)
    print(f"Result: {after}")

    assert before == after, "list should be unchanged when source == target"
    print("List unchanged. [SUCCESS]")
    end()
    seq.close()


def test_T08_chord_token_round_trip():
    banner("RUNNING TEST T-08: CHORD TOKEN SURVIVES REPEAT_CURRENT")
    seq = MusicSequencer()
    seq.insert_back("C4+E4+G4:1.0")
    print(f"Initial: {seq}")

    print("\nExecuting: repeat_current()")
    seq.repeat_current()
    print(f"Result: {seq} | Size: {seq.size()}")

    assert seq.size() == 2
    assert seq.current_phrase() == "C4+E4+G4:1.0"
    print("Chord token duplicated intact. [SUCCESS]")
    end()
    seq.close()


if __name__ == "__main__":
    test_T01_empty_list_removal()
    test_T02_move_tail_to_head()
    test_T03_insert_out_of_bounds()
    test_T04_navigation_bounds()
    test_T05_single_element_list()
    test_T06_move_current_between_source_and_target()
    test_T07_move_noop_same_index()
    test_T08_chord_token_round_trip()
    print("\nAll boundary tests completed.")