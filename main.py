from midi_player import MidiPlayer

def main():
    print("=================================================")
    print("  CSDS 233: Music Sequencer Demonstration Main   ")
    print("=================================================")

    # Initialize the real-time MIDI Player Engine
    player = MidiPlayer()

    # 1. Direct demonstration of playing individual phrases
    print("\nPlaying a basic Major Arpeggio...")
    arpeggio = "C4:0.25 E4:0.25 G4:0.25 C5:0.5 R:0.25 C5:0.25 G4:0.25 E4:0.25 C4:0.5"
    player.play(arpeggio)

    # 2. Demonstration of playing sequential phrases (simulating Doubly Linked List traversal)
    print("\nPlaying sequential phrases simulating list traversal...")
    mock_composition_list = [
        "C4:0.5 C4:0.5 G4:0.5 G4:0.5",  # Phrase 1
        "A4:0.5 A4:0.5 G4:1.0",          # Phrase 2
        "F4:0.5 F4:0.5 E4:0.5 E4:0.5",  # Phrase 3
        "D4:0.5 D4:0.5 C4:1.0"           # Phrase 4
    ]

    for i, phrase in enumerate(mock_composition_list):
        print(f"\nPlaying List Node [{i}]: {phrase}")
        player.play(phrase)

    # 3. Simple Interactive Console Menu Loop
    print("\n=================================================")
    print("            Interactive Player Test              ")
    print("=================================================")
    print("Format: PITCH:DURATION (separated by spaces)")
    print("Pitches: C4, D#4, Eb4, R (for rest), etc.")
    print("Durations: 0.25 (sixteenth), 0.5 (eighth), 1.0 (quarter)")
    print("Example input: E4:0.5 D#4:0.5 E4:0.5 B3:0.5 D4:0.5 C4:1.0")

    while True:
        try:
            user_input = input("\nEnter a musical phrase to play (or type 'exit' to quit): \n> ").strip()
            if user_input.lower() == 'exit':
                print("Exiting player...")
                break
            elif user_input:
                print("Playing phrase...")
                player.play(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting player...")
            break

    # Release MIDI interface resources cleanly
    player.close()
    print("MIDI Engine shutdown cleanly. Goodbye!")

if __name__ == "__main__":
    main()