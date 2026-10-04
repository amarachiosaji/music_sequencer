from music_sequencer import MusicSequencer


MENU = """
=================================================
          INTERACTIVE MUSIC SEQUENCER
=================================================
 1. Insert Front          2. Insert Back
 3. Insert After Current  4. Repeat Current
 5. Remove Current        6. Remove At Index
 7. Move Phrase (source -> target)
 8. Play All              9. Play From Current
10. Play Current         11. Move Forward
12. Move Backward        13. Show Composition
14. Exit
=================================================
"""


def prompt_phrase() -> str:
    print('Format: PITCH:DURATION tokens, e.g. "C4+E4+G4:1.0 G4:0.5 R:0.25"')
    return input("Enter phrase: ").strip()


def prompt_index(label: str) -> int:
    raw = input(f"Enter {label} (0-based index): ").strip()
    return int(raw)  # a bad int() triggers ValueError, caught below


def show_state(sequencer: MusicSequencer) -> None:
    print(f"\nSize: {sequencer.size()} | Current Index: {sequencer.current_index()}")
    print(f"Composition: {sequencer}")
    if not sequencer.is_empty():
        print(f"Current Phrase: {sequencer.current_phrase()}")


def main():
    sequencer = MusicSequencer()

    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()

            try:
                if choice == '1':
                    sequencer.insert_front(prompt_phrase())
                elif choice == '2':
                    sequencer.insert_back(prompt_phrase())
                elif choice == '3':
                    sequencer.insert_current(prompt_phrase())
                elif choice == '4':
                    sequencer.repeat_current()
                elif choice == '5':
                    removed = sequencer.remove_current()
                    print(f"Removed: {removed}")
                elif choice == '6':
                    idx = prompt_index("index to remove")
                    removed = sequencer.remove_specific(idx)
                    print(f"Removed: {removed}")
                elif choice == '7':
                    src = prompt_index("source index")
                    tgt = prompt_index("target index")
                    sequencer.move_phrase(src, tgt, verbose=True)
                elif choice == '8':
                    sequencer.play_all()
                elif choice == '9':
                    sequencer.play_from_current()
                elif choice == '10':
                    sequencer.play_current()
                elif choice == '11':
                    sequencer.move_forward()
                elif choice == '12':
                    sequencer.move_backward()
                elif choice == '13':
                    pass  # falls through to show_state() below
                elif choice == '14':
                    print("Exiting sequencer...")
                    break
                else:
                    print("Unrecognized option, try again.")
                    continue

                show_state(sequencer)

            except (IndexError, ValueError) as e:
                print(f"[WARNING] Operation rejected: {e}")

    except (KeyboardInterrupt, EOFError):
        print("\nExiting sequencer...")

    finally:
        sequencer.close()
        print("MIDI Engine shut down cleanly. Goodbye!")


if __name__ == "__main__":
    main()