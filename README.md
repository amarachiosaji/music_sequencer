# music_sequencer
Music Sequencer Project for class
Music Sequencer Project Lab Report

Name: Amarachi Osaji

Provide an introductory section describing the project and your approach:

For this assignment, I built a console-based Interactive Music Sequencer that stores and manipulates musical "phrases" using a custom-built doubly linked list implemented entirely from scratch, without relying on any built-in sequence structures (no Python list, deque, etc.).

The project is organized into four components, each with a distinct responsibility: doubly_ll.py (the data structure), music_sequencer.py (the domain layer), main.py (the interactive console driver), and midi_player.py.

My approach was to build and verify the system bottom-up rather than writing everything at once. I started with the lowest-level piece: the Node class and the raw pointer logic in LList. Then, I tested it in isolation before building anything that depended on it. Only once I was confident the pointer manipulation itself was alright did I build MusicSequencer on top of it, followed by the interactive main.py menu.

This order mattered most for the in-place move requirement, since the assignment explicitly disallows allocating a new Node or copying data between nodes during a move. I implemented this as an unlink step (detaching the node from its current position) followed by a re-link step (attaching the same node object at its new position), and verified it against the assignment's own example trace (moving a node from the tail to the head of a 3-node list, including confirming the backward links were correctly re-threaded) before trusting it inside the higher-level sequencer logic.

What is the asymptotic runtime of each of your functions and how do you know?:

Since the list is built from raw nodes rather than an array, it all comes down to how many pointers must be followed before doing O(1) work:

size(), is_empty() -> O(1): just reads a stored counter.
insert_first(x), insert_last(x) -> O(1): head/tail are tracked directly, no traversal needed.
get(i), remove_at(i), insert_at(i) -> O(min(i, n-i)): because _node_at(i) walks forward from head if i is in the first half, or backward from tail if it's in the second half, so it never has to cross more than half the list.
move(src, tgt) -> O(n) worst case: one seek to find the source node, one seek to find the target position (each O(min(index, n-index))); the actual unlink/re-link is O(1) regardless of how far the node moves.
iter_from(i) -> O(n) total when fully used: one seek to i, then O(1) per element walking .next forward; not O(1) per repeated get() call, which would make play_from_current() accidentally O(n²).
Full traversal (__iter__, __str__) -> O(n): has to visit every node once.

Edge cases: an empty list short-circuits every operation to O(1) via a bounds check; a size-1 list is O(1) everywhere since index 0 is equidistant from both ends; the true worst case is an index near the middle of a large list, O(n/2) → O(n).

MusicSequencer's methods inherit these costs directly plus O(1) for current_index; insert_front/insert_back/move_forward/move_backward stay O(1), everything else follows the underlying list operation it calls.

Describe how you tested your code, list your test cases, and provide a log of your test runs:

I tested my code in two parts:
(test_sequencer.py), which was 8 scripted scenarios covering the categories the assignment explicitly mentioned: an empty list, a size-1 list, out-of-bounds indices, in-place move (including the tail-to-head case from the assignment's own example), and the two different branches of how the current pointer has to shift when a move happens on either side of it.
(main.py), I ran it and in the terminal, I built an actual composition (entering "Happy Birthday" phrase by phrase), exercising every menu option including real audio playback, to confirm the system behaves correctly end-to-end, not just in isolated unit tests.

What was the most interesting part of this assignment?:

The most interesting part of this assignment was testing the finished sequencer, more so than writing the code itself. Actually hearing phrases play back as real audio, especially once I started testing with full songs instead of single notes, made the structure feel so cool in a way that writing the code logic alone didn't. It was during that testing phase that the role of the doubly linked list really clicked: I thought through the current tracking the right phrase through inserts and moves, hearing the composition play correctly from front to back and from the current position, and made the "node with prev/next pointers" concept visibly connect to hearing the audio result. 


What was the most challenging part of this assignment?:

The most challenging part was understanding how all the pieces actually fit together. One specific issue was, tracing why main.py only talks to MusicSequencer and never touches MidiPlayer directly, and why MidiPlayer lives inside MusicSequencer instead of being called from the top level. I had to reason through that layering and that was initially a bit confusing. Also, coming up with meaningful test cases was similarly difficult: it wasn't enough to check that an operation "worked," I had to think through what could actually go wrong at each boundary and create a scenario that would actually expose a bug if one existed.


How would you like to extend your solution (i.e., what other functions would you like to provide for this application)?:

I think two extensions would make this project meaningfully more usable, from a usability stand-point of having potential diverse users of this project. First, a graphical interface instead of a console menu, maybe something closer to a simple piano-roll or sheet view where phrases could be seen and rearranged visually rather than through numbered menu options. Second, and more specifically motivated by my own experience testing this: supporting alternate note-entry formats for people who don't read standard pitch notation. While building test songs, I had to look up the actual values for "Happy Birthday" even though I already knew the melody- what I actually remembered was the solfège scale (Do-Re-Mi-Fa-Sol-La-Ti-Do), which most people learn informally regardless of musical background. A natural extension would be a translator function that accepts solfège syllables (mapped to scale degrees relative to a chosen key) and converts them into the existing standardized notation internally, so the core data structure and playback engine wouldn't need to change at all, just an additional input layer in front of it.

Any feedback you’d like to provide about the assignment?

This was a genuinely engaging assignment, pairing a classic data structures exercise with real-time audio output made the doubly linked list feel like more than just an exercise. Hearing actual music come out of code I'd written myself, built entirely on node pointers, was honestly fascinating, and gave me a deeper understanding of the abstract structure (prev/next, head/tail).
